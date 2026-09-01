"""Assignment and resolution service (§5, cross-lane, pending Sbu's review).

Continues directly from S5's schema/ledger work -- this session's NEXT item.
Implements:

  - create_assignment(): the assignment invariants from §5's "Assignment
    invariants" list that are NOT already enforced by a DB constraint
    (no-self-verification, no double-assignment already caught by the
    schema's UniqueConstraint, revoked/expired audio not assignable).
  - resolve_contribution(): §5's resolver pseudocode, verbatim -- same
    branch structure, same states, nothing added or reordered.

Deliberately NOT built here (real scope boundaries, not oversights):

  - "assignment is random within the eligible closed cohort for the
    language" -- the actual cohort-selection/pooling logic (who's eligible
    to be assigned what) needs the consent/audio-storage layer (§7, §10)
    this session didn't build. create_assignment() takes an explicit
    verifier_id rather than picking one, so the caller (a future
    assignment-dispatch job) supplies the already-selected verifier.
  - Consent and audio-quality state are not modelled as their own tables
    yet (§10's ConsentGrant exists in app/models.py but nothing yet
    computes "required consent is active" from it, and Contribution's
    quality_json is opaque). resolve_contribution() takes explicit
    `audio_quality_passed` and `consent_active` booleans rather than
    invent that derivation now -- the resolver's own branch logic is
    what's being implemented and tested here, not the consent/quality
    subsystems that will eventually supply those booleans.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ledger import credit_reward
from app.consent import require_active_scope, ConsentRequiredError
from app.models import (
    Assignment,
    AssignmentMode,
    AudioObject,
    AudioObjectState,
    CampaignRewardRule,
    Contribution,
    ContributionState,
    EligibilityDecision,
    ConsentScope,
)


class SelfVerificationError(Exception):
    """§5: 'the speaker cannot verify their own contribution.' A CHECK
    constraint can't enforce this across the contributions/assignments
    tables (§5 says so explicitly), so it's enforced here, in the
    assignment-creation transaction."""


class AudioNotAssignableError(Exception):
    """§5: 'revoked or expired audio cannot be assigned.'"""


def create_assignment(
    session: Session,
    *,
    contribution_id: uuid.UUID,
    verifier_id: uuid.UUID,
    mode: AssignmentMode,
) -> Assignment:
    """Creates one assignment, enforcing the invariants a DB constraint
    can't reach on its own. The remaining §5 invariants are enforced
    elsewhere already:
      - no double-assignment: Assignment's UniqueConstraint on
        (contribution_id, verifier_id) (app/models.py) -- committing a
        duplicate here raises IntegrityError, which this function does
        not swallow; that's the caller's signal.
      - learner MCQ never counting toward the resolution threshold: the
        resolver below only counts AssignmentMode.PROFICIENT_VERIFIER rows.
        """

    contribution = session.get(Contribution, contribution_id)
    if contribution is None:
        raise ValueError(f"no such contribution {contribution_id}")

    if contribution.speaker_id == verifier_id:
        raise SelfVerificationError(
            f"user {verifier_id} is the speaker of contribution {contribution_id} and cannot verify it"
        )

    if contribution.state in (ContributionState.VOIDED, ContributionState.EXPIRED):
        raise AudioNotAssignableError(
            f"contribution {contribution_id} is {contribution.state.value}, not assignable"
        )
    if contribution.expires_at is not None and contribution.expires_at <= datetime.now(timezone.utc):
        raise AudioNotAssignableError(f"contribution {contribution_id} has expired")

    assignment = Assignment(
        contribution_id=contribution_id,
        verifier_id=verifier_id,
        mode=mode,
    )
    session.add(assignment)
    session.commit()
    return assignment


class ResolutionNotReadyError(Exception):
    pass


def resolve_from_persisted_state(session: Session, contribution_id: uuid.UUID) -> EligibilityDecision:
    """Resolve only from persisted audio, consent, reward, and peer state."""
    existing = session.get(EligibilityDecision, contribution_id)
    if existing is not None:
        return existing
    contribution = session.get(Contribution, contribution_id)
    if contribution is None:
        raise ValueError(f"no such contribution {contribution_id}")
    completed = session.scalars(
        select(Assignment).where(
            Assignment.contribution_id == contribution_id,
            Assignment.mode == AssignmentMode.PROFICIENT_VERIFIER,
            Assignment.answered_at.is_not(None),
        )
    ).all()
    if len(completed) < 2:
        raise ResolutionNotReadyError(f"contribution {contribution_id} needs two proficient answers")
    audio = session.scalar(select(AudioObject).where(AudioObject.contribution_id == contribution_id))
    try:
        consent = require_active_scope(session, contribution.speaker_id, ConsentScope.RECORD_PROCESS_ROUND)
    except ConsentRequiredError:
        consent = None
    rule = session.get(CampaignRewardRule, contribution.reward_rule_id) if contribution.reward_rule_id else None
    return resolve_contribution(
        session,
        contribution_id=contribution_id,
        audio_quality_passed=audio is not None and audio.state == AudioObjectState.AVAILABLE,
        consent_active=consent is not None,
        reward_amount_cents=rule.contribution_reward_cents if rule else None,
        campaign_id=rule.campaign_id if rule else None,
    )


def resolve_contribution(
    session: Session,
    *,
    contribution_id: uuid.UUID,
    audio_quality_passed: bool,
    consent_active: bool,
    reward_amount_cents: Optional[int] = None,
    campaign_id: Optional[uuid.UUID] = None,
) -> EligibilityDecision:
    """§5's resolver, implemented as exactly the stated pseudocode:

        if fewer than 2 proficient answers:
            remain OPEN until expiry
        elif both violation votes are true:
            VOIDED
        elif violation votes disagree:
            REVIEW_REQUIRED
        elif both answers match accepted_answers:
            UNDERSTOOD
            if audio quality passes and required consent is active:
                CORPUS_ELIGIBLE
                credit speaker reward once
            else:
                UNVALIDATED
        else:
            UNVALIDATED

    'Resolution runs in a database transaction and is safe to call
    repeatedly' (§5's own requirement): calling this twice on an already-
    decided contribution returns the existing EligibilityDecision
    unchanged rather than re-deciding or crediting a second reward --
    EligibilityDecision's primary key IS contribution_id (app/models.py),
    so a second insert attempt is structurally impossible; this function
    checks first and returns early, rather than relying on that PK
    collision to signal "already decided" via an exception.

    Returns the EligibilityDecision row. When still OPEN (fewer than two
    proficient answers), returns None instead -- there is nothing to
    persist yet, matching the pseudocode's "remain OPEN" branch, which is
    a non-decision, not a decision recorded as some placeholder state.
    """
    existing = session.get(EligibilityDecision, contribution_id)
    if existing is not None:
        return existing

    contribution = session.get(Contribution, contribution_id)
    if contribution is None:
        raise ValueError(f"no such contribution {contribution_id}")

    proficient_answers = session.execute(
        select(Assignment).where(
            Assignment.contribution_id == contribution_id,
            Assignment.mode == AssignmentMode.PROFICIENT_VERIFIER,
            Assignment.answered_at.is_not(None),
        )
    ).scalars().all()

    if len(proficient_answers) < 2:
        contribution.state = ContributionState.OPEN
        session.commit()
        return None

    # §5: "exactly two completed proficient-verifier assignments are
    # required for automatic resolution" -- only the first two count;
    # a third, if one somehow exists, is not part of the decision. This
    # mirrors the pseudocode's binary branching (it only ever reasons
    # about "both" answers/votes), which presumes exactly two.
    a, b = proficient_answers[0], proficient_answers[1]

    if a.violation_vote and b.violation_vote:
        contribution.state = ContributionState.VOIDED
        understood = False
        corpus_eligible = False
        reason = "both verifiers voted a banned-word violation"
    elif bool(a.violation_vote) != bool(b.violation_vote):
        contribution.state = ContributionState.REVIEW_REQUIRED
        understood = False
        corpus_eligible = False
        reason = "verifiers disagreed on the banned-word violation vote"
    elif bool(a.matched) and bool(b.matched):
        understood = True
        if audio_quality_passed and consent_active:
            corpus_eligible = True
            reason = "understood by both verifiers, audio quality passed, consent active"
            contribution.state = ContributionState.CORPUS_ELIGIBLE
        else:
            corpus_eligible = False
            reason = (
                "understood by both verifiers but "
                + ("consent not active" if not consent_active else "audio quality did not pass")
            )
            contribution.state = ContributionState.UNVALIDATED
    else:
        understood = False
        corpus_eligible = False
        reason = "not both verifier answers matched accepted_answers"
        contribution.state = ContributionState.UNVALIDATED

    decision = EligibilityDecision(
        contribution_id=contribution_id,
        understood=understood,
        corpus_eligible=corpus_eligible,
        reason=reason,
        consent_version="v1" if consent_active else "n/a",
    )
    session.add(decision)

    try:
        if corpus_eligible:
            if reward_amount_cents is None or reward_amount_cents <= 0:
                raise ValueError(
                    "a corpus-eligible resolution requires a positive reward_amount_cents"
                )
            # §5: "credit speaker reward once." Keep this uncommitted until
            # the contribution state and EligibilityDecision can commit with
            # it. A failed budget check must leave all three unchanged.
            credit_reward(
                session,
                contribution_id=contribution_id,
                user_id=contribution.speaker_id,
                reward_type="SPEAKER_HONORARIUM",
                amount_cents=reward_amount_cents,
                idempotency_key=f"resolve-{contribution_id}",
                campaign_id=campaign_id,
                commit=False,
            )
        session.commit()
    except Exception:
        session.rollback()
        raise

    return decision
