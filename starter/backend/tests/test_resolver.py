"""Tests for app/resolver.py (§5), run against real PostgreSQL 16.

Covers:
  - create_assignment(): self-verification rejected, double-assignment
    rejected (via the DB constraint, not reimplemented here), expired/
    voided contribution rejected, a normal assignment succeeds.
  - resolve_contribution(): every branch of §5's resolver pseudocode,
    plus "safe to call repeatedly" (calling twice returns the same
    decision and does not credit a second reward -- exercises
    credit_reward's own idempotency from app/ledger.py, not a separate
    mechanism).
"""
from __future__ import annotations

import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from threading import Barrier

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import (
    Assignment,
    AssignmentMode,
    AudioObject,
    AudioObjectState,
    Campaign,
    CampaignRewardRule,
    Card,
    ConsentGrant,
    ConsentScope,
    Contribution,
    ContributionState,
    EligibilityDecision,
    OutboxEvent,
    RewardEvent,
    User,
)
from app.resolver import (
    AudioNotAssignableError,
    CampaignRewardNotConfiguredError,
    SelfVerificationError,
    create_assignment,
    resolve_from_persisted_state,
    resolve_contribution,
)


def _user(db_session, **overrides) -> User:
    defaults = dict(provider_subject=f"msisdn:{uuid.uuid4().hex[:10]}", declared_languages=["tn"])
    defaults.update(overrides)
    u = User(**defaults)
    db_session.add(u)
    db_session.flush()
    return u


def _campaign(db_session, **overrides) -> Campaign:
    defaults = dict(name="test campaign", language="tn", budget_cents=100_000, funded_cents=10_000, committed_cents=0)
    defaults.update(overrides)
    c = Campaign(**defaults)
    db_session.add(c)
    db_session.flush()
    return c


def _contribution(db_session, speaker: User, campaign: Campaign | None = None, **overrides) -> Contribution:
    if campaign is None:
        campaign = _campaign(db_session)
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
    defaults = dict(
        speaker_id=speaker.id,
        card_id=card.id,
        declared_language="tn",
        state=ContributionState.OPEN,
    )
    defaults.update(overrides)
    contribution = Contribution(**defaults)
    db_session.add(contribution)
    db_session.flush()
    db_session.commit()
    return contribution


def _answered_assignment(db_session, contribution, verifier, *, matched: bool, violation_vote: bool) -> Assignment:
    a = Assignment(
        contribution_id=contribution.id,
        verifier_id=verifier.id,
        mode=AssignmentMode.PROFICIENT_VERIFIER,
        answer_text="sefofane",
        answer_normalised="sefofane",
        matched=matched,
        violation_vote=violation_vote,
        answered_at=datetime.now(timezone.utc),
    )
    db_session.add(a)
    db_session.commit()
    return a


# --- create_assignment() ---


def test_create_assignment_succeeds_for_normal_case(db_session):
    speaker = _user(db_session)
    verifier = _user(db_session)
    contribution = _contribution(db_session, speaker)

    assignment = create_assignment(
        db_session, contribution_id=contribution.id, verifier_id=verifier.id, mode=AssignmentMode.PROFICIENT_VERIFIER
    )
    assert assignment.id is not None
    assert assignment.verifier_id == verifier.id


def test_create_assignment_rejects_self_verification(db_session):
    speaker = _user(db_session)
    contribution = _contribution(db_session, speaker)

    with pytest.raises(SelfVerificationError):
        create_assignment(
            db_session, contribution_id=contribution.id, verifier_id=speaker.id, mode=AssignmentMode.PROFICIENT_VERIFIER
        )


def test_create_assignment_rejects_double_assignment_via_db_constraint(db_session):
    """The no-double-assignment invariant is enforced by the schema's
    UniqueConstraint (app/models.py), not reimplemented in the service
    layer -- this test proves create_assignment() doesn't accidentally
    swallow that IntegrityError."""
    speaker = _user(db_session)
    verifier = _user(db_session)
    contribution = _contribution(db_session, speaker)

    create_assignment(db_session, contribution_id=contribution.id, verifier_id=verifier.id, mode=AssignmentMode.PROFICIENT_VERIFIER)
    with pytest.raises(IntegrityError):
        create_assignment(db_session, contribution_id=contribution.id, verifier_id=verifier.id, mode=AssignmentMode.PROFICIENT_VERIFIER)


def test_create_assignment_rejects_voided_contribution(db_session):
    speaker = _user(db_session)
    verifier = _user(db_session)
    contribution = _contribution(db_session, speaker, state=ContributionState.VOIDED)

    with pytest.raises(AudioNotAssignableError):
        create_assignment(db_session, contribution_id=contribution.id, verifier_id=verifier.id, mode=AssignmentMode.PROFICIENT_VERIFIER)


def test_create_assignment_rejects_expired_contribution(db_session):
    speaker = _user(db_session)
    verifier = _user(db_session)
    past = datetime.now(timezone.utc) - timedelta(hours=1)
    contribution = _contribution(db_session, speaker, expires_at=past)

    with pytest.raises(AudioNotAssignableError):
        create_assignment(db_session, contribution_id=contribution.id, verifier_id=verifier.id, mode=AssignmentMode.PROFICIENT_VERIFIER)


def test_create_assignment_two_different_verifiers_both_succeed(db_session):
    speaker = _user(db_session)
    v1, v2 = _user(db_session), _user(db_session)
    contribution = _contribution(db_session, speaker)

    create_assignment(db_session, contribution_id=contribution.id, verifier_id=v1.id, mode=AssignmentMode.PROFICIENT_VERIFIER)
    create_assignment(db_session, contribution_id=contribution.id, verifier_id=v2.id, mode=AssignmentMode.PROFICIENT_VERIFIER)  # must not raise


# --- resolve_contribution(): pseudocode branches ---


def test_resolve_remains_open_with_fewer_than_two_answers(db_session):
    speaker = _user(db_session)
    v1 = _user(db_session)
    contribution = _contribution(db_session, speaker)
    _answered_assignment(db_session, contribution, v1, matched=True, violation_vote=False)

    decision = resolve_contribution(db_session, contribution_id=contribution.id, audio_quality_passed=True, consent_active=True)
    assert decision is None
    db_session.refresh(contribution)
    assert contribution.state == ContributionState.OPEN


def test_resolve_learner_mcq_does_not_count_toward_threshold(db_session):
    """§5: 'learner MCQ assignments never count toward that two.'"""
    speaker = _user(db_session)
    v1 = _user(db_session)
    learner = _user(db_session)
    contribution = _contribution(db_session, speaker)
    _answered_assignment(db_session, contribution, v1, matched=True, violation_vote=False)
    learner_assignment = Assignment(
        contribution_id=contribution.id,
        verifier_id=learner.id,
        mode=AssignmentMode.LEARNER_MCQ,
        matched=True,
        violation_vote=False,
        answered_at=datetime.now(timezone.utc),
    )
    db_session.add(learner_assignment)
    db_session.commit()

    decision = resolve_contribution(db_session, contribution_id=contribution.id, audio_quality_passed=True, consent_active=True)
    assert decision is None  # still only 1 proficient answer -- the learner one doesn't count


def test_resolve_both_violation_votes_true_voids(db_session):
    speaker = _user(db_session)
    v1, v2 = _user(db_session), _user(db_session)
    contribution = _contribution(db_session, speaker)
    _answered_assignment(db_session, contribution, v1, matched=True, violation_vote=True)
    _answered_assignment(db_session, contribution, v2, matched=True, violation_vote=True)

    decision = resolve_contribution(db_session, contribution_id=contribution.id, audio_quality_passed=True, consent_active=True)
    assert decision.understood is False
    assert decision.corpus_eligible is False
    db_session.refresh(contribution)
    assert contribution.state == ContributionState.VOIDED


def test_resolve_violation_votes_disagree_review_required(db_session):
    speaker = _user(db_session)
    v1, v2 = _user(db_session), _user(db_session)
    contribution = _contribution(db_session, speaker)
    _answered_assignment(db_session, contribution, v1, matched=True, violation_vote=True)
    _answered_assignment(db_session, contribution, v2, matched=True, violation_vote=False)

    decision = resolve_contribution(db_session, contribution_id=contribution.id, audio_quality_passed=True, consent_active=True)
    assert decision.understood is False
    db_session.refresh(contribution)
    assert contribution.state == ContributionState.REVIEW_REQUIRED


def test_resolve_both_matched_quality_and_consent_ok_corpus_eligible_and_reward_credited(db_session):
    speaker = _user(db_session)
    v1, v2 = _user(db_session), _user(db_session)
    campaign = _campaign(db_session, funded_cents=10_000, committed_cents=0)
    contribution = _contribution(db_session, speaker, campaign)
    _answered_assignment(db_session, contribution, v1, matched=True, violation_vote=False)
    _answered_assignment(db_session, contribution, v2, matched=True, violation_vote=False)

    decision = resolve_contribution(
        db_session,
        contribution_id=contribution.id,
        audio_quality_passed=True,
        consent_active=True,
        reward_amount_cents=200,
        campaign_id=campaign.id,
    )
    assert decision.understood is True
    assert decision.corpus_eligible is True
    db_session.refresh(contribution)
    assert contribution.state == ContributionState.CORPUS_ELIGIBLE

    reward = db_session.query(RewardEvent).filter_by(contribution_id=contribution.id).one()
    assert reward.amount_cents == 200
    assert reward.user_id == speaker.id


def test_resolve_rolls_back_state_and_decision_when_reward_cannot_be_committed(db_session):
    """§5 requires resolution to be one transaction, including its reward.

    A reward that exceeds the funded campaign budget must not leave a terminal
    contribution state or an EligibilityDecision behind. Otherwise a retry
    would see the decision and never be able to credit the speaker.
    """
    speaker = _user(db_session)
    v1, v2 = _user(db_session), _user(db_session)
    campaign = _campaign(db_session, funded_cents=100, committed_cents=0)
    contribution = _contribution(db_session, speaker, campaign)
    _answered_assignment(db_session, contribution, v1, matched=True, violation_vote=False)
    _answered_assignment(db_session, contribution, v2, matched=True, violation_vote=False)

    with pytest.raises(IntegrityError):
        resolve_contribution(
            db_session,
            contribution_id=contribution.id,
            audio_quality_passed=True,
            consent_active=True,
            reward_amount_cents=200,
            campaign_id=campaign.id,
        )

    db_session.rollback()
    db_session.refresh(contribution)
    assert contribution.state == ContributionState.OPEN
    assert db_session.get(EligibilityDecision, contribution.id) is None
    assert db_session.query(RewardEvent).filter_by(contribution_id=contribution.id).count() == 0
    # Plan 02's Stop Rule for Stage 4 is explicit that a rollback must not
    # leave an event behind: a surviving ContributionResolved row would let
    # the Council publish an outcome for a resolution that never committed.
    assert db_session.query(OutboxEvent).filter_by(aggregate_id=contribution.id).count() == 0


def test_resolve_eligible_requires_a_positive_explicit_reward_amount(db_session):
    """The resolver may not silently turn an omitted amount into 0 cents."""
    speaker = _user(db_session)
    v1, v2 = _user(db_session), _user(db_session)
    contribution = _contribution(db_session, speaker)
    _answered_assignment(db_session, contribution, v1, matched=True, violation_vote=False)
    _answered_assignment(db_session, contribution, v2, matched=True, violation_vote=False)

    with pytest.raises(ValueError, match="positive reward_amount_cents"):
        resolve_contribution(
            db_session,
            contribution_id=contribution.id,
            audio_quality_passed=True,
            consent_active=True,
        )

    db_session.refresh(contribution)
    assert contribution.state == ContributionState.OPEN
    assert db_session.get(EligibilityDecision, contribution.id) is None
    assert db_session.query(RewardEvent).filter_by(contribution_id=contribution.id).count() == 0
    # Plan 02's Stop Rule for Stage 4 is explicit that a rollback must not
    # leave an event behind: a surviving ContributionResolved row would let
    # the Council publish an outcome for a resolution that never committed.
    assert db_session.query(OutboxEvent).filter_by(aggregate_id=contribution.id).count() == 0


def test_resolve_both_matched_but_quality_failed_unvalidated_no_reward(db_session):
    speaker = _user(db_session)
    v1, v2 = _user(db_session), _user(db_session)
    contribution = _contribution(db_session, speaker)
    _answered_assignment(db_session, contribution, v1, matched=True, violation_vote=False)
    _answered_assignment(db_session, contribution, v2, matched=True, violation_vote=False)

    decision = resolve_contribution(db_session, contribution_id=contribution.id, audio_quality_passed=False, consent_active=True)
    assert decision.understood is True
    assert decision.corpus_eligible is False
    db_session.refresh(contribution)
    assert contribution.state == ContributionState.UNVALIDATED
    assert db_session.query(RewardEvent).filter_by(contribution_id=contribution.id).count() == 0


def test_resolve_both_matched_but_consent_inactive_unvalidated_no_reward(db_session):
    speaker = _user(db_session)
    v1, v2 = _user(db_session), _user(db_session)
    contribution = _contribution(db_session, speaker)
    _answered_assignment(db_session, contribution, v1, matched=True, violation_vote=False)
    _answered_assignment(db_session, contribution, v2, matched=True, violation_vote=False)

    decision = resolve_contribution(db_session, contribution_id=contribution.id, audio_quality_passed=True, consent_active=False)
    assert decision.corpus_eligible is False
    assert db_session.query(RewardEvent).filter_by(contribution_id=contribution.id).count() == 0


def test_resolve_answers_dont_both_match_unvalidated(db_session):
    speaker = _user(db_session)
    v1, v2 = _user(db_session), _user(db_session)
    contribution = _contribution(db_session, speaker)
    _answered_assignment(db_session, contribution, v1, matched=True, violation_vote=False)
    _answered_assignment(db_session, contribution, v2, matched=False, violation_vote=False)

    decision = resolve_contribution(db_session, contribution_id=contribution.id, audio_quality_passed=True, consent_active=True)
    assert decision.understood is False
    assert decision.corpus_eligible is False
    db_session.refresh(contribution)
    assert contribution.state == ContributionState.UNVALIDATED


# --- "safe to call repeatedly" ---


def test_resolve_called_twice_returns_same_decision_and_credits_one_reward(db_session):
    """§5: 'Resolution runs in a database transaction and is safe to call
    repeatedly.' Proves both halves: the SAME EligibilityDecision row
    comes back (no re-decision), and only one RewardEvent exists even
    after two full resolve_contribution() calls."""
    speaker = _user(db_session)
    v1, v2 = _user(db_session), _user(db_session)
    contribution = _contribution(db_session, speaker)
    _answered_assignment(db_session, contribution, v1, matched=True, violation_vote=False)
    _answered_assignment(db_session, contribution, v2, matched=True, violation_vote=False)

    d1 = resolve_contribution(db_session, contribution_id=contribution.id, audio_quality_passed=True, consent_active=True, reward_amount_cents=200)
    d2 = resolve_contribution(db_session, contribution_id=contribution.id, audio_quality_passed=True, consent_active=True, reward_amount_cents=200)

    assert d1.contribution_id == d2.contribution_id
    rewards = db_session.query(RewardEvent).filter_by(contribution_id=contribution.id).all()
    assert len(rewards) == 1


def test_persisted_resolution_uses_snapshot_and_is_idempotent_across_sessions(db_session):
    speaker = _user(db_session)
    v1, v2 = _user(db_session), _user(db_session)
    campaign = _campaign(db_session, funded_cents=1_000)
    contribution = _contribution(db_session, speaker, campaign)
    rule = CampaignRewardRule(
        campaign_id=campaign.id,
        version="snapshot-v2",
        contribution_reward_cents=125,
        effective_from=datetime.now(timezone.utc),
    )
    db_session.add(rule)
    db_session.flush()
    contribution.reward_rule_id = rule.id
    db_session.add(ConsentGrant(
        user_id=speaker.id,
        version="consent-v3",
        scope=ConsentScope.RECORD_PROCESS_ROUND,
    ))
    db_session.add(AudioObject(
        contribution_id=contribution.id,
        object_key=f"audio/{contribution.id}",
        sha256="a" * 64,
        mime_type="audio/wav",
        codec="pcm",
        duration_ms=1000,
        byte_length=10,
        state=AudioObjectState.AVAILABLE,
    ))
    db_session.commit()
    _answered_assignment(db_session, contribution, v1, matched=True, violation_vote=False)
    _answered_assignment(db_session, contribution, v2, matched=True, violation_vote=False)

    barrier = Barrier(2)

    def resolve_in_new_session():
        session = Session(db_session.bind)
        try:
            barrier.wait(timeout=10)
            decision = resolve_from_persisted_state(session, contribution.id)
            return decision.contribution_id, decision.corpus_eligible
        finally:
            session.close()

    with ThreadPoolExecutor(max_workers=2) as executor:
        decisions = list(executor.map(lambda _: resolve_in_new_session(), range(2)))

    assert {decision_id for decision_id, _ in decisions} == {contribution.id}
    assert all(corpus_eligible for _, corpus_eligible in decisions)
    assert db_session.query(EligibilityDecision).filter_by(contribution_id=contribution.id).count() == 1
    assert db_session.query(RewardEvent).filter_by(contribution_id=contribution.id).count() == 1
    db_session.refresh(campaign)
    assert campaign.committed_cents == 125


def test_persisted_resolution_rejects_missing_reward_rule_without_decision(db_session):
    speaker = _user(db_session)
    v1, v2 = _user(db_session), _user(db_session)
    contribution = _contribution(db_session, speaker)
    _answered_assignment(db_session, contribution, v1, matched=True, violation_vote=False)
    _answered_assignment(db_session, contribution, v2, matched=True, violation_vote=False)

    with pytest.raises(CampaignRewardNotConfiguredError):
        resolve_from_persisted_state(db_session, contribution.id)
    assert db_session.get(EligibilityDecision, contribution.id) is None
    assert db_session.query(OutboxEvent).filter_by(aggregate_id=contribution.id).count() == 0
