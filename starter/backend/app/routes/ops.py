"""MTN Language Ops API (Plan 03, Task 9).

CROSS-LANE, PENDING SBU'S REVIEW -- money/authorisation territory.

This is the ONLY module in the codebase that calls `authorise_mission`, and
`tests/test_missions.py` asserts that fact by scanning the source tree, so
no worker, scheduler or outbox consumer can acquire an authorisation path
without a test failing. The route is a POST that requires an authenticated
human principal, the `MTN_LANGUAGE_OPS` role, an `Idempotency-Key` header
and an exact confirmation echo in the body. There is no GET, no cron entry
point, and no default value for the confirmation.
"""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_session
from app.identity import (
    AuthenticatedIdentity,
    get_current_identity,
    require_identity_user,
)
from app.missions import (
    CONFIRMATION_TEXT,
    IdempotencyConflict,
    MissionAlreadyDecided,
    MissionRejected,
    OperatorAuthorisationRequired,
    authorise_mission,
    principal_for_user,
)
from app.models import (
    Contribution,
    ContributionState,
    MTN_LANGUAGE_OPS_ROLE,
    MissionAuthorisation,
    MissionProposal,
    MissionProposalState,
    User,
)

router = APIRouter(prefix="/ops", tags=["ops"])

#: Copy shown when a readiness field has no backing data source yet. Stated
#: as an absence, never as a number -- `content/error_states.json`'s tone
#: rule: do not promise what the system cannot do.
MODEL_EVIDENCE_UNAVAILABLE = "Model evidence unavailable"


class MissionAuthorisationRequest(BaseModel):
    """Empty of mission terms by design: language, domain, target, fixed
    reward and budget are read from the persisted proposal, never from the
    request. The only field is the operator's confirmation echo."""

    confirmation: str = Field(min_length=1, max_length=500)


def _readiness(session: Session) -> list[dict]:
    """Readiness rows built from real rows in this database.

    `Peer coverage` is a real count. `Model evidence` has no backing data
    source in this repo yet (no evaluation-run table exists), so it is
    returned as an explicit unavailable marker rather than a fabricated
    number, and the UI labels it as such.
    """
    verified = session.scalar(
        select(func.count(Contribution.id)).where(
            Contribution.state == ContributionState.UNDERSTOOD
        )
    )
    languages_active = session.scalar(
        select(func.count(func.distinct(Contribution.declared_language))).where(
            Contribution.state == ContributionState.UNDERSTOOD
        )
    )
    return [
        {
            "label": "Peer coverage",
            "value": str(verified or 0),
            "detail": f"{verified or 0} peer-verified contributions across "
            f"{languages_active or 0} languages",
            "available": True,
        },
        {
            "label": "Model evidence",
            "value": None,
            "detail": (
                "No evaluation run is recorded in this environment, so no "
                "model score is shown."
            ),
            "available": False,
        },
        {
            "label": "Evidence label",
            "value": "Peer truth is authoritative",
            "detail": "Advisory AI output never overrides a peer decision.",
            "available": True,
        },
    ]


def _gaps(session: Session) -> list[dict]:
    rows = session.execute(
        select(
            Contribution.declared_language,
            func.count(Contribution.id),
        )
        .where(Contribution.state == ContributionState.UNDERSTOOD)
        .group_by(Contribution.declared_language)
        .order_by(Contribution.declared_language)
    ).all()
    return [
        {"language": language, "verified_contributions": count}
        for language, count in rows
    ]


def _proposal_dto(session: Session, proposal: MissionProposal) -> dict:
    authorisation = session.scalar(
        select(MissionAuthorisation).where(
            MissionAuthorisation.proposal_id == proposal.id
        )
    )
    authorised_by = None
    if authorisation is not None:
        operator = session.get(User, authorisation.operator_id)
        if operator is not None:
            authorised_by = operator.display_name or operator.provider_subject
    return {
        "id": str(proposal.id),
        "language": proposal.language,
        "province_code": proposal.province_code,
        "domain": proposal.domain,
        "rationale": proposal.rationale,
        "target_verified_clips": proposal.target_verified_clips,
        "fixed_reward_cents": proposal.fixed_reward_cents,
        "budget_cents": proposal.budget_cents,
        "state": proposal.state.value,
        "authorised_by": authorised_by,
    }


@router.get("")
def get_ops(
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
):
    user = require_identity_user(session, identity)
    principal = principal_for_user(user)
    if not principal.is_human_mtn_operator:
        # No proposals, no terms, no controls for a non-operator.
        return {
            "principal_kind": principal.kind,
            "roles": [],
            "display_name": principal.display_name,
            "confirmation_text": CONFIRMATION_TEXT,
            "readiness": [],
            "gaps": [],
            "proposals": [],
        }
    proposals = session.scalars(
        select(MissionProposal).order_by(
            MissionProposal.created_at, MissionProposal.id
        )
    ).all()
    return {
        "principal_kind": principal.kind,
        "roles": list(principal.roles),
        "display_name": principal.display_name,
        "confirmation_text": CONFIRMATION_TEXT,
        "readiness": _readiness(session),
        "gaps": _gaps(session),
        "proposals": [_proposal_dto(session, p) for p in proposals],
    }


@router.post("/missions/{proposal_id}/authorise")
def authorise(
    proposal_id: UUID,
    body: MissionAuthorisationRequest,
    idempotency_key: str = Header(alias="Idempotency-Key"),
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
):
    user = require_identity_user(session, identity)
    principal = principal_for_user(user)
    try:
        proposal = authorise_mission(
            session,
            proposal_id,
            principal,
            idempotency_key,
            confirmation_text=body.confirmation,
        )
        session.commit()
    except OperatorAuthorisationRequired as exc:
        session.rollback()
        raise HTTPException(
            status_code=403,
            detail={"code": exc.code, "message": str(exc)},
        ) from exc
    except (MissionAlreadyDecided, IdempotencyConflict) as exc:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail={"code": exc.code, "message": str(exc)},
        ) from exc
    except MissionRejected as exc:
        session.rollback()
        raise HTTPException(
            status_code=422,
            detail={"code": exc.code, "message": str(exc)},
        ) from exc
    session.refresh(proposal)
    assert proposal.state is MissionProposalState.AUTHORISED
    return _proposal_dto(session, proposal)


__all__ = ["router", "MTN_LANGUAGE_OPS_ROLE", "MODEL_EVIDENCE_UNAVAILABLE"]
