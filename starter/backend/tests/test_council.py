"""Council determinism, idempotency, authority isolation, and status states.

Closes Final Acceptance Checklist items 3 and 4 of
docs/superpowers/plans/2026-09-01-amazwi-02-council-data-models.md:

  3. "Council outputs are versioned, canonically hashed, independently
     retryable, and idempotent per event/specialist/version."
  4. "AI-disabled, pending, partial, failed, and exhausted states preserve
     peer truth, reward, wallet, receipt, and result polling."

Before this file, app/routes/council.py and scripts/run_council_worker.py
had no test coverage at all: test_council_schema.py proved the uniqueness
constraint at the DB level, but nothing proved that run_council_event
respects it, that a failing specialist leaves its siblings intact, or that
the status route reports the right state.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import uuid

import pytest
from fastapi.testclient import TestClient

from app import council as council_module
from app.council import (
    DataStewardRulesV1,
    ExplainerRulesV1,
    LanguageScoutRulesV1,
    ResolutionFacts,
    SoundSentinelRulesV1,
    SpecialistResult,
    canonical_sha256,
    run_council_event,
)
from app.db import get_session
from app.identity import AuthenticatedIdentity, get_current_identity
from app.main import app
from app.models import (
    AudioObject,
    AudioObjectState,
    Card,
    Campaign,
    Contribution,
    ContributionState,
    CouncilOutput,
    CouncilOutputState,
    OutboxEvent,
    RewardEvent,
    User,
)
from app.outbox import COUNCIL_ATTEMPTS_EXHAUSTED, claim_events
from app.routes import council as council_route
from scripts.run_council_worker import process_once

NOW = datetime(2026, 9, 2, 12, 0, 0, tzinfo=timezone.utc)
ALL_SPECIALISTS = (DataStewardRulesV1, SoundSentinelRulesV1, LanguageScoutRulesV1, ExplainerRulesV1)


class ExplodingSpecialist:
    """A specialist that always fails, to prove sibling isolation."""

    name = "SOUND_SENTINEL"
    version = "rules-1"

    def run(self, facts):
        raise RuntimeError("model unavailable")


def _speaker(db_session, subject: str) -> User:
    user = User(id=uuid.uuid4(), provider_subject=subject, declared_languages=["tn"],
                age_confirmed_at=NOW, created_at=NOW)
    db_session.add(user)
    db_session.flush()
    return user


def _contribution(db_session, speaker: User, *, state=ContributionState.CORPUS_ELIGIBLE) -> Contribution:
    campaign = Campaign(id=uuid.uuid4(), name="Council", language="tn", budget_cents=1000,
                        funded_cents=1000, committed_cents=0, provider_mode="DEMO_PROVIDER")
    db_session.add(campaign)
    db_session.flush()
    card = Card(id=uuid.uuid4(), language="tn", target="kgomo", blocked_words=["a", "b", "c", "d"],
                accepted_answers=["kgomo", "kgomo"], distractors=["x", "y", "z"],
                campaign_id=campaign.id, active=True)
    db_session.add(card)
    db_session.flush()
    contribution = Contribution(id=uuid.uuid4(), speaker_id=speaker.id, card_id=card.id,
                                declared_language="tn", state=state)
    db_session.add(contribution)
    db_session.flush()
    db_session.add(AudioObject(id=uuid.uuid4(), contribution_id=contribution.id,
                               object_key=f"council/{contribution.id}", sha256="a" * 64,
                               state=AudioObjectState.AVAILABLE, byte_length=4, duration_ms=1000))
    db_session.commit()
    return contribution


def _event(db_session, contribution: Contribution, **payload) -> OutboxEvent:
    body = {
        "contribution_id": str(contribution.id),
        "language": "tn",
        "peer_understood": True,
        "audio_quality_passed": True,
        "model_consent_active": True,
    }
    body.update(payload)
    event = OutboxEvent(event_type="ContributionResolved", aggregate_type="Contribution",
                        aggregate_id=contribution.id, dedupe_key=f"council:{contribution.id}",
                        payload_json=body, occurred_at=NOW, available_at=NOW)
    db_session.add(event)
    db_session.commit()
    return event


# --- Checklist item 3: versioned, hashed, retryable, idempotent ---------------


def test_canonical_hash_ignores_key_order_but_not_values():
    a = canonical_sha256({"b": 2, "a": 1})
    b = canonical_sha256({"a": 1, "b": 2})
    c = canonical_sha256({"a": 1, "b": 3})
    assert a == b, "canonical JSON must sort keys, or manifest hashes drift on dict order"
    assert a != c
    assert len(a) == 64


def test_specialist_results_are_deterministic_for_identical_facts():
    facts = ResolutionFacts(contribution_id="c1", language="tn", peer_understood=True,
                            audio_quality_passed=True, model_consent_active=True)
    for specialist_cls in ALL_SPECIALISTS:
        first = specialist_cls().run(facts)
        second = specialist_cls().run(facts)
        assert (first.code, first.evidence) == (second.code, second.evidence)


def test_specialist_codes_are_exact_for_each_governed_input():
    base = dict(contribution_id="c1", language="tn", peer_understood=True,
                audio_quality_passed=True, model_consent_active=True)
    steward = DataStewardRulesV1()
    assert steward.run(ResolutionFacts(**base)).code == "TRAINING_READY"
    assert steward.run(ResolutionFacts(**{**base, "model_consent_active": False})).code == "BLOCKED_CONSENT"
    assert steward.run(ResolutionFacts(**base, source_class="EVALUATION_ONLY")).code == "BLOCKED_LICENCE"
    assert steward.run(ResolutionFacts(**base, source_class="SYNTHETIC_FIXTURE")).code == "BLOCKED_LICENCE"
    assert steward.run(ResolutionFacts(**base, source_class="EXTERNAL_LICENSED")).code == "TRAINING_READY"
    assert SoundSentinelRulesV1().run(ResolutionFacts(**base)).code == "RECORDING_OK"
    assert SoundSentinelRulesV1().run(
        ResolutionFacts(**{**base, "audio_quality_passed": False})).code == "RE_RECORD_RISK"
    assert ExplainerRulesV1().run(ResolutionFacts(**base)).evidence == {"authority": "peer_resolution"}


def test_council_run_is_idempotent_per_event_specialist_and_version(db_session):
    speaker = _speaker(db_session, "council-idem")
    contribution = _contribution(db_session, speaker)
    event = _event(db_session, contribution)
    specialists = [cls() for cls in ALL_SPECIALISTS]

    first = run_council_event(db_session, event, specialists, NOW)
    second = run_council_event(db_session, event, specialists, NOW + timedelta(hours=1))

    assert len(first) == 4
    assert [row.id for row in first] == [row.id for row in second], "a re-run must reuse rows, not insert new ones"
    assert db_session.query(CouncilOutput).filter_by(event_id=event.id).count() == 4
    assert {row.model_version for row in second} == {"rules-1"}
    assert all(row.state == CouncilOutputState.SUCCEEDED for row in second)
    assert len({row.input_sha256 for row in second}) == 1, "all specialists see the same redacted input hash"
    assert second[0].completed_at == NOW, "an already-succeeded row is not re-timestamped"


def test_input_hash_is_the_canonical_hash_of_the_redacted_facts_only(db_session):
    """The hash must cover the redacted fact set -- not raw audio, not the payload."""
    speaker = _speaker(db_session, "council-hash")
    contribution = _contribution(db_session, speaker)
    event = _event(db_session, contribution, secret_field="must-not-be-hashed")

    outputs = run_council_event(db_session, event, [DataStewardRulesV1()], NOW)

    expected = canonical_sha256({
        "contribution_id": str(contribution.id),
        "language": "tn",
        "peer_understood": True,
        "audio_quality_passed": True,
        "model_consent_active": True,
        "source_class": "AMAZWI_OPTED_IN",
    })
    assert outputs[0].input_sha256 == expected


def test_a_failing_specialist_does_not_lose_its_siblings_and_is_retryable(db_session):
    speaker = _speaker(db_session, "council-partial")
    contribution = _contribution(db_session, speaker)
    event = _event(db_session, contribution)

    partial = [DataStewardRulesV1(), ExplodingSpecialist(), LanguageScoutRulesV1(), ExplainerRulesV1()]
    outputs = run_council_event(db_session, event, partial, NOW)

    by_name = {row.specialist: row for row in outputs}
    assert by_name["SOUND_SENTINEL"].state == CouncilOutputState.FAILED
    assert by_name["SOUND_SENTINEL"].failure_reason == "model unavailable"
    assert by_name["SOUND_SENTINEL"].retry_count == 1
    for name in ("DATA_STEWARD", "LANGUAGE_SCOUT", "EXPLAINER"):
        assert by_name[name].state == CouncilOutputState.SUCCEEDED, "a sibling failure must not roll back successes"
        assert by_name[name].output_json is not None

    # Independently retryable: rerunning with a working specialist repairs
    # only the failed row and leaves the succeeded rows byte-identical.
    succeeded_before = {
        name: (by_name[name].id, by_name[name].output_json)
        for name in ("DATA_STEWARD", "LANGUAGE_SCOUT", "EXPLAINER")
    }
    repaired = run_council_event(db_session, event, [cls() for cls in ALL_SPECIALISTS], NOW + timedelta(minutes=5))
    repaired_by_name = {row.specialist: row for row in repaired}

    assert repaired_by_name["SOUND_SENTINEL"].state == CouncilOutputState.SUCCEEDED
    assert repaired_by_name["SOUND_SENTINEL"].id == by_name["SOUND_SENTINEL"].id, "retry reuses the row"
    assert repaired_by_name["SOUND_SENTINEL"].output_json["code"] == "RECORDING_OK"
    assert db_session.query(CouncilOutput).filter_by(event_id=event.id).count() == 4
    for name, (row_id, output) in succeeded_before.items():
        assert repaired_by_name[name].id == row_id
        assert repaired_by_name[name].output_json == output


def test_council_never_mutates_peer_reward_or_contribution_authority_state(db_session):
    """Specialists are advisory. Running them must change nothing authoritative."""
    speaker = _speaker(db_session, "council-authority")
    contribution = _contribution(db_session, speaker)
    event = _event(db_session, contribution, model_consent_active=False, audio_quality_passed=False)

    before_state = contribution.state
    before_rewards = db_session.query(RewardEvent).count()
    before_audio = db_session.query(AudioObject).filter_by(contribution_id=contribution.id).one()
    before_audio_state = before_audio.state

    outputs = run_council_event(db_session, event, [cls() for cls in ALL_SPECIALISTS], NOW)
    assert {row.output_json["code"] for row in outputs} == {
        "BLOCKED_CONSENT", "RE_RECORD_RISK", "LANGUAGE_REVIEW", "ADVISORY_ONLY",
    }, "the Council may disagree with the peer outcome without changing it"

    db_session.refresh(contribution)
    db_session.refresh(before_audio)
    assert contribution.state == before_state
    assert db_session.query(RewardEvent).count() == before_rewards
    assert before_audio.state == before_audio_state


# --- Checklist item 4: disabled / pending / partial / failed / exhausted ------


@pytest.fixture()
def council_client(db_session):
    app.dependency_overrides[get_session] = lambda: db_session
    yield lambda user: _client_for(db_session, user)
    app.dependency_overrides.clear()


def _client_for(db_session, user: User) -> TestClient:
    app.dependency_overrides[get_current_identity] = lambda: AuthenticatedIdentity(
        user.id, user.provider_subject
    )
    return TestClient(app)


def _status(client_factory, user, contribution):
    with client_factory(user) as client:
        response = client.get(f"/contributions/{contribution.id}/council")
    assert response.status_code == 200, response.text
    return response.json()


def test_status_is_disabled_when_the_council_flag_is_off(council_client, db_session, monkeypatch):
    speaker = _speaker(db_session, "council-disabled")
    contribution = _contribution(db_session, speaker)
    event = _event(db_session, contribution)
    run_council_event(db_session, event, [cls() for cls in ALL_SPECIALISTS], NOW)

    # app/routes/council.py binds the flag by value at import time
    # (`from app.config import AI_COUNCIL_ENABLED`), so the route's own
    # module attribute is the one that must be patched. Patching
    # app.config alone would silently have no effect.
    monkeypatch.setattr(council_route, "AI_COUNCIL_ENABLED", False)
    body = _status(council_client, speaker, contribution)

    assert body == {"state": "DISABLED", "outputs": []}, "disabled mode must leak no Council output"


def test_status_is_pending_when_no_resolution_event_exists(council_client, db_session, monkeypatch):
    monkeypatch.setattr(council_route, "AI_COUNCIL_ENABLED", True)
    speaker = _speaker(db_session, "council-pending")
    contribution = _contribution(db_session, speaker, state=ContributionState.OPEN)
    db_session.commit()

    assert _status(council_client, speaker, contribution) == {"state": "PENDING", "outputs": []}


def test_status_is_ready_and_ordered_when_every_specialist_succeeded(council_client, db_session, monkeypatch):
    monkeypatch.setattr(council_route, "AI_COUNCIL_ENABLED", True)
    speaker = _speaker(db_session, "council-ready")
    contribution = _contribution(db_session, speaker)
    event = _event(db_session, contribution)
    run_council_event(db_session, event, [cls() for cls in ALL_SPECIALISTS], NOW)

    body = _status(council_client, speaker, contribution)

    assert body["state"] == "READY"
    assert [row["specialist"] for row in body["outputs"]] == [
        "DATA_STEWARD", "SOUND_SENTINEL", "LANGUAGE_SCOUT", "EXPLAINER",
    ], "presentation order is fixed, not database order"
    assert body["outputs"][0]["output"]["code"] == "TRAINING_READY"
    assert all(row["model_version"] == "rules-1" for row in body["outputs"])
    assert all(row["failure_reason"] is None for row in body["outputs"])


def test_status_is_partial_when_one_specialist_failed(council_client, db_session, monkeypatch):
    monkeypatch.setattr(council_route, "AI_COUNCIL_ENABLED", True)
    speaker = _speaker(db_session, "council-partial-api")
    contribution = _contribution(db_session, speaker)
    event = _event(db_session, contribution)
    run_council_event(
        db_session, event,
        [DataStewardRulesV1(), ExplodingSpecialist(), LanguageScoutRulesV1(), ExplainerRulesV1()],
        NOW,
    )

    body = _status(council_client, speaker, contribution)

    assert body["state"] == "PARTIAL"
    failed = [row for row in body["outputs"] if row["state"] == "FAILED"]
    assert [row["specialist"] for row in failed] == ["SOUND_SENTINEL"]
    assert failed[0]["failure_reason"] == "model unavailable"


def test_status_is_failed_once_the_event_is_exhausted(council_client, db_session, monkeypatch):
    monkeypatch.setattr(council_route, "AI_COUNCIL_ENABLED", True)
    speaker = _speaker(db_session, "council-exhausted-api")
    contribution = _contribution(db_session, speaker)
    event = _event(db_session, contribution)
    run_council_event(db_session, event, [cls() for cls in ALL_SPECIALISTS], NOW)

    event.last_error = COUNCIL_ATTEMPTS_EXHAUSTED
    db_session.commit()

    assert _status(council_client, speaker, contribution)["state"] == "FAILED"


def test_status_does_not_leak_another_speakers_council_output(council_client, db_session, monkeypatch):
    monkeypatch.setattr(council_route, "AI_COUNCIL_ENABLED", True)
    speaker = _speaker(db_session, "council-owner")
    stranger = _speaker(db_session, "council-stranger")
    db_session.commit()
    contribution = _contribution(db_session, speaker)
    event = _event(db_session, contribution)
    run_council_event(db_session, event, [cls() for cls in ALL_SPECIALISTS], NOW)

    assert _status(council_client, stranger, contribution) == {"state": "PENDING", "outputs": []}


def test_status_requires_a_matching_persisted_identity(council_client, db_session, monkeypatch):
    monkeypatch.setattr(council_route, "AI_COUNCIL_ENABLED", True)
    speaker = _speaker(db_session, "council-identity")
    contribution = _contribution(db_session, speaker)
    db_session.commit()

    impostor = User(id=speaker.id, provider_subject="not-the-real-subject", declared_languages=["tn"])
    with _client_for(db_session, impostor) as client:
        response = client.get(f"/contributions/{contribution.id}/council")
    assert response.status_code == 401


# --- Worker: recovery, exhaustion, and the peer-truth guarantee ---------------


def test_worker_completes_a_claimed_event_and_writes_council_outputs(db_session):
    speaker = _speaker(db_session, "worker-happy")
    contribution = _contribution(db_session, speaker)
    event = _event(db_session, contribution)

    assert process_once(db_session, worker_id="w", batch_size=10, now=NOW) == 1

    db_session.refresh(event)
    assert event.completed_at == NOW
    assert event.claimed_by is None
    assert db_session.query(CouncilOutput).filter_by(event_id=event.id).count() == 4
    assert process_once(db_session, worker_id="w", batch_size=10, now=NOW + timedelta(hours=1)) == 0


def test_worker_retries_a_failing_event_with_backoff_then_exhausts_it(db_session):
    """AI_COUNCIL_MAX_ATTEMPTS was dead config before this: a permanently
    failing event was retried forever and the API's FAILED state was
    unreachable because nothing ever wrote COUNCIL_ATTEMPTS_EXHAUSTED."""
    speaker = _speaker(db_session, "worker-exhaust")
    contribution = _contribution(db_session, speaker)
    event = _event(db_session, contribution)

    def boom(session, ev, specialists, now):
        raise RuntimeError("council backend down")

    now = NOW
    for attempt in range(1, 4):
        assert process_once(db_session, worker_id="w", batch_size=10, now=now,
                            max_attempts=3, runner=boom) == 1
        db_session.refresh(event)
        assert event.attempt_count == attempt
        if attempt < 3:
            assert event.completed_at is None
            assert event.last_error == "council backend down"
            assert event.available_at == now + timedelta(seconds=min(2 ** attempt, 300))
            now = event.available_at
        else:
            assert event.completed_at == now, "the third attempt hits the budget and terminates"
            assert event.last_error == COUNCIL_ATTEMPTS_EXHAUSTED

    assert process_once(db_session, worker_id="w", batch_size=10, now=now + timedelta(days=1),
                        max_attempts=3, runner=boom) == 0, "an exhausted event is not retried forever"


def test_worker_crash_before_completion_is_recovered_by_lease_expiry(db_session):
    speaker = _speaker(db_session, "worker-crash")
    contribution = _contribution(db_session, speaker)
    event = _event(db_session, contribution)

    # Worker A claims and then "crashes" -- never completes, never retries.
    claimed = claim_events(db_session, worker_id="worker-a", now=NOW, limit=10)
    assert [row.id for row in claimed] == [event.id]

    # Worker B picks it up only after the lease expires, and finishes it once.
    assert process_once(db_session, worker_id="worker-b", batch_size=10,
                        now=NOW + timedelta(seconds=30)) == 0
    assert process_once(db_session, worker_id="worker-b", batch_size=10,
                        now=NOW + timedelta(seconds=120)) == 1

    db_session.refresh(event)
    assert event.completed_at == NOW + timedelta(seconds=120)
    assert db_session.query(CouncilOutput).filter_by(event_id=event.id).count() == 4, (
        "recovery must not duplicate Council output rows"
    )


def test_worker_failure_preserves_peer_truth_and_reward_state(db_session):
    speaker = _speaker(db_session, "worker-peer-truth")
    contribution = _contribution(db_session, speaker)
    event = _event(db_session, contribution)
    before_state = contribution.state
    before_rewards = db_session.query(RewardEvent).count()

    def boom(session, ev, specialists, now):
        raise RuntimeError("down")

    process_once(db_session, worker_id="w", batch_size=10, now=NOW, max_attempts=1, runner=boom)

    db_session.refresh(event)
    db_session.refresh(contribution)
    assert event.last_error == COUNCIL_ATTEMPTS_EXHAUSTED
    assert contribution.state == before_state, "an exhausted Council must not change the peer decision"
    assert db_session.query(RewardEvent).count() == before_rewards


def test_run_council_event_defaults_missing_payload_fields_conservatively(db_session):
    """A payload written by an older resolver version must not be read as
    consented or quality-passed by omission."""
    speaker = _speaker(db_session, "council-defaults")
    contribution = _contribution(db_session, speaker)
    event = OutboxEvent(event_type="ContributionResolved", aggregate_type="Contribution",
                        aggregate_id=contribution.id, dedupe_key=f"legacy:{contribution.id}",
                        payload_json={"contribution_id": str(contribution.id)},
                        occurred_at=NOW, available_at=NOW)
    db_session.add(event)
    db_session.commit()

    outputs = run_council_event(db_session, event, [DataStewardRulesV1(), SoundSentinelRulesV1()], NOW)
    codes = {row.specialist: row.output_json["code"] for row in outputs}

    assert codes["DATA_STEWARD"] == "BLOCKED_CONSENT"
    assert codes["SOUND_SENTINEL"] == "RE_RECORD_RISK"


def test_specialist_result_confidence_is_persisted_when_supplied(db_session):
    class ConfidentSpecialist:
        name = "LANGUAGE_SCOUT"
        version = "rules-1"

        def run(self, facts):
            return SpecialistResult("LANGUAGE_REVIEW", {"language": facts.language}, confidence=0.25)

    speaker = _speaker(db_session, "council-confidence")
    contribution = _contribution(db_session, speaker)
    event = _event(db_session, contribution)

    outputs = run_council_event(db_session, event, [ConfidentSpecialist()], NOW)
    assert outputs[0].confidence == pytest.approx(0.25)


def test_council_module_exposes_the_four_governed_specialists():
    names = [cls.name for cls in ALL_SPECIALISTS]
    assert names == ["DATA_STEWARD", "SOUND_SENTINEL", "LANGUAGE_SCOUT", "EXPLAINER"]
    assert all(cls.version == "rules-1" for cls in ALL_SPECIALISTS)
    assert council_module.canonical_sha256({}) == canonical_sha256({})


def test_worker_main_is_a_no_op_when_the_council_is_disabled(monkeypatch):
    """AI-disabled isolation, checklist item 4: with the flag off the worker
    entrypoint must exit cleanly *without* requiring a database URL or
    opening an engine at all. Guarding this matters because the disabled
    check sits before the AMAZWI_DATABASE_URL lookup -- reordering those
    two lines would make a disabled deployment crash on startup instead of
    quietly doing nothing, and nothing else in the suite would notice.
    """
    import scripts.run_council_worker as worker

    monkeypatch.setattr(worker, "AI_COUNCIL_ENABLED", False)
    monkeypatch.delenv("AMAZWI_DATABASE_URL", raising=False)

    def _fail(*args, **kwargs):  # pragma: no cover - must never be reached
        raise AssertionError("disabled mode must not create a database engine")

    monkeypatch.setattr(worker, "create_engine", _fail)
    monkeypatch.setattr("sys.argv", ["run_council_worker.py", "--once"])

    assert worker.main() == 0
