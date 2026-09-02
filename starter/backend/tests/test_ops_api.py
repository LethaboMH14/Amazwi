"""MTN Language Ops API tests (Plan 03, Task 9).

Proves the human gate holds at the HTTP boundary too, not only in the
service layer: an automated principal is refused 403 even with a perfect
request body, and a request that omits the confirmation echo is refused
before anything is written.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select

from app.db import get_session
from app.identity import AuthenticatedIdentity, get_current_identity
from app.main import app
from app.missions import CONFIRMATION_TEXT, propose_mission
from app.models import (
    Contribution,
    ContributionState,
    CouncilOutput,
    CouncilOutputState,
    Campaign,
    Card,
    MissionAuthorisation,
    MissionProposal,
    MissionProposalState,
    OutboxEvent,
    User,
)


def _make_user(db_session, subject, kind, roles, name=None):
    user = User(
        id=uuid.uuid4(),
        provider_subject=subject,
        declared_languages=["tn"],
        principal_kind=kind,
        roles=list(roles),
        display_name=name,
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture
def actors(db_session):
    operator = _make_user(
        db_session, "ops-human", "HUMAN", ["MTN_LANGUAGE_OPS"], "Thandi Nkosi"
    )
    outsider = _make_user(db_session, "speaker", "HUMAN", [])
    robot = _make_user(
        db_session, "scheduler", "AUTOMATED", ["MTN_LANGUAGE_OPS"], "nightly-job"
    )
    db_session.expire_on_commit = False
    db_session.commit()
    return {"operator": operator, "outsider": outsider, "robot": robot}


@pytest.fixture
def seeded_proposal(db_session, actors):
    event = OutboxEvent(
        event_type="ContributionResolved",
        aggregate_type="contribution",
        aggregate_id=uuid.uuid4(),
        dedupe_key=str(uuid.uuid4()),
        payload_json={},
    )
    db_session.add(event)
    db_session.flush()
    output = CouncilOutput(
        event_id=event.id,
        specialist="LANGUAGE_SCOUT",
        model_version="v1",
        state=CouncilOutputState.SUCCEEDED,
        input_sha256="b" * 64,
    )
    db_session.add(output)
    db_session.flush()
    proposal = propose_mission(
        db_session,
        advisory_output_id=output.id,
        language="tn",
        province_code="NW",
        domain="support",
        rationale="Setswana support coverage is the largest verified gap.",
        target_verified_clips=100,
        fixed_reward_cents=250,
        budget_cents=25_000,
    )
    db_session.commit()
    return proposal


def _client(db_session, user):
    def override_session():
        yield db_session

    app.dependency_overrides[get_session] = override_session
    app.dependency_overrides[get_current_identity] = lambda: AuthenticatedIdentity(
        user_id=user.id, provider_subject=user.provider_subject
    )
    return TestClient(app)


@pytest.fixture(autouse=True)
def _clear_overrides():
    yield
    app.dependency_overrides.clear()


# --- GET /ops ------------------------------------------------------------


def test_ops_view_exposes_persisted_terms_to_an_operator(
    db_session, actors, seeded_proposal
):
    with _client(db_session, actors["operator"]) as client:
        body = client.get("/ops").json()
    assert body["roles"] == ["MTN_LANGUAGE_OPS"]
    assert body["confirmation_text"] == CONFIRMATION_TEXT
    proposal = body["proposals"][0]
    assert proposal["fixed_reward_cents"] == 250
    assert proposal["budget_cents"] == 25_000
    assert proposal["state"] == "PROPOSED"


def test_ops_view_hides_everything_from_a_non_operator(
    db_session, actors, seeded_proposal
):
    with _client(db_session, actors["outsider"]) as client:
        body = client.get("/ops").json()
    assert body["roles"] == []
    assert body["proposals"] == []
    assert body["readiness"] == []


def test_model_evidence_is_reported_unavailable_not_invented(
    db_session, actors, seeded_proposal
):
    with _client(db_session, actors["operator"]) as client:
        rows = client.get("/ops").json()["readiness"]
    model_row = next(r for r in rows if r["label"] == "Model evidence")
    assert model_row["available"] is False
    assert model_row["value"] is None


def test_peer_coverage_counts_real_rows(db_session, actors, seeded_proposal):
    campaign = Campaign(
        name="c", language="tn", budget_cents=1, funded_cents=1, committed_cents=0
    )
    db_session.add(campaign)
    db_session.flush()
    card = Card(
        language="tn",
        target="metsi",
        blocked_words=["a", "b", "c", "d"],
        accepted_answers=["metsi", "water"],
        distractors=["x", "y", "z"],
        campaign_id=campaign.id,
    )
    db_session.add(card)
    db_session.flush()
    db_session.add(
        Contribution(
            speaker_id=actors["outsider"].id,
            card_id=card.id,
            declared_language="tn",
            state=ContributionState.UNDERSTOOD,
        )
    )
    db_session.commit()

    with _client(db_session, actors["operator"]) as client:
        body = client.get("/ops").json()
    coverage = next(r for r in body["readiness"] if r["label"] == "Peer coverage")
    assert coverage["value"] == "1"
    assert body["gaps"] == [{"language": "tn", "verified_contributions": 1}]


# --- POST /ops/missions/{id}/authorise -----------------------------------


def test_automated_principal_is_refused_at_the_http_boundary(
    db_session, actors, seeded_proposal
):
    """The scheduler sends a byte-perfect request and is still refused."""
    with _client(db_session, actors["robot"]) as client:
        response = client.post(
            f"/ops/missions/{seeded_proposal.id}/authorise",
            headers={"Idempotency-Key": "ops-robot-1"},
            json={"confirmation": CONFIRMATION_TEXT},
        )
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "OPERATOR_ROLE_REQUIRED"
    assert db_session.scalar(select(func.count(MissionAuthorisation.id))) == 0
    assert (
        db_session.get(MissionProposal, seeded_proposal.id).state
        is MissionProposalState.PROPOSED
    )


def test_non_operator_human_is_refused(db_session, actors, seeded_proposal):
    with _client(db_session, actors["outsider"]) as client:
        response = client.post(
            f"/ops/missions/{seeded_proposal.id}/authorise",
            headers={"Idempotency-Key": "ops-outsider-1"},
            json={"confirmation": CONFIRMATION_TEXT},
        )
    assert response.status_code == 403
    assert db_session.scalar(select(func.count(MissionAuthorisation.id))) == 0


def test_missing_confirmation_is_refused(db_session, actors, seeded_proposal):
    with _client(db_session, actors["operator"]) as client:
        response = client.post(
            f"/ops/missions/{seeded_proposal.id}/authorise",
            headers={"Idempotency-Key": "ops-1"},
            json={},
        )
    assert response.status_code == 422
    assert db_session.scalar(select(func.count(MissionAuthorisation.id))) == 0


def test_wrong_confirmation_text_is_refused(db_session, actors, seeded_proposal):
    with _client(db_session, actors["operator"]) as client:
        response = client.post(
            f"/ops/missions/{seeded_proposal.id}/authorise",
            headers={"Idempotency-Key": "ops-1"},
            json={"confirmation": "ok"},
        )
    assert response.status_code == 403
    assert db_session.scalar(select(func.count(MissionAuthorisation.id))) == 0


def test_missing_idempotency_key_is_refused(db_session, actors, seeded_proposal):
    with _client(db_session, actors["operator"]) as client:
        response = client.post(
            f"/ops/missions/{seeded_proposal.id}/authorise",
            json={"confirmation": CONFIRMATION_TEXT},
        )
    assert response.status_code == 422
    assert db_session.scalar(select(func.count(MissionAuthorisation.id))) == 0


def test_human_operator_authorises_and_replays_safely(
    db_session, actors, seeded_proposal
):
    with _client(db_session, actors["operator"]) as client:
        first = client.post(
            f"/ops/missions/{seeded_proposal.id}/authorise",
            headers={"Idempotency-Key": "ops-1"},
            json={"confirmation": CONFIRMATION_TEXT},
        )
        second = client.post(
            f"/ops/missions/{seeded_proposal.id}/authorise",
            headers={"Idempotency-Key": "ops-1"},
            json={"confirmation": CONFIRMATION_TEXT},
        )
        third = client.post(
            f"/ops/missions/{seeded_proposal.id}/authorise",
            headers={"Idempotency-Key": "ops-2"},
            json={"confirmation": CONFIRMATION_TEXT},
        )
    assert first.status_code == 200
    assert first.json()["state"] == "AUTHORISED"
    assert first.json()["authorised_by"] == "Thandi Nkosi"
    assert first.json()["fixed_reward_cents"] == 250
    assert second.status_code == 200
    assert third.status_code == 409
    assert third.json()["detail"]["code"] == "MISSION_ALREADY_DECIDED"
    assert db_session.scalar(select(func.count(MissionAuthorisation.id))) == 1


def test_authorise_route_accepts_no_mission_terms_from_the_request(
    db_session, actors, seeded_proposal
):
    """Sending mutated terms must not change what is authorised."""
    with _client(db_session, actors["operator"]) as client:
        response = client.post(
            f"/ops/missions/{seeded_proposal.id}/authorise",
            headers={"Idempotency-Key": "ops-1"},
            json={
                "confirmation": CONFIRMATION_TEXT,
                "fixed_reward_cents": 999_999,
                "budget_cents": 999_999_999,
            },
        )
    assert response.status_code == 200
    assert response.json()["fixed_reward_cents"] == 250
    assert response.json()["budget_cents"] == 25_000
