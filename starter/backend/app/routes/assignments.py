from __future__ import annotations

import random
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api_types import AssignmentAnswerRequest, AssignmentResponse, ContributionResult
from app.cohorts import select_next_verifier
from app.db import get_session
from app.identity import AuthenticatedIdentity, get_current_identity
from app.matching import is_correct, normalise_answer
from app.models import Assignment, AssignmentMode, Card, Contribution, EligibilityDecision
from app.resolver import ResolutionNotReadyError, create_assignment, resolve_from_persisted_state


router = APIRouter(tags=["assignments"])


def _assignment_response(assignment: Assignment) -> AssignmentResponse:
    return AssignmentResponse(
        id=str(assignment.id),
        contribution_id=str(assignment.contribution_id),
        mode=assignment.mode.value,
    )


@router.get("/assignments/next", response_model=AssignmentResponse)
def next_assignment(
    contribution_id: uuid.UUID,
    language: str,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
) -> AssignmentResponse:
    verifier = select_next_verifier(session, contribution_id, language, random.SystemRandom(), identity.user_id)
    if verifier is None:
        raise HTTPException(status_code=404, detail={"code": "NO_ASSIGNMENT"})
    try:
        assignment = create_assignment(
            session,
            contribution_id=contribution_id,
            verifier_id=identity.user_id,
            mode=AssignmentMode.PROFICIENT_VERIFIER,
        )
    except Exception as exc:
        raise HTTPException(status_code=409, detail={"code": "NO_ASSIGNMENT"}) from exc
    return _assignment_response(assignment)


@router.post("/assignments/{assignment_id}/answer", response_model=AssignmentResponse)
def answer_assignment(
    assignment_id: uuid.UUID,
    request: AssignmentAnswerRequest,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
) -> AssignmentResponse:
    assignment = session.get(Assignment, assignment_id)
    if assignment is None or assignment.verifier_id != identity.user_id:
        raise HTTPException(status_code=403, detail={"code": "ASSIGNMENT_NOT_AUTHORISED"})
    if assignment.answered_at is not None:
        raise HTTPException(status_code=409, detail={"code": "ASSIGNMENT_ALREADY_ANSWERED"})
    contribution = session.get(Contribution, assignment.contribution_id)
    card = session.get(Card, contribution.card_id) if contribution else None
    if contribution is None or card is None:
        raise HTTPException(status_code=404, detail={"code": "NO_ASSIGNMENT"})
    assignment.answer_text = request.answer_text
    assignment.answer_normalised = normalise_answer(request.answer_text)
    assignment.matched = is_correct(request.answer_text, card.accepted_answers)
    assignment.violation_vote = request.violation_vote
    from datetime import datetime, timezone
    assignment.answered_at = datetime.now(timezone.utc)
    session.commit()
    try:
        resolve_from_persisted_state(session, assignment.contribution_id)
    except ResolutionNotReadyError:
        pass
    return _assignment_response(assignment)


@router.post("/assignments/{assignment_id}/referee", response_model=AssignmentResponse)
def referee_assignment(
    assignment_id: uuid.UUID,
    request: AssignmentAnswerRequest,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
) -> AssignmentResponse:
    return answer_assignment(assignment_id, request, identity, session)


@router.get("/contributions/{contribution_id}/result", response_model=ContributionResult)
def contribution_result(
    contribution_id: uuid.UUID,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
) -> ContributionResult:
    contribution = session.get(Contribution, contribution_id)
    if contribution is None or contribution.speaker_id != identity.user_id:
        raise HTTPException(status_code=403, detail={"code": "AUDIO_NOT_AUTHORISED"})
    decision = session.get(EligibilityDecision, contribution_id)
    if decision is None:
        return ContributionResult(status="PENDING")
    return ContributionResult(
        status="RESOLVED",
        understood=decision.understood,
        corpus_eligible=decision.corpus_eligible,
        reason=decision.reason,
    )
