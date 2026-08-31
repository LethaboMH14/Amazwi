"""Assignment invariant tests (§5), run against real PostgreSQL.

Only the invariant that's actually enforceable as a single-table
constraint is tested here: the same verifier cannot receive the same
contribution twice (UniqueConstraint on (contribution_id, verifier_id)).

Not tested here (deliberately, not an oversight): "the speaker cannot
verify their own contribution" and "assignment is random within the
eligible closed cohort" are assignment-creation *business logic*, not
schema constraints -- §5 itself says a CHECK can't enforce no-self-
assignment across tables, and the assignment-creation service function
doesn't exist yet (this session builds S5's schema/ledger layer, not the
assignment/resolver service -- see BUILD_LOG.md's NEXT). Testing them here
would mean inventing an assignment service just to test it, which is out
of scope for a schema-layer PR.
"""
from __future__ import annotations

import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Assignment, AssignmentMode, Campaign, Card, Contribution, ContributionState, User


def _user(db_session, **overrides) -> User:
    defaults = dict(provider_subject=f"msisdn:{uuid.uuid4().hex[:10]}", declared_languages=["tn"])
    defaults.update(overrides)
    u = User(**defaults)
    db_session.add(u)
    db_session.flush()
    return u


def _contribution(db_session, speaker) -> Contribution:
    campaign = Campaign(name="c", language="tn", budget_cents=1000, funded_cents=1000, committed_cents=0)
    db_session.add(campaign)
    db_session.flush()
    card = Card(
        language="tn",
        target="sefofane",
        blocked_words=["fofa", "loapi", "maeto", "boemafofane"],
        accepted_answers=["sefofane", "difofane"],
        distractors=["koloi", "teksi", "setimela"],
        campaign_id=campaign.id,
    )
    db_session.add(card)
    db_session.flush()
    contribution = Contribution(
        speaker_id=speaker.id,
        card_id=card.id,
        declared_language="tn",
        state=ContributionState.OPEN,
    )
    db_session.add(contribution)
    db_session.flush()
    return contribution


def test_same_verifier_cannot_be_assigned_same_contribution_twice(db_session):
    speaker = _user(db_session)
    verifier = _user(db_session)
    contribution = _contribution(db_session, speaker)

    db_session.add(Assignment(
        contribution_id=contribution.id,
        verifier_id=verifier.id,
        mode=AssignmentMode.PROFICIENT_VERIFIER,
    ))
    db_session.commit()

    db_session.add(Assignment(
        contribution_id=contribution.id,
        verifier_id=verifier.id,
        mode=AssignmentMode.PROFICIENT_VERIFIER,
    ))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_two_different_verifiers_can_both_be_assigned_same_contribution(db_session):
    """The invariant is per-(contribution, verifier), not one-assignment-
    per-contribution -- exactly two DIFFERENT proficient verifiers must be
    assignable to the same contribution (§5's own requirement)."""
    speaker = _user(db_session)
    v1 = _user(db_session)
    v2 = _user(db_session)
    contribution = _contribution(db_session, speaker)

    db_session.add(Assignment(contribution_id=contribution.id, verifier_id=v1.id, mode=AssignmentMode.PROFICIENT_VERIFIER))
    db_session.add(Assignment(contribution_id=contribution.id, verifier_id=v2.id, mode=AssignmentMode.PROFICIENT_VERIFIER))
    db_session.commit()  # must not raise
