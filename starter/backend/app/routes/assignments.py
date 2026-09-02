from __future__ import annotations

import random
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api_types import AssignmentAnswerRequest, AssignmentResponse, ContributionResult
from app.cohorts import select_next_verifier
from app.db import get_session
from app.identity import AuthenticatedIdentity, get_current_identity, require_identity_user
from app.matching import is_correct, normalise_answer
from app.models import Assignment, AssignmentMode, Card, Contribution, EligibilityDecision, RewardEvent
from app.contributions import issue_verifier_playback_token
from app.audio import get_audio_store
from app.storage import LocalAudioObjectStore
from app.resolver import ResolutionNotReadyError, create_assignment, resolve_from_persisted_state


router = APIRouter(tags=["assignments"])


def _assignment_response(assignment: Assignment, language: str) -> AssignmentResponse:
    return AssignmentResponse(
        id=str(assignment.id),
        contribution_id=str(assignment.contribution_id),
        mode=assignment.mode.value,
        language=language,
        prompt_text="Listen once, then type the word you heard.",
    )


@router.get("/assignments/next", response_model=AssignmentResponse)
def next_assignment(
    contribution_id: uuid.UUID,
    language: str,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
) -> AssignmentResponse:
    require_identity_user(session, identity)

    # Resume an assignment this verifier already holds, rather than trying to
    # create a second one. Assignment has a UniqueConstraint on
    # (contribution_id, verifier_id), so the create path below raises for any
    # verifier who already has one -- which the route then reported as
    # NO_ASSIGNMENT, permanently locking that verifier out of their OWN
    # assignment.
    #
    # This is not a rare edge case: React StrictMode double-mounts effects in
    # development, so the verifier route fires this endpoint twice on a single
    # page load. The first call created the assignment, the second failed, and
    # the failure is the state the component kept -- a fresh verifier device
    # could land in a dead "NO_ASSIGNMENT" screen on its very first load.
    # Found by walking the verifier route in a real browser.
    #
    # "Next assignment for me" is idempotent by definition: asking twice must
    # return the same assignment, not an error.
    existing = session.scalar(
        select(Assignment).where(
            Assignment.contribution_id == contribution_id,
            Assignment.verifier_id == identity.user_id,
        )
    )
    if existing is not None:
        if existing.answered_at is not None:
            # They have already done their part. Distinct from "no assignment
            # available" so the UI can say something true.
            raise HTTPException(status_code=409, detail={"code": "ALREADY_ANSWERED"})
        return _assignment_response(existing, language)

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
        session.commit()
    except Exception as exc:
        raise HTTPException(status_code=409, detail={"code": "NO_ASSIGNMENT"}) from exc
    return _assignment_response(assignment, language)


@router.post("/assignments/{assignment_id}/playback")
def assignment_playback(
    assignment_id: uuid.UUID,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
    store: LocalAudioObjectStore = Depends(get_audio_store),
):
    require_identity_user(session, identity)
    try:
        token = issue_verifier_playback_token(session, store, assignment_id, identity)
    except Exception as exc:
        raise HTTPException(status_code=403, detail={"code": "AUDIO_NOT_AUTHORISED"}) from exc
    return {"url": f"/private-audio/play/{token}"}


@router.post("/assignments/{assignment_id}/answer", response_model=AssignmentResponse)
def answer_assignment(
    assignment_id: uuid.UUID,
    request: AssignmentAnswerRequest,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
) -> AssignmentResponse:
    require_identity_user(session, identity)
    assignment = session.scalar(
        select(Assignment).where(Assignment.id == assignment_id).with_for_update()
    )
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
    return _assignment_response(assignment, contribution.declared_language)


@router.post("/assignments/{assignment_id}/referee", response_model=AssignmentResponse)
def referee_assignment(
    assignment_id: uuid.UUID,
    request: AssignmentAnswerRequest,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
) -> AssignmentResponse:
    require_identity_user(session, identity)
    assignment = session.scalar(
        select(Assignment).where(Assignment.id == assignment_id).with_for_update()
    )
    if assignment is None or assignment.verifier_id != identity.user_id:
        raise HTTPException(status_code=403, detail={"code": "ASSIGNMENT_NOT_AUTHORISED"})
    if assignment.mode != AssignmentMode.PROFICIENT_VERIFIER:
        raise HTTPException(status_code=409, detail={"code": "REFEREE_NOT_ALLOWED"})
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
    return _assignment_response(assignment, contribution.declared_language)


@router.get("/contributions/{contribution_id}/result", response_model=ContributionResult)
def contribution_result(
    contribution_id: uuid.UUID,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
) -> ContributionResult:
    require_identity_user(session, identity)
    contribution = session.get(Contribution, contribution_id)
    if contribution is None or contribution.speaker_id != identity.user_id:
        raise HTTPException(status_code=403, detail={"code": "AUDIO_NOT_AUTHORISED"})
    decision = session.get(EligibilityDecision, contribution_id)
    if decision is None:
        return ContributionResult(status="PENDING")
    return ContributionResult(
        status="RESOLVED",
        outcome="CORPUS_ELIGIBLE" if decision.corpus_eligible else "UNVALIDATED",
        reward_minor=session.scalar(select(RewardEvent.amount_cents).where(RewardEvent.contribution_id == contribution_id).limit(1)) or 0,
        understood=decision.understood,
        corpus_eligible=decision.corpus_eligible,
        reason=decision.reason,
    )
