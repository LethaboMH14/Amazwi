from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.consent import require_active_scope
from app.identity import AuthenticatedIdentity
from app.models import (
    Assignment,
    AudioObject,
    AudioObjectState,
    Campaign,
    CampaignRewardRule,
    Card,
    ConsentScope,
    Contribution,
    ContributionState,
)
from app.storage import AudioUnavailable, LocalAudioObjectStore


class ContributionError(Exception):
    pass


class CampaignRewardNotConfigured(ContributionError):
    pass


class AudioFormatUnsupported(ContributionError):
    pass


class AudioDurationInvalid(ContributionError):
    pass


class AudioNotAuthorised(ContributionError):
    pass


def create_contribution(
    session: Session,
    *,
    principal: AuthenticatedIdentity,
    card_id: uuid.UUID,
) -> Contribution:
    require_active_scope(session, principal.user_id, ConsentScope.RECORD_PROCESS_ROUND)
    card = session.scalar(select(Card).where(Card.id == card_id).with_for_update())
    if card is None or not card.active:
        raise ContributionError("card is not active")
    campaign = session.scalar(select(Campaign).where(Campaign.id == card.campaign_id).with_for_update())
    rule = session.scalar(
        select(CampaignRewardRule)
        .where(
            CampaignRewardRule.campaign_id == card.campaign_id,
            CampaignRewardRule.retired_at.is_(None),
        )
        .with_for_update()
    )
    if campaign is None or rule is None:
        raise CampaignRewardNotConfigured("CAMPAIGN_REWARD_NOT_CONFIGURED")
    contribution = Contribution(
        speaker_id=principal.user_id,
        card_id=card.id,
        declared_language=card.language,
        state=ContributionState.DRAFT,
        created_at=datetime.now(timezone.utc),
        reward_rule_id=rule.id,
    )
    session.add(contribution)
    session.flush()
    return contribution


def begin_audio_upload(
    session: Session,
    store: LocalAudioObjectStore,
    contribution_id: uuid.UUID,
    speaker_id: uuid.UUID,
) -> AudioObject:
    contribution = session.get(Contribution, contribution_id)
    if contribution is None or contribution.speaker_id != speaker_id:
        raise AudioNotAuthorised("AUDIO_NOT_AUTHORISED")
    require_active_scope(session, speaker_id, ConsentScope.RECORD_PROCESS_ROUND)
    existing = session.scalar(select(AudioObject).where(AudioObject.contribution_id == contribution_id))
    if existing is not None:
        return existing
    audio = AudioObject(
        contribution_id=contribution_id,
        object_key=f"audio/{contribution_id}",
        state=AudioObjectState.PENDING,
        created_at=datetime.now(timezone.utc),
    )
    session.add(audio)
    session.flush()
    return audio


def finalise_audio(
    session: Session,
    store: LocalAudioObjectStore,
    contribution_id: uuid.UUID,
    sha256: str,
    mime_type: str,
    codec: str,
    duration_ms: int,
    byte_length: int,
) -> AudioObject:
    if mime_type not in {"audio/webm", "audio/ogg", "audio/wav"}:
        raise AudioFormatUnsupported("AUDIO_FORMAT_UNSUPPORTED")
    if not 500 <= duration_ms <= 20_000:
        raise AudioDurationInvalid("AUDIO_DURATION_INVALID")
    contribution = session.get(Contribution, contribution_id)
    audio = session.scalar(select(AudioObject).where(AudioObject.contribution_id == contribution_id).with_for_update())
    if contribution is None or audio is None:
        raise AudioUnavailable("AUDIO_UNAVAILABLE")
    require_active_scope(session, contribution.speaker_id, ConsentScope.RECORD_PROCESS_ROUND)
    stored = store.verify(audio.object_key, sha256, byte_length)
    store.finalise(stored)
    audio.sha256 = stored.sha256
    audio.byte_length = stored.byte_length
    audio.mime_type = mime_type
    audio.codec = codec
    audio.duration_ms = duration_ms
    audio.state = AudioObjectState.AVAILABLE
    audio.finalised_at = datetime.now(timezone.utc)
    contribution.audio_key = audio.object_key
    contribution.duration_ms = duration_ms
    contribution.quality_json = json.dumps({"physical": {"mime_type": mime_type, "codec": codec, "duration_ms": duration_ms, "sha256": stored.sha256}})
    contribution.state = ContributionState.RECORDED
    session.flush()
    return audio


def issue_contributor_playback_token(
    session: Session,
    store: LocalAudioObjectStore,
    contribution_id: uuid.UUID,
    principal: AuthenticatedIdentity,
) -> str:
    contribution = session.get(Contribution, contribution_id)
    if contribution is None or contribution.speaker_id != principal.user_id:
        raise AudioNotAuthorised("AUDIO_NOT_AUTHORISED")
    require_active_scope(session, principal.user_id, ConsentScope.RECORD_PROCESS_ROUND)
    audio = session.scalar(select(AudioObject).where(AudioObject.contribution_id == contribution_id))
    if audio is None or audio.state != AudioObjectState.AVAILABLE:
        raise AudioUnavailable("AUDIO_UNAVAILABLE")
    return store.issue_token(
        audio.object_key,
        audience=str(principal.user_id),
        purpose="REPLAY",
        ttl_seconds=300,
        now=datetime.now(timezone.utc),
    )


def issue_verifier_playback_token(
    session: Session,
    store: LocalAudioObjectStore,
    assignment_id: uuid.UUID,
    principal: AuthenticatedIdentity,
) -> str:
    """Issue a short-lived URL only to the verifier assigned this clip."""
    assignment = session.get(Assignment, assignment_id)
    if assignment is None or assignment.verifier_id != principal.user_id:
        raise AudioNotAuthorised("AUDIO_NOT_AUTHORISED")
    contribution = session.get(Contribution, assignment.contribution_id)
    if contribution is None:
        raise AudioUnavailable("AUDIO_UNAVAILABLE")
    require_active_scope(session, contribution.speaker_id, ConsentScope.ASSIGNED_VERIFIER_PLAYBACK)
    require_active_scope(session, principal.user_id, ConsentScope.ASSIGNED_VERIFIER_PLAYBACK)
    audio = session.scalar(select(AudioObject).where(AudioObject.contribution_id == contribution.id))
    if audio is None or audio.state != AudioObjectState.AVAILABLE:
        raise AudioUnavailable("AUDIO_UNAVAILABLE")
    return store.issue_token(
        audio.object_key,
        audience=str(principal.user_id),
        purpose="VERIFY",
        ttl_seconds=300,
        now=datetime.now(timezone.utc),
    )
