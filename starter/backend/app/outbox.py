"""Small transactional-outbox helpers; worker leasing is deliberately separate."""
from datetime import datetime, timezone
import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import OutboxEvent

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
