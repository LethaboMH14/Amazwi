"""Mission proposal + human-only authorisation tests (Plan 03, Task 9).

The single most important test in this file is
`test_automated_actor_cannot_authorise_without_the_human_step`: it is the
one that tries to authorise a real mission with no human involved and
asserts the attempt is refused and leaves no trace.
"""
from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pytest
from sqlalchemy import func, select

from app.missions import (
    CONFIRMATION_TEXT,
    IdempotencyConflict,
    MissionAlreadyDecided,
    MissionRejected,
    OperatorAuthorisationRequired,
    authorise_mission,
    principal_for_user,
    propose_mission,
)
from app.models import (
    AuditEvent,
    Campaign,
    CouncilOutput,
    CouncilOutputState,
    MissionAuthorisation,
    MissionProposal,
    MissionProposalState,
    OutboxEvent,
    User,
)

NOW = datetime(2026, 9, 2, 10, 0, tzinfo=timezone.utc)
APP_ROOT = Path(__file__).resolve().parents[1] / "app"


def _user(session, subject, *, kind="HUMAN", roles=(), name=None):
    user = User(
        provider_subject=subject,
        declared_languages=["zu"],
        principal_kind=kind,
        roles=list(roles),
        display_name=name,
    )
    session.add(user)
    session.flush()
    return user


def _advisory_output(session):
    event = OutboxEvent(
        event_type="ContributionResolved",
        aggregate_type="contribution",
        aggregate_id=uuid.uuid4(),
        dedupe_key=str(uuid.uuid4()),
        payload_json={},
    )
    session.add(event)
    session.flush()
    output = CouncilOutput(
        event_id=event.id,
        specialist="LANGUAGE_SCOUT",
        model_version="v1",
        state=CouncilOutputState.SUCCEEDED,
        input_sha256="a" * 64,
        output_json={"gap": "support"},
    )
    session.add(output)
    session.flush()
    return output


@pytest.fixture()
def proposal(db_session):
    output = _advisory_output(db_session)
    record = propose_mission(
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
    # Committed so the gate tests can roll back and prove that a refused
    # authorisation left nothing behind, without also discarding the proposal.
    db_session.expire_on_commit = False
    db_session.commit()
    return record


@pytest.fixture()
def mtn_operator(db_session):
    return principal_for_user(
        _user(
            db_session,
            "ops-human",
            kind="HUMAN",
            roles=["MTN_LANGUAGE_OPS"],
            name="Thandi (MTN Language Ops)",
        )
    )


@pytest.fixture()
def advisory_actor(db_session):
    """An automated advisory worker. Deliberately given the operator role to
    prove the role alone is not enough -- being a machine is disqualifying."""
    return principal_for_user(
        _user(
            db_session,
            "advisory-worker",
            kind="AUTOMATED",
            roles=["MTN_LANGUAGE_OPS"],
        )
    )


# --- the human gate ------------------------------------------------------


def test_automated_actor_cannot_authorise_without_the_human_step(
    db_session, proposal, advisory_actor
):
    """THE gate test: no human, no authorisation, no side effects.

    The automated actor here holds the MTN_LANGUAGE_OPS role and supplies
    the correct confirmation text -- everything an automated caller could
    possibly supply. It is still refused, because `principal_kind` is a
    persisted database fact it cannot assert its way out of.
    """
    with pytest.raises(OperatorAuthorisationRequired):
        authorise_mission(
            db_session,
            proposal.id,
            advisory_actor,
            "key-1",
            NOW,
            confirmation_text=CONFIRMATION_TEXT,
        )

    db_session.rollback()
    assert db_session.scalar(select(func.count(MissionAuthorisation.id))) == 0
    assert (
        db_session.get(MissionProposal, proposal.id).state
        is MissionProposalState.PROPOSED
    )
    assert (
        db_session.scalar(
            select(func.count(AuditEvent.id)).where(
                AuditEvent.action == "MISSION_AUTHORISED"
            )
        )
        == 0
    )


def test_human_without_the_operator_role_cannot_authorise(db_session, proposal):
    ordinary = principal_for_user(_user(db_session, "speaker-1", kind="HUMAN"))
    with pytest.raises(OperatorAuthorisationRequired):
        authorise_mission(
            db_session,
            proposal.id,
            ordinary,
            "key-1",
            NOW,
            confirmation_text=CONFIRMATION_TEXT,
        )
    db_session.rollback()
    assert db_session.scalar(select(func.count(MissionAuthorisation.id))) == 0


def test_operator_without_explicit_confirmation_cannot_authorise(
    db_session, proposal, mtn_operator
):
    """A correct human operator who did not confirm is still refused."""
    for wrong in ("", "yes", CONFIRMATION_TEXT.lower(), CONFIRMATION_TEXT + " "):
        with pytest.raises(OperatorAuthorisationRequired):
            authorise_mission(
                db_session,
                proposal.id,
                mtn_operator,
                "key-1",
                NOW,
                confirmation_text=wrong,
            )
        db_session.rollback()
    assert db_session.scalar(select(func.count(MissionAuthorisation.id))) == 0


def test_no_module_outside_the_ops_route_can_call_authorise_mission():
    """Structural proof that no automated process has an authorisation path.

    If a future worker, scheduler or outbox consumer imports
    `authorise_mission`, this test fails and forces the change to be made
    deliberately and reviewed.
    """
    callers = []
    for path in APP_ROOT.rglob("*.py"):
        if path.name == "missions.py":
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"\bauthorise_mission\b", text):
            callers.append(path.relative_to(APP_ROOT).as_posix())
    assert callers == ["routes/ops.py"], callers


# --- authorisation behaviour --------------------------------------------


def test_human_operator_authorisation_is_idempotent_and_preserves_terms(
    db_session, proposal, mtn_operator
):
    original_reward = proposal.fixed_reward_cents
    original_budget = proposal.budget_cents
    first = authorise_mission(
        db_session, proposal.id, mtn_operator, "key-1", NOW,
        confirmation_text=CONFIRMATION_TEXT,
    )
    second = authorise_mission(
        db_session, proposal.id, mtn_operator, "key-1", NOW,
        confirmation_text=CONFIRMATION_TEXT,
    )
    assert first.id == second.id
    assert first.state is MissionProposalState.AUTHORISED
    assert first.fixed_reward_cents == original_reward
    assert first.budget_cents == original_budget
    assert db_session.scalar(select(func.count(MissionAuthorisation.id))) == 1


def test_different_idempotency_key_cannot_reauthorise(
    db_session, proposal, mtn_operator
):
    authorise_mission(
        db_session, proposal.id, mtn_operator, "key-1", NOW,
        confirmation_text=CONFIRMATION_TEXT,
    )
    with pytest.raises(MissionAlreadyDecided):
        authorise_mission(
            db_session, proposal.id, mtn_operator, "key-2", NOW,
            confirmation_text=CONFIRMATION_TEXT,
        )


def test_reused_key_on_another_mission_is_an_idempotency_conflict(
    db_session, proposal, mtn_operator
):
    other = propose_mission(
        db_session,
        advisory_output_id=_advisory_output(db_session).id,
        language="zu",
        province_code="KZN",
        domain="banking",
        rationale="isiZulu banking terms are unrepresented.",
        target_verified_clips=10,
        fixed_reward_cents=250,
        budget_cents=2_500,
    )
    authorise_mission(
        db_session, proposal.id, mtn_operator, "key-1", NOW,
        confirmation_text=CONFIRMATION_TEXT,
    )
    with pytest.raises(IdempotencyConflict):
        authorise_mission(
            db_session, other.id, mtn_operator, "key-1", NOW,
            confirmation_text=CONFIRMATION_TEXT,
        )


def test_authorisation_writes_an_audit_event_and_moves_no_money(
    db_session, proposal, mtn_operator
):
    campaign = Campaign(
        name="Setswana support", language="tn", budget_cents=100_000,
        funded_cents=100_000, committed_cents=0,
    )
    db_session.add(campaign)
    db_session.flush()

    authorise_mission(
        db_session, proposal.id, mtn_operator, "key-1", NOW,
        confirmation_text=CONFIRMATION_TEXT,
    )
    event = db_session.scalar(
        select(AuditEvent).where(AuditEvent.action == "MISSION_AUTHORISED")
    )
    assert event is not None
    assert event.actor_id == mtn_operator.user_id
    assert event.entity_id == str(proposal.id)
    assert CONFIRMATION_TEXT in event.event_metadata

    db_session.refresh(campaign)
    assert campaign.committed_cents == 0
    assert campaign.funded_cents == 100_000


def test_authorisation_record_stores_what_the_operator_confirmed(
    db_session, proposal, mtn_operator
):
    authorise_mission(
        db_session, proposal.id, mtn_operator, "key-1", NOW,
        confirmation_text=CONFIRMATION_TEXT,
    )
    record = db_session.scalar(select(MissionAuthorisation))
    assert record.confirmation_text == CONFIRMATION_TEXT
    assert record.operator_id == mtn_operator.user_id
    assert record.authorised_at == NOW


# --- proposal validation -------------------------------------------------


def test_proposal_budget_must_cover_the_target(db_session):
    output = _advisory_output(db_session)
    with pytest.raises(MissionRejected):
        propose_mission(
            db_session,
            advisory_output_id=output.id,
            language="tn",
            province_code="NW",
            domain="support",
            rationale="under-budgeted",
            target_verified_clips=100,
            fixed_reward_cents=250,
            budget_cents=24_999,
        )


@pytest.mark.parametrize(
    "field,value",
    [("language", "xx"), ("province_code", "ZZ"), ("domain", "gambling")],
)
def test_proposal_rejects_values_outside_the_approved_vocabularies(
    db_session, field, value
):
    output = _advisory_output(db_session)
    kwargs = dict(
        advisory_output_id=output.id,
        language="tn",
        province_code="NW",
        domain="support",
        rationale="vocab check",
        target_verified_clips=10,
        fixed_reward_cents=250,
        budget_cents=2_500,
    )
    kwargs[field] = value
    with pytest.raises(MissionRejected):
        propose_mission(db_session, **kwargs)


def test_one_advisory_output_yields_at_most_one_proposal(db_session, proposal):
    with pytest.raises(MissionRejected):
        propose_mission(
            db_session,
            advisory_output_id=proposal.advisory_output_id,
            language="tn",
            province_code="NW",
            domain="support",
            rationale="duplicate",
            target_verified_clips=10,
            fixed_reward_cents=250,
            budget_cents=2_500,
        )
