from datetime import datetime, timezone
import random
import uuid

import pytest

from app.cohorts import select_next_verifier
from app.consent import revoke_scope
from app.models import (
    Assignment,
    AssignmentMode,
    Campaign,
    CampaignRewardRule,
    Card,
    ConsentGrant,
    ConsentScope,
    Contribution,
    ContributionState,
    User,
    VerifierQualification,
)


@pytest.fixture
def cohort_context(db_session):
    now = datetime.now(timezone.utc)
    speaker = User(id=uuid.uuid4(), provider_subject="cohort-speaker", declared_languages=["tn"], age_confirmed_at=now, created_at=now)
    eligible = User(id=uuid.uuid4(), provider_subject="cohort-eligible", declared_languages=["tn"], age_confirmed_at=now, created_at=now)
    wrong_language = User(id=uuid.uuid4(), provider_subject="cohort-wrong", declared_languages=["en"], age_confirmed_at=now, created_at=now)
    campaign = Campaign(id=uuid.uuid4(), name="Cohort", language="tn", budget_cents=1000, funded_cents=1000, committed_cents=0, provider_mode="DEMO_PROVIDER")
    rule = CampaignRewardRule(id=uuid.uuid4(), campaign_id=campaign.id, version="v1", contribution_reward_cents=100, effective_from=now)
    card = Card(id=uuid.uuid4(), language="tn", target="kgomo", blocked_words=["a", "b", "c", "d"], accepted_answers=["kgomo", "kgomo"], distractors=["x", "y", "z"], campaign_id=campaign.id, active=True)
    contribution = Contribution(id=uuid.uuid4(), speaker_id=speaker.id, card_id=card.id, declared_language="tn", state=ContributionState.OPEN, reward_rule_id=rule.id, created_at=now)
    db_session.add_all([speaker, eligible, wrong_language, campaign])
    db_session.flush()
    db_session.add(rule)
    db_session.flush()
    db_session.add(card)
    db_session.flush()
    db_session.add(contribution)
    db_session.flush()
    db_session.add_all([
        ConsentGrant(user_id=speaker.id, version="v1", scope=ConsentScope.ASSIGNED_VERIFIER_PLAYBACK),
        VerifierQualification(user_id=eligible.id, language="tn", qualified_at=now, reviewed_by=speaker.id),
        VerifierQualification(user_id=wrong_language.id, language="en", qualified_at=now, reviewed_by=speaker.id),
    ])
    db_session.commit()
    return speaker, eligible, wrong_language, contribution


def test_cohort_excludes_speaker_wrong_language_and_prior_assignees(db_session, cohort_context):
    speaker, eligible, _, contribution = cohort_context
    chosen = select_next_verifier(db_session, contribution.id, "tn", random.Random(7))
    assert chosen.id == eligible.id
    db_session.add(Assignment(contribution_id=contribution.id, verifier_id=eligible.id, mode=AssignmentMode.PROFICIENT_VERIFIER))
    db_session.commit()
    assert select_next_verifier(db_session, contribution.id, "tn", random.Random(7)) is None


def test_revoked_playback_consent_yields_no_assignment(db_session, cohort_context):
    speaker, _, _, contribution = cohort_context
    revoke_scope(db_session, speaker.id, ConsentScope.ASSIGNED_VERIFIER_PLAYBACK, speaker.id, "stop")
    db_session.commit()
    assert select_next_verifier(db_session, contribution.id, "tn", random.Random(7)) is None
