from datetime import datetime, timezone
import uuid

from fastapi.testclient import TestClient

from app.datasets import approve_export, create_export, revoke_export
from app.council import DataStewardRulesV1, ExplainerRulesV1, LanguageScoutRulesV1, SoundSentinelRulesV1, run_council_event
from app.db import get_session
from app.identity import AuthenticatedIdentity, get_current_identity
from app.main import app
from app.models import (
    Assignment, AssignmentMode, AudioObject, AudioObjectState, Card, Campaign,
    CampaignRewardRule, ConsentGrant, ConsentScope, Contribution,
    ContributionState, EligibilityDecision, OutboxEvent, User,
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

    event = OutboxEvent(event_type="ContributionResolved", aggregate_type="Contribution", aggregate_id=contribution.id, dedupe_key=f"e2e:{contribution.id}", payload_json={"contribution_id": str(contribution.id), "language": "tn", "peer_understood": True, "audio_quality_passed": True, "model_consent_active": True})
    db_session.add(event)
    db_session.flush()
    council = run_council_event(db_session, event, [DataStewardRulesV1(), SoundSentinelRulesV1(), LanguageScoutRulesV1(), ExplainerRulesV1()], now)
    assert council[0].output_json["code"] == "TRAINING_READY"

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


def test_resolver_reward_outbox_and_retry_are_idempotent(db_session):
    from app.outbox import claim_events, retry_event
    from app.resolver import resolve_contribution

    now = datetime.now(timezone.utc)
    speaker = User(id=uuid.uuid4(), provider_subject="resolver-export", declared_languages=["tn"])
    v1 = User(id=uuid.uuid4(), provider_subject="resolver-v1", declared_languages=["tn"])
    v2 = User(id=uuid.uuid4(), provider_subject="resolver-v2", declared_languages=["tn"])
    campaign = Campaign(id=uuid.uuid4(), name="Resolver", language="tn", budget_cents=1000, funded_cents=1000, committed_cents=0, provider_mode="DEMO_PROVIDER")
    card = Card(id=uuid.uuid4(), language="tn", target="kgomo", blocked_words=["a", "b", "c", "d"], accepted_answers=["kgomo", "kgomo"], distractors=["x", "y", "z"], campaign_id=campaign.id)
    rule = CampaignRewardRule(id=uuid.uuid4(), campaign_id=campaign.id, version="r1", contribution_reward_cents=100, effective_from=now)
    contribution = Contribution(id=uuid.uuid4(), speaker_id=speaker.id, card_id=card.id, declared_language="tn", state=ContributionState.OPEN, reward_rule_id=rule.id)
    db_session.add_all([speaker, v1, v2])
    db_session.flush()
    db_session.add(campaign)
    db_session.flush()
    db_session.add(card)
    db_session.flush()
    db_session.add(rule)
    db_session.flush()
    db_session.add(contribution)
    db_session.flush()
    db_session.add_all([
        ConsentGrant(user_id=speaker.id, version="c1", scope=ConsentScope.RECORD_PROCESS_ROUND),
        AudioObject(contribution_id=contribution.id, object_key="resolver/audio", sha256="a" * 64, state=AudioObjectState.AVAILABLE, byte_length=4, duration_ms=1000),
        Assignment(contribution_id=contribution.id, verifier_id=v1.id, mode=AssignmentMode.PROFICIENT_VERIFIER, matched=True, violation_vote=False, answered_at=now),
        Assignment(contribution_id=contribution.id, verifier_id=v2.id, mode=AssignmentMode.PROFICIENT_VERIFIER, matched=True, violation_vote=False, answered_at=now),
    ])
    db_session.commit()
    decision = resolve_contribution(db_session, contribution_id=contribution.id, audio_quality_passed=True, consent_active=True, reward_amount_cents=100, campaign_id=campaign.id)
    assert decision.corpus_eligible is True
    assert db_session.query(EligibilityDecision).filter_by(contribution_id=contribution.id).count() == 1
    events = db_session.query(OutboxEvent).filter_by(aggregate_id=contribution.id).all()
    assert len(events) == 1
    claimed = claim_events(db_session, worker_id="e2e-worker", now=datetime.now(timezone.utc), limit=1)
    assert len(claimed) == 1
    retry_at = retry_event(db_session, claimed[0].id, "e2e-worker", datetime.now(timezone.utc), "temporary")
    assert retry_at > datetime.now(timezone.utc)


def test_governed_export_routes_complete_public_acceptance_path(db_session):
    now = datetime.now(timezone.utc)
    speaker = User(
        id=uuid.uuid4(),
        provider_subject="export-api-speaker",
        declared_languages=["tn"],
        age_confirmed_at=now,
        created_at=now,
    )
    campaign = Campaign(
        id=uuid.uuid4(),
        name="Export API",
        language="tn",
        budget_cents=1000,
        funded_cents=1000,
        committed_cents=0,
        provider_mode="DEMO_PROVIDER",
    )
    card = Card(
        id=uuid.uuid4(),
        language="tn",
        target="kgomo",
        blocked_words=["a", "b", "c", "d"],
        accepted_answers=["kgomo", "kgomo"],
        distractors=["x", "y", "z"],
        campaign_id=campaign.id,
        active=True,
    )
    contribution = Contribution(
        id=uuid.uuid4(),
        speaker_id=speaker.id,
        card_id=card.id,
        declared_language="tn",
        state=ContributionState.CORPUS_ELIGIBLE,
    )
    db_session.add(speaker)
    db_session.flush()
    db_session.add(campaign)
    db_session.flush()
    db_session.add(card)
    db_session.flush()
    db_session.add(contribution)
    db_session.flush()
    db_session.add_all(
        [
            AudioObject(
                id=uuid.uuid4(),
                contribution_id=contribution.id,
                object_key="api/audio",
                sha256="a" * 64,
                state=AudioObjectState.AVAILABLE,
                byte_length=4,
                duration_ms=1000,
            ),
            ConsentGrant(
                user_id=speaker.id,
                version="model-v1",
                scope=ConsentScope.RETAIN_MODEL_DEVELOPMENT,
                granted_at=now,
            ),
        ]
    )
    db_session.commit()

    app.dependency_overrides[get_session] = lambda: db_session
    app.dependency_overrides[get_current_identity] = lambda: AuthenticatedIdentity(
        speaker.id, speaker.provider_subject
    )
    try:
        with TestClient(app) as client:
            drafted = client.post(
                "/dataset-exports",
                json={
                    "purpose": "ASR training",
                    "rows": [
                        {
                            "source_class": "AMAZWI_OPTED_IN",
                            "source_record_id": "record-api-1",
                            "contribution_id": str(contribution.id),
                            "object_sha256": "a" * 64,
                        }
                    ],
                },
            )
            assert drafted.status_code == 201, drafted.text
            export_id = drafted.json()["id"]
            assert drafted.json()["state"] == "DRAFT"

            approved = client.post(
                f"/dataset-exports/{export_id}/approve",
                json={"manifest_id": "manifest-api-1", "manifest_sha256": "b" * 64},
            )
            assert approved.status_code == 200, approved.text
            assert approved.json()["state"] == "APPROVED"
            assert approved.json()["manifest_sha256"] == "b" * 64

            revoked = client.post(f"/dataset-exports/{export_id}/revoke")
            assert revoked.status_code == 200, revoked.text
            assert revoked.json()["state"] == "REVOKED"

            model_consent = db_session.query(ConsentGrant).filter_by(
                user_id=speaker.id, scope=ConsentScope.RETAIN_MODEL_DEVELOPMENT
            ).one()
            db_session.delete(model_consent)
            db_session.commit()
            rejected = client.post(
                "/dataset-exports",
                json={
                    "purpose": "ASR training",
                    "rows": [
                        {
                            "source_class": "AMAZWI_OPTED_IN",
                            "source_record_id": "record-api-2",
                            "contribution_id": str(contribution.id),
                            "object_sha256": "a" * 64,
                        }
                    ],
                },
            )
            assert rejected.status_code == 422, rejected.text
            assert "consent" in rejected.json()["detail"].lower()
    finally:
        app.dependency_overrides.clear()
