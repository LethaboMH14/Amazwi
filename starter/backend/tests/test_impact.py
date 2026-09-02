"""Tests for app/impact.py's aggregate Coverage Constellation query.

Run against real PostgreSQL 16 (see tests/conftest.py) because the
aggregation is a real GROUP BY over real joins, not a Python fold over
synthetic rows -- a SQLite-backed version would not exercise the same
query planner or the ARRAY columns on `cards`.

Note on scope: the plan's (language, province, domain) cell key cannot
be built today -- the schema has no geographic or domain column. These
tests therefore assert the honest approximation actually implemented
(language x campaign), including that `province_code` stays `None` and
`geography_available` stays `False` rather than being faked.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.impact import MIN_CELL_SIZE, build_coverage, count_band
from app.models import (
    Campaign,
    Card,
    Contribution,
    ContributionState,
    EligibilityDecision,
    User,
)

NOW = datetime(2026, 9, 2, 0, 0, tzinfo=timezone.utc)


def _campaign(db_session, name: str, language: str) -> Campaign:
    campaign = Campaign(
        name=name,
        language=language,
        budget_cents=100_000,
        funded_cents=10_000,
        committed_cents=0,
    )
    db_session.add(campaign)
    db_session.flush()
    return campaign


def _card(db_session, campaign: Campaign) -> Card:
    card = Card(
        language=campaign.language,
        target="sefofane",
        blocked_words=["fofa", "loapi", "maeto", "boemafofane"],
        accepted_answers=["sefofane", "difofane"],
        distractors=["koloi", "teksi", "setimela"],
        campaign_id=campaign.id,
    )
    db_session.add(card)
    db_session.flush()
    return card


def _verified(db_session, *, language: str, campaign_name: str, count: int, corpus_eligible: bool = True) -> None:
    """Create `count` real committed, peer-verified contributions."""
    campaign = _campaign(db_session, campaign_name, language)
    card = _card(db_session, campaign)
    for _ in range(count):
        speaker = User(provider_subject=f"msisdn:{uuid.uuid4().hex[:10]}", declared_languages=[language])
        db_session.add(speaker)
        db_session.flush()
        contribution = Contribution(
            speaker_id=speaker.id,
            card_id=card.id,
            declared_language=language,
            state=(
                ContributionState.CORPUS_ELIGIBLE
                if corpus_eligible
                else ContributionState.UNDERSTOOD
            ),
        )
        db_session.add(contribution)
        db_session.flush()
        db_session.add(
            EligibilityDecision(
                contribution_id=contribution.id,
                understood=True,
                corpus_eligible=corpus_eligible,
                reason="PEER_VERIFIED",
                consent_version="2026-09-01",
            )
        )
    db_session.commit()


def test_coverage_suppresses_cells_below_five(db_session):
    _verified(db_session, language="tn", campaign_name="support", count=MIN_CELL_SIZE - 1)
    response = build_coverage(db_session, NOW)
    assert response.nodes == []
    # The underlying total is still reported -- suppression hides the
    # cell, it does not erase the population figure.
    assert response.verified_total == MIN_CELL_SIZE - 1
    assert response.suppressed_cell_count == 1


def test_coverage_publishes_a_cell_at_exactly_the_threshold(db_session):
    _verified(db_session, language="tn", campaign_name="support", count=MIN_CELL_SIZE)
    response = build_coverage(db_session, NOW)
    assert len(response.nodes) == 1
    assert response.nodes[0].verified_count_band == "5-19"
    assert response.suppressed_cell_count == 0


def test_coverage_returns_bands_without_personal_or_audio_fields(db_session):
    _verified(db_session, language="zu", campaign_name="code switch", count=7)
    node = build_coverage(db_session, NOW).nodes[0].model_dump()
    assert node["verified_count_band"] == "5-19"
    forbidden = {"user_id", "speaker_id", "contribution_id", "latitude", "longitude", "audio_url", "audio_key", "transcript"}
    assert forbidden.isdisjoint(node)
    # Exact counts are never published for a cell either.
    assert "verified_count" not in node


def test_only_committed_corpus_eligible_contributions_count(db_session):
    _verified(db_session, language="tn", campaign_name="support", count=6, corpus_eligible=False)
    response = build_coverage(db_session, NOW)
    assert response.verified_total == 0
    assert response.nodes == []


def test_province_and_model_gap_are_null_because_no_such_data_exists(db_session):
    _verified(db_session, language="zu", campaign_name="support", count=6)
    response = build_coverage(db_session, NOW)
    assert response.geography_available is False
    assert response.nodes[0].province_code is None
    assert response.nodes[0].model_gap_percent is None


def test_missions_completed_is_zero_not_approximated(db_session):
    _verified(db_session, language="zu", campaign_name="support", count=6)
    # No mission_proposals table exists yet; the field must not be
    # derived from contribution volume.
    assert build_coverage(db_session, NOW).missions_completed == 0


def test_totals_languages_and_coverage_share(db_session):
    _verified(db_session, language="zu", campaign_name="support", count=30)
    _verified(db_session, language="tn", campaign_name="support", count=10)
    response = build_coverage(db_session, NOW)
    assert response.verified_total == 40
    assert response.languages_active == 2
    bands = {node.language: node.verified_count_band for node in response.nodes}
    assert bands == {"zu": "20-49", "tn": "5-19"}
    shares = {node.language: node.coverage_percent for node in response.nodes}
    assert shares == {"zu": 75, "tn": 25}


def test_nodes_are_deterministically_ordered(db_session):
    _verified(db_session, language="zu", campaign_name="support", count=6)
    _verified(db_session, language="tn", campaign_name="sales", count=6)
    _verified(db_session, language="tn", campaign_name="support", count=6)
    ids = [node.id for node in build_coverage(db_session, NOW).nodes]
    assert ids == sorted(ids)
    assert ids == ["tn:NATIONAL:sales", "tn:NATIONAL:support", "zu:NATIONAL:support"]


def test_count_band_boundaries():
    assert count_band(5) == "5-19"
    assert count_band(19) == "5-19"
    assert count_band(20) == "20-49"
    assert count_band(49) == "20-49"
    assert count_band(50) == "50-99"
    assert count_band(99) == "50-99"
    assert count_band(100) == "100+"
    assert count_band(10_000) == "100+"


def test_empty_database_returns_empty_but_valid_response(db_session):
    response = build_coverage(db_session, NOW)
    assert response.verified_total == 0
    assert response.languages_active == 0
    assert response.nodes == []
    assert response.generated_at == NOW
