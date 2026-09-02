"""Small transactional-outbox helpers; worker leasing is deliberately separate."""
from datetime import datetime, timezone, timedelta
import uuid
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from .models import OutboxEvent

# Terminal marker written when a Council event has burned its retry budget.
# app/routes/council.py reads this exact string to report a FAILED Council
# state, so the constant is shared rather than duplicated as a literal.
COUNCIL_ATTEMPTS_EXHAUSTED = "COUNCIL_ATTEMPTS_EXHAUSTED"

def enqueue_contribution_resolved(session: Session, contribution_id: uuid.UUID, decision_id: uuid.UUID) -> OutboxEvent:
    event = session.scalar(select(OutboxEvent).where(OutboxEvent.dedupe_key == f"contribution-resolved:{contribution_id}"))
    if event is not None:
        return event
    event = OutboxEvent(event_type="ContributionResolved", aggregate_type="Contribution", aggregate_id=contribution_id, dedupe_key=f"contribution-resolved:{contribution_id}", payload_json={"contribution_id": str(contribution_id), "decision_id": str(decision_id)})
    session.add(event)
    return event

def mark_completed(session: Session, event: OutboxEvent) -> None:
    event.completed_at = datetime.now(timezone.utc)
    event.claimed_at = None
    event.claimed_by = None

def claim_events(session: Session, *, worker_id: str, now: datetime, limit: int = 10, lease_seconds: int = 60) -> list[OutboxEvent]:
    stmt = (select(OutboxEvent).where(OutboxEvent.completed_at.is_(None), OutboxEvent.available_at <= now, or_(OutboxEvent.claimed_at.is_(None), OutboxEvent.claimed_at < now - timedelta(seconds=lease_seconds))).order_by(OutboxEvent.occurred_at, OutboxEvent.id).with_for_update(skip_locked=True).limit(limit))
    rows = list(session.scalars(stmt))
    for row in rows:
        row.claimed_at = now
        row.claimed_by = worker_id
        row.attempt_count += 1
    session.commit()
    return rows

def complete_event(session: Session, event_id: uuid.UUID, worker_id: str, now: datetime) -> None:
    event = session.scalar(select(OutboxEvent).where(OutboxEvent.id == event_id).with_for_update())
    if event is None or event.claimed_by != worker_id:
        raise ValueError("OUTBOX_WORKER_NOT_OWNER")
    event.completed_at = now
    event.claimed_at = None
    event.claimed_by = None
    session.commit()

def retry_event(session: Session, event_id: uuid.UUID, worker_id: str, now: datetime, error: str) -> datetime:
    event = session.scalar(select(OutboxEvent).where(OutboxEvent.id == event_id).with_for_update())
    if event is None or event.claimed_by != worker_id:
        raise ValueError("OUTBOX_WORKER_NOT_OWNER")
    delay = min(2 ** max(event.attempt_count, 0), 300)
    event.available_at = now + timedelta(seconds=delay)
    event.last_error = error[:2000]
    event.claimed_at = None
    event.claimed_by = None
    session.commit()
    return event.available_at

def exhaust_event(session: Session, event_id: uuid.UUID, worker_id: str, now: datetime) -> None:
    """Terminally give up on an event whose retry budget is spent.

    completed_at is set so claim_events stops handing the row out -- without
    this the worker retried a permanently failing event forever, and the
    FAILED Council state in app/routes/council.py was unreachable because
    nothing ever wrote COUNCIL_ATTEMPTS_EXHAUSTED.
    """
    event = session.scalar(select(OutboxEvent).where(OutboxEvent.id == event_id).with_for_update())
    if event is None or event.claimed_by != worker_id:
        raise ValueError("OUTBOX_WORKER_NOT_OWNER")
    event.last_error = COUNCIL_ATTEMPTS_EXHAUSTED
    event.completed_at = now
    event.claimed_at = None
    event.claimed_by = None
    session.commit()


def release_event_for_admin_retry(session: Session, event_id: uuid.UUID, actor_id: uuid.UUID, reason: str, now: datetime) -> None:
    event = session.scalar(select(OutboxEvent).where(OutboxEvent.id == event_id).with_for_update())
    if event is None:
        raise ValueError("OUTBOX_EVENT_NOT_FOUND")
    if event.completed_at is not None:
        # An exhausted event is the one completed state an admin may reopen.
        # Genuinely processed events stay closed so a mistyped id cannot
        # cause a second delivery.
        if event.last_error != COUNCIL_ATTEMPTS_EXHAUSTED:
            raise ValueError("OUTBOX_EVENT_ALREADY_COMPLETED")
        event.completed_at = None
        event.attempt_count = 0
    event.available_at = now
    event.claimed_at = None
    event.claimed_by = None
    event.last_error = reason[:2000]
    from .models import AuditEvent
    session.add(AuditEvent(actor_id=actor_id, action="OUTBOX_ADMIN_RETRY", entity_type="OutboxEvent", entity_id=str(event_id), event_metadata=reason[:2000]))
    session.commit()
