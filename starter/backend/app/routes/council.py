from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
import uuid
from app.config import AI_COUNCIL_ENABLED
from app.db import get_session
from app.identity import (
    AuthenticatedIdentity,
    get_current_identity,
    require_identity_user,
)
from app.models import Contribution, CouncilOutput, CouncilOutputState, OutboxEvent

router = APIRouter(tags=["council"])
ORDER = {"DATA_STEWARD": 0, "SOUND_SENTINEL": 1, "LANGUAGE_SCOUT": 2, "EXPLAINER": 3}


@router.get("/contributions/{contribution_id}/council")
def council_status(
    contribution_id: uuid.UUID,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
):
    require_identity_user(session, identity)
    contribution = session.get(Contribution, contribution_id)
    if contribution is None or contribution.speaker_id != identity.user_id:
        return {"state": "PENDING", "outputs": []}
    if not AI_COUNCIL_ENABLED:
        return {"state": "DISABLED", "outputs": []}
    event = session.scalar(
        select(OutboxEvent)
        .where(
            OutboxEvent.aggregate_id == contribution_id,
            OutboxEvent.event_type == "ContributionResolved",
        )
        .order_by(OutboxEvent.occurred_at.desc())
    )
    if event is None:
        return {"state": "PENDING", "outputs": []}
    rows = session.scalars(
        select(CouncilOutput).where(CouncilOutput.event_id == event.id)
    ).all()
    outputs = [
        {
            "specialist": r.specialist,
            "model_version": r.model_version,
            "state": r.state.value,
            "confidence": r.confidence,
            "output": r.output_json,
            "failure_reason": r.failure_reason,
        }
        for r in sorted(rows, key=lambda r: ORDER.get(r.specialist, 99))
    ]
    states = {r.state for r in rows}
    state = (
        "READY"
        if rows and states == {CouncilOutputState.SUCCEEDED}
        else "PARTIAL"
        if rows
        else "PENDING"
    )
    if event.last_error == "COUNCIL_ATTEMPTS_EXHAUSTED":
        state = "FAILED"
    return {"state": state, "outputs": outputs}
