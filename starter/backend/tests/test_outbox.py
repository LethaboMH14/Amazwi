"""Outbox leasing, retry, exhaustion and audited recovery.

Written to close Final Acceptance Checklist item 2 of
docs/superpowers/plans/2026-09-01-amazwi-02-council-data-models.md
("PostgreSQL workers use FOR UPDATE SKIP LOCKED, leases, deterministic
retry delays, and audited recovery without duplicate claims"), which had
no test of its own -- test_council_data_e2e.py only proved one happy
claim and one retry.

These are real-PostgreSQL tests by necessity: SKIP LOCKED has no
meaningful behaviour to assert without two genuinely concurrent
transactions, so one of them is held open on a separate connection.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import uuid

import pytest
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.models import AuditEvent, OutboxEvent, User
from app.outbox import (
    COUNCIL_ATTEMPTS_EXHAUSTED,
    claim_events,
    complete_event,
    enqueue_contribution_resolved,
    exhaust_event,
    mark_completed,
    release_event_for_admin_retry,
    retry_event,
)

NOW = datetime(2026, 9, 2, 12, 0, 0, tzinfo=timezone.utc)


def _event(db_session, key: str, *, occurred_at: datetime) -> OutboxEvent:
    event = OutboxEvent(
        event_type="ContributionResolved",
        aggregate_type="Contribution",
        aggregate_id=uuid.uuid4(),
        dedupe_key=key,
        payload_json={"contribution_id": str(uuid.uuid4())},
        occurred_at=occurred_at,
        available_at=occurred_at,
    )
    db_session.add(event)
    db_session.commit()
    return event


def test_enqueue_is_idempotent_per_contribution(db_session):
    contribution_id = uuid.uuid4()
    first = enqueue_contribution_resolved(db_session, contribution_id, uuid.uuid4())
    db_session.commit()
    second = enqueue_contribution_resolved(db_session, contribution_id, uuid.uuid4())
    db_session.commit()

    assert first.id == second.id
    assert db_session.query(OutboxEvent).filter_by(aggregate_id=contribution_id).count() == 1


def test_skip_locked_never_hands_the_same_row_to_two_workers(db_session, db_engine):
    """A row locked by an open transaction must be skipped, not waited on."""
    first = _event(db_session, "skip-locked:1", occurred_at=NOW)
    second = _event(db_session, "skip-locked:2", occurred_at=NOW + timedelta(seconds=1))

    holder = db_engine.connect()
    try:
        holder.execute(text("BEGIN"))
        locked = holder.execute(
            text(
                "SELECT id FROM outbox_events WHERE completed_at IS NULL "
                "ORDER BY occurred_at, id FOR UPDATE SKIP LOCKED LIMIT 1"
            )
        ).scalar_one()
        assert locked == first.id, "ordering is occurred_at then id, so the older row is first"

        claimed = claim_events(db_session, worker_id="worker-b", now=NOW + timedelta(seconds=2), limit=10)

        assert [row.id for row in claimed] == [second.id]
        assert first.id not in {row.id for row in claimed}
        assert claimed[0].claimed_by == "worker-b"
        assert claimed[0].attempt_count == 1
    finally:
        holder.execute(text("ROLLBACK"))
        holder.close()


def test_an_unexpired_lease_is_not_reclaimed_but_an_expired_one_is(db_session):
    event = _event(db_session, "lease:1", occurred_at=NOW)

    first = claim_events(db_session, worker_id="worker-a", now=NOW, limit=10, lease_seconds=60)
    assert [row.id for row in first] == [event.id]

    within_lease = claim_events(
        db_session, worker_id="worker-b", now=NOW + timedelta(seconds=59), limit=10, lease_seconds=60
    )
    assert within_lease == []

    after_lease = claim_events(
        db_session, worker_id="worker-b", now=NOW + timedelta(seconds=61), limit=10, lease_seconds=60
    )
    assert [row.id for row in after_lease] == [event.id]
    assert after_lease[0].claimed_by == "worker-b"
    assert after_lease[0].attempt_count == 2, "a reclaim after lease expiry counts as a new attempt"


def test_retry_delay_is_a_deterministic_capped_power_of_two(db_session):
    event = _event(db_session, "retry:1", occurred_at=NOW)
    seen = []
    claim_at = NOW
    for attempt in range(1, 11):
        claimed = claim_events(db_session, worker_id="w", now=claim_at, limit=1)
        assert [row.id for row in claimed] == [event.id]
        assert claimed[0].attempt_count == attempt
        # retry always measured from the same instant so the assertion below
        # is about the delay function itself, not about wall-clock drift.
        available_at = retry_event(db_session, event.id, "w", NOW, "boom")
        seen.append(available_at - NOW)
        claim_at = available_at

    assert seen == [
        timedelta(seconds=min(2 ** attempt, 300)) for attempt in range(1, 11)
    ]
    assert seen[-1] == timedelta(seconds=300), "the backoff is capped, not unbounded"


def test_only_the_owning_worker_may_complete_retry_or_exhaust(db_session):
    event = _event(db_session, "owner:1", occurred_at=NOW)
    claim_events(db_session, worker_id="owner", now=NOW, limit=1)

    for call in (
        lambda: complete_event(db_session, event.id, "impostor", NOW),
        lambda: retry_event(db_session, event.id, "impostor", NOW, "x"),
        lambda: exhaust_event(db_session, event.id, "impostor", NOW),
    ):
        with pytest.raises(ValueError, match="OUTBOX_WORKER_NOT_OWNER"):
            call()

    db_session.rollback()
    db_session.refresh(event)
    assert event.completed_at is None
    assert event.claimed_by == "owner"


def test_completing_clears_the_lease_and_removes_the_row_from_claiming(db_session):
    event = _event(db_session, "complete:1", occurred_at=NOW)
    claim_events(db_session, worker_id="w", now=NOW, limit=1)
    complete_event(db_session, event.id, "w", NOW)

    db_session.refresh(event)
    assert event.completed_at == NOW
    assert event.claimed_at is None and event.claimed_by is None
    assert claim_events(db_session, worker_id="w2", now=NOW + timedelta(hours=1), limit=10) == []


def test_mark_completed_matches_complete_event_lease_clearing(db_session):
    event = _event(db_session, "mark:1", occurred_at=NOW)
    claim_events(db_session, worker_id="w", now=NOW, limit=1)
    mark_completed(db_session, event)
    db_session.commit()

    db_session.refresh(event)
    assert event.completed_at is not None
    assert event.claimed_at is None and event.claimed_by is None


def test_exhausted_event_is_terminal_and_stops_being_claimed(db_session):
    event = _event(db_session, "exhaust:1", occurred_at=NOW)
    claim_events(db_session, worker_id="w", now=NOW, limit=1)
    exhaust_event(db_session, event.id, "w", NOW)

    db_session.refresh(event)
    assert event.last_error == COUNCIL_ATTEMPTS_EXHAUSTED
    assert event.completed_at == NOW
    assert claim_events(db_session, worker_id="w", now=NOW + timedelta(days=1), limit=10) == []


def test_admin_recovery_reopens_an_exhausted_event_and_writes_an_audit_row(db_session):
    admin = User(id=uuid.uuid4(), provider_subject="outbox-admin", declared_languages=["zu"])
    db_session.add(admin)
    db_session.commit()

    event = _event(db_session, "recover:1", occurred_at=NOW)
    claim_events(db_session, worker_id="w", now=NOW, limit=1)
    exhaust_event(db_session, event.id, "w", NOW)

    release_event_for_admin_retry(db_session, event.id, admin.id, "manual review cleared", NOW)

    db_session.refresh(event)
    assert event.completed_at is None, "an exhausted event must be reopenable by an audited admin"
    assert event.attempt_count == 0, "the retry budget is reset so recovery is not instantly re-exhausted"
    assert event.claimed_at is None and event.claimed_by is None

    audit = db_session.scalars(
        select(AuditEvent).where(AuditEvent.entity_id == str(event.id))
    ).all()
    assert len(audit) == 1
    assert audit[0].action == "OUTBOX_ADMIN_RETRY"
    assert audit[0].actor_id == admin.id
    assert audit[0].event_metadata == "manual review cleared"

    reclaimed = claim_events(db_session, worker_id="w2", now=NOW, limit=10)
    assert [row.id for row in reclaimed] == [event.id]


def test_admin_recovery_refuses_to_resurrect_a_genuinely_completed_event(db_session):
    """A mistyped event id must not cause a second delivery of processed work."""
    admin = User(id=uuid.uuid4(), provider_subject="outbox-admin-2", declared_languages=["zu"])
    db_session.add(admin)
    db_session.commit()

    event = _event(db_session, "recover:2", occurred_at=NOW)
    claim_events(db_session, worker_id="w", now=NOW, limit=1)
    complete_event(db_session, event.id, "w", NOW)

    with pytest.raises(ValueError, match="OUTBOX_EVENT_ALREADY_COMPLETED"):
        release_event_for_admin_retry(db_session, event.id, admin.id, "oops", NOW)

    db_session.rollback()
    db_session.refresh(event)
    assert event.completed_at == NOW
    assert db_session.query(AuditEvent).count() == 0


def test_release_of_an_unknown_event_is_rejected(db_session):
    with pytest.raises(ValueError, match="OUTBOX_EVENT_NOT_FOUND"):
        release_event_for_admin_retry(db_session, uuid.uuid4(), uuid.uuid4(), "x", NOW)


def test_events_are_not_claimed_before_their_available_at(db_session):
    event = _event(db_session, "delayed:1", occurred_at=NOW)
    claim_events(db_session, worker_id="w", now=NOW, limit=1)
    available_at = retry_event(db_session, event.id, "w", NOW, "later")

    assert claim_events(db_session, worker_id="w", now=available_at - timedelta(seconds=1), limit=10) == []
    assert [row.id for row in claim_events(db_session, worker_id="w", now=available_at, limit=10)] == [event.id]


def test_claim_order_is_deterministic_across_repeat_runs(db_session):
    ids = []
    for index in range(5):
        ids.append(_event(db_session, f"order:{index}", occurred_at=NOW + timedelta(seconds=index)).id)

    first_pass = [row.id for row in claim_events(db_session, worker_id="w", now=NOW + timedelta(minutes=1), limit=10)]
    for event_id in first_pass:
        complete_event(db_session, event_id, "w", NOW + timedelta(minutes=1))

    assert first_pass == ids, "occurred_at then id, so replaying the same rows gives the same order"
