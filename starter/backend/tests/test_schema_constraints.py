"""Schema-level tests (S5): CHECK/UNIQUE constraints from `plan/02_TECH.md`
§3-§4 and `content/SCHEMA.md`, run against a real embedded PostgreSQL 16 --
not asserted from reading the model code, actually attempted and observed
to raise or not raise.
"""
from __future__ import annotations

import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import (
    Campaign,
    Card,
    User,
)


def _campaign(**overrides) -> Campaign:
    defaults = dict(name="Setswana pilot", language="tn", budget_cents=10_000, funded_cents=5_000, committed_cents=0)
    defaults.update(overrides)
    return Campaign(**defaults)


def _card(campaign_id, **overrides) -> Card:
    defaults = dict(
        language="tn",
        target="sefofane",
        blocked_words=["fofa", "loapi", "maeto", "boemafofane"],
        accepted_answers=["sefofane", "difofane"],
        distractors=["koloi", "teksi", "setimela"],
        campaign_id=campaign_id,
    )
    defaults.update(overrides)
    return Card(**defaults)


# --- Campaign CHECK constraints -----------------------------------------


def test_campaign_committed_le_funded_accepted(db_session):
    c = _campaign(funded_cents=5_000, committed_cents=5_000)
    db_session.add(c)
    db_session.commit()  # committed == funded is allowed (the boundary itself)


def test_campaign_committed_exceeds_funded_rejected(db_session):
    """§8 invariant 5: campaign commitments never exceed the funded budget."""
    c = _campaign(funded_cents=5_000, committed_cents=5_001)
    db_session.add(c)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_campaign_negative_committed_rejected(db_session):
    c = _campaign(committed_cents=-1)
    db_session.add(c)
    with pytest.raises(IntegrityError):
        db_session.commit()


# --- Card CHECK constraints (content/SCHEMA.md field rules) -------------


def test_card_with_valid_shape_accepted(db_session):
    campaign = _campaign()
    db_session.add(campaign)
    db_session.flush()
    card = _card(campaign.id)
    db_session.add(card)
    db_session.commit()


def test_card_with_single_accepted_answer_rejected(db_session):
    """SCHEMA.md's build-gate check: the bare target alone is not
    exhaustive -- accepted_answers needs >= 2 entries."""
    campaign = _campaign()
    db_session.add(campaign)
    db_session.flush()
    card = _card(campaign.id, accepted_answers=["sefofane"])
    db_session.add(card)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_card_with_wrong_blocked_words_count_rejected(db_session):
    """SCHEMA.md: blocked_words -- exactly 4."""
    campaign = _campaign()
    db_session.add(campaign)
    db_session.flush()
    card = _card(campaign.id, blocked_words=["fofa", "loapi", "maeto"])
    db_session.add(card)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_card_with_wrong_distractor_count_rejected(db_session):
    """SCHEMA.md: distractors -- exactly 3."""
    campaign = _campaign()
    db_session.add(campaign)
    db_session.flush()
    card = _card(campaign.id, distractors=["koloi", "teksi"])
    db_session.add(card)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_card_requires_existing_campaign_fk(db_session):
    card = _card(uuid.uuid4())  # no such campaign row
    db_session.add(card)
    with pytest.raises(IntegrityError):
        db_session.commit()


# --- User uniqueness ------------------------------------------------------


def test_duplicate_provider_subject_rejected(db_session):
    db_session.add(User(provider_subject="msisdn:2771...", declared_languages=["tn"]))
    db_session.commit()
    db_session.add(User(provider_subject="msisdn:2771...", declared_languages=["zu"]))
    with pytest.raises(IntegrityError):
        db_session.commit()
