from datetime import datetime, timezone
import hashlib
import uuid

import pytest

from app.contributions import (
    AudioDurationInvalid,
    AudioFormatUnsupported,
    begin_audio_upload,
    create_contribution,
    finalise_audio,
)
from app.identity import AuthenticatedIdentity
from app.models import Campaign, CampaignRewardRule, Card, ConsentGrant, ConsentScope, ContributionState, User
from app.storage import LocalAudioObjectStore


@pytest.fixture
def contribution_context(db_session, tmp_path):
    now = datetime.now(timezone.utc)
    speaker = User(id=uuid.uuid4(), provider_subject="speaker", declared_languages=["tn"], age_confirmed_at=now, created_at=now)
    campaign = Campaign(id=uuid.uuid4(), name="Test", language="tn", budget_cents=1000, funded_cents=1000, committed_cents=0, provider_mode="DEMO_PROVIDER")
    rule = CampaignRewardRule(id=uuid.uuid4(), campaign_id=campaign.id, version="v1", contribution_reward_cents=100, effective_from=now)
    card = Card(id=uuid.uuid4(), language="tn", target="kgomo", blocked_words=["a", "b", "c", "d"], accepted_answers=["kgomo", "kgomo"], distractors=["x", "y", "z"], campaign_id=campaign.id, active=True)
    db_session.add_all([speaker, campaign, rule, card])
    db_session.commit()
    principal = AuthenticatedIdentity(user_id=speaker.id, provider_subject=speaker.provider_subject)
    store = LocalAudioObjectStore(tmp_path, secret=b"task-4-secret")
    return speaker, campaign, rule, card, principal, store


def test_contribution_creation_requires_round_consent(db_session, contribution_context):
    _, _, _, card, principal, _ = contribution_context
    with pytest.raises(Exception, match="active consent required"):
        create_contribution(db_session, principal=principal, card_id=card.id)


def test_contribution_creation_snapshots_active_reward_rule(db_session, contribution_context):
    speaker, _, rule, card, principal, _ = contribution_context
    db_session.add(ConsentGrant(user_id=speaker.id, version="2026-09-01", scope=ConsentScope.RECORD_PROCESS_ROUND))
    db_session.commit()
    contribution = create_contribution(db_session, principal=principal, card_id=card.id)
    db_session.commit()
    assert contribution.speaker_id == speaker.id
    assert contribution.reward_rule_id == rule.id
    assert contribution.state == ContributionState.DRAFT


def test_finalise_audio_rejects_unsupported_format_and_invalid_duration(db_session, contribution_context):
    speaker, _, _, card, principal, store = contribution_context
    db_session.add(ConsentGrant(user_id=speaker.id, version="2026-09-01", scope=ConsentScope.RECORD_PROCESS_ROUND))
    db_session.commit()
    contribution = create_contribution(db_session, principal=principal, card_id=card.id)
    db_session.commit()
    audio = begin_audio_upload(db_session, store, contribution.id, speaker.id)
    store.write_upload(audio.object_key, b"voice")
    with pytest.raises(AudioFormatUnsupported):
        finalise_audio(db_session, store, contribution.id, hashlib.sha256(b"voice").hexdigest(), "audio/mp3", "mp3", 1000, 5)
    with pytest.raises(AudioDurationInvalid):
        finalise_audio(db_session, store, contribution.id, hashlib.sha256(b"voice").hexdigest(), "audio/webm", "opus", 100, 5)
