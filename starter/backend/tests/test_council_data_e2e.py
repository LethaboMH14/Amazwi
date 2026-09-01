from datetime import datetime, timezone
import uuid

from app.datasets import approve_export, create_export, revoke_export
from app.models import (
    AudioObject, AudioObjectState, Card, Campaign, ConsentGrant, ConsentScope,
    Contribution, ContributionState, User,
)


def test_resolved_opted_in_contribution_can_be_approved_and_revoked(db_session):
    now = datetime.now(timezone.utc)
    speaker = User(id=uuid.uuid4(), provider_subject="export-speaker", declared_languages=["tn"], age_confirmed_at=now, created_at=now)
    campaign = Campaign(id=uuid.uuid4(), name="Export", language="tn", budget_cents=1000, funded_cents=1000, committed_cents=0, provider_mode="DEMO_PROVIDER")
    card = Card(id=uuid.uuid4(), language="tn", target="kgomo", blocked_words=["a", "b", "c", "d"], accepted_answers=["kgomo", "kgomo"], distractors=["x", "y", "z"], campaign_id=campaign.id, active=True)
    contribution = Contribution(id=uuid.uuid4(), speaker_id=speaker.id, card_id=card.id, declared_language="tn", state=ContributionState.CORPUS_ELIGIBLE)
    audio = AudioObject(id=uuid.uuid4(), contribution_id=contribution.id, object_key="final/audio", sha256="a" * 64, state=AudioObjectState.AVAILABLE, byte_length=4, duration_ms=1000)
    consent = ConsentGrant(user_id=speaker.id, version="model-v1", scope=ConsentScope.RETAIN_MODEL_DEVELOPMENT, granted_at=now)
    db_session.add(speaker)
    db_session.flush()
    db_session.add(campaign)
    db_session.flush()
    db_session.add(card)
    db_session.flush()
    db_session.add(contribution)
    db_session.flush()
    db_session.add(consent)
    db_session.flush()
    db_session.add(audio)
    db_session.flush()

    export = create_export(db_session, purpose="ASR training", requested_by=speaker.id, rows=[{"source_class": "AMAZWI_OPTED_IN", "source_record_id": "record-1", "contribution_id": contribution.id, "object_sha256": "a" * 64}])
    approved = approve_export(db_session, export_id=export.id, actor_id=speaker.id, manifest_id="manifest-1", manifest_sha256="b" * 64)
    assert approved.state.value == "APPROVED"
    revoked = revoke_export(db_session, export_id=export.id, actor_id=speaker.id)
    assert revoked.state.value == "REVOKED"


def test_export_rejects_missing_model_consent(db_session):
    now = datetime.now(timezone.utc)
    speaker = User(id=uuid.uuid4(), provider_subject="export-no-consent", declared_languages=["tn"], age_confirmed_at=now, created_at=now)
    campaign = Campaign(id=uuid.uuid4(), name="Export", language="tn", budget_cents=1000, funded_cents=1000, committed_cents=0, provider_mode="DEMO_PROVIDER")
    card = Card(id=uuid.uuid4(), language="tn", target="kgomo", blocked_words=["a", "b", "c", "d"], accepted_answers=["kgomo", "kgomo"], distractors=["x", "y", "z"], campaign_id=campaign.id, active=True)
    contribution = Contribution(id=uuid.uuid4(), speaker_id=speaker.id, card_id=card.id, declared_language="tn", state=ContributionState.CORPUS_ELIGIBLE)
    audio = AudioObject(id=uuid.uuid4(), contribution_id=contribution.id, object_key="final/audio-2", sha256="a" * 64, state=AudioObjectState.AVAILABLE, byte_length=4, duration_ms=1000)
    db_session.add(speaker)
    db_session.flush()
    db_session.add(campaign)
    db_session.flush()
    db_session.add(card)
    db_session.flush()
    db_session.add(contribution)
    db_session.flush()
    db_session.add(audio)
    db_session.flush()
    import pytest
    from app.datasets import ExportRejected
    with pytest.raises(ExportRejected):
        create_export(db_session, purpose="ASR training", requested_by=speaker.id, rows=[{"source_class": "AMAZWI_OPTED_IN", "source_record_id": "record-2", "contribution_id": contribution.id, "object_sha256": "a" * 64}])
