from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models import (
    AudioObject,
    AudioObjectState,
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

NOW = datetime.now(timezone.utc)


def _user(provider_subject: str) -> User:
    return User(
        id=uuid.uuid4(),
        provider_subject=provider_subject,
        declared_languages=["tn"],
        created_at=NOW,
    )


@pytest.fixture()
def user(db_session):
    value = _user("schema-user")
    db_session.add(value)
    db_session.flush()
    return value


@pytest.fixture()
def reviewer(db_session):
    value = _user("schema-reviewer")
    db_session.add(value)
    db_session.flush()
    return value


@pytest.fixture()
def campaign(db_session):
    value = Campaign(
        id=uuid.uuid4(),
        name="Schema campaign",
        language="tn",
        budget_cents=1000,
        funded_cents=1000,
        committed_cents=0,
        provider_mode="DEMO_PROVIDER",
    )
    db_session.add(value)
    db_session.flush()
    return value


@pytest.fixture()
def contribution_factory(db_session, user, campaign):
    card = Card(
        id=uuid.uuid4(),
        language="tn",
        target="hello",
        blocked_words=["a", "b", "c", "d"],
        accepted_answers=["hello", "hi"],
        distractors=["one", "two", "three"],
        campaign_id=campaign.id,
        active=True,
    )
    db_session.add(card)
    db_session.flush()

    def create(**kwargs):
        value = Contribution(
            id=uuid.uuid4(),
            speaker_id=user.id,
            card_id=card.id,
            declared_language="tn",
            state=ContributionState.DRAFT,
            created_at=NOW,
            **kwargs,
        )
        db_session.add(value)
        db_session.flush()
        return value

    return create


@pytest.fixture()
def contribution(contribution_factory):
    return contribution_factory()


@pytest.fixture()
def two_contributions(contribution_factory):
    return contribution_factory(), contribution_factory()


@pytest.fixture()
def reward_rule(db_session, campaign):
    value = CampaignRewardRule(
        id=uuid.uuid4(),
        campaign_id=campaign.id,
        version="speaker-v1",
        contribution_reward_cents=200,
        effective_from=NOW,
    )
    db_session.add(value)
    db_session.flush()
    return value


def test_only_one_active_grant_per_user_scope(db_session, user):
    db_session.add(
        ConsentGrant(
            user_id=user.id,
            version="2026-09-01",
            scope=ConsentScope.RECORD_PROCESS_ROUND,
        )
    )
    db_session.commit()
    db_session.add(
        ConsentGrant(
            user_id=user.id,
            version="2026-09-01",
            scope=ConsentScope.RECORD_PROCESS_ROUND,
        )
    )
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_only_one_audio_object_exists_per_contribution(db_session, contribution):
    db_session.add(
        AudioObject(
            contribution_id=contribution.id,
            object_key="audio/a",
            sha256="a" * 64,
            state=AudioObjectState.AVAILABLE,
        )
    )
    db_session.commit()
    db_session.add(
        AudioObject(
            contribution_id=contribution.id,
            object_key="audio/b",
            sha256="b" * 64,
            state=AudioObjectState.AVAILABLE,
        )
    )
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_duplicate_hash_is_recorded_not_rejected(db_session, two_contributions):
    for contribution, key in zip(two_contributions, ("audio/a", "audio/b")):
        db_session.add(
            AudioObject(
                contribution_id=contribution.id,
                object_key=key,
                sha256="a" * 64,
                state=AudioObjectState.AVAILABLE,
            )
        )
    db_session.commit()
    assert db_session.scalar(select(AudioObject).where(AudioObject.sha256 == "a" * 64))


def test_verifier_qualification_is_persisted_per_language(db_session, user, reviewer):
    db_session.add(
        VerifierQualification(
            user_id=user.id,
            language="tn",
            qualified_at=NOW,
            reviewed_by=reviewer.id,
        )
    )
    db_session.commit()
    assert db_session.scalar(
        select(VerifierQualification).where(VerifierQualification.user_id == user.id)
    )


def test_reward_rule_is_positive_and_contribution_snapshots_rule(
    db_session, campaign, contribution_factory
):
    rule = CampaignRewardRule(
        campaign_id=campaign.id,
        version="speaker-v1",
        contribution_reward_cents=200,
        effective_from=NOW,
    )
    db_session.add(rule)
    db_session.flush()
    contribution = contribution_factory(reward_rule_id=rule.id)
    db_session.commit()
    assert contribution.reward_rule_id == rule.id


def test_reward_rule_rejects_non_positive_amount(db_session, campaign):
    db_session.add(
        CampaignRewardRule(
            campaign_id=campaign.id,
            version="invalid",
            contribution_reward_cents=0,
            effective_from=NOW,
        )
    )
    with pytest.raises(IntegrityError):
        db_session.commit()
