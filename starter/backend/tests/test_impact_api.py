"""GET /impact -- the aggregate Coverage Constellation endpoint.

Asserts the wire shape a browser actually receives, including that the
serialised payload carries no personal, per-contribution, geographic or
audio field anywhere in it (checked against the raw response text, not
only the parsed top level).
"""
from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient

from app.db import get_session
from app.main import app
from app.models import (
    Campaign,
    Card,
    Contribution,
    ContributionState,
    EligibilityDecision,
    User,
)


@pytest.fixture
def impact_client(db_session):
    app.dependency_overrides[get_session] = lambda: db_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _seed(db_session, *, language: str, campaign_name: str, count: int) -> None:
    campaign = Campaign(
        name=campaign_name, language=language, budget_cents=1000, funded_cents=1000, committed_cents=0
    )
    db_session.add(campaign)
    db_session.flush()
    card = Card(
        language=language,
        target="kgomo",
        blocked_words=["a", "b", "c", "d"],
        accepted_answers=["kgomo", "dikgomo"],
        distractors=["x", "y", "z"],
        campaign_id=campaign.id,
    )
    db_session.add(card)
    db_session.flush()
    for _ in range(count):
        speaker = User(provider_subject=f"msisdn:{uuid.uuid4().hex[:10]}", declared_languages=[language])
        db_session.add(speaker)
        db_session.flush()
        contribution = Contribution(
            speaker_id=speaker.id,
            card_id=card.id,
            declared_language=language,
            state=ContributionState.CORPUS_ELIGIBLE,
        )
        db_session.add(contribution)
        db_session.flush()
        db_session.add(
            EligibilityDecision(
                contribution_id=contribution.id,
                understood=True,
                corpus_eligible=True,
                reason="PEER_VERIFIED",
                consent_version="2026-09-01",
            )
        )
    db_session.expire_on_commit = False
    db_session.commit()


def test_impact_endpoint_returns_bands_and_no_identifiers(impact_client, db_session):
    _seed(db_session, language="zu", campaign_name="support", count=6)
    response = impact_client.get("/impact")
    assert response.status_code == 200
    body = response.json()
    assert body["verified_total"] == 6
    assert body["languages_active"] == 1
    assert body["geography_available"] is False
    assert len(body["nodes"]) == 1
    node = body["nodes"][0]
    assert node["verified_count_band"] == "5-19"
    assert node["province_code"] is None
    assert node["model_gap_percent"] is None
    for forbidden in ("speaker_id", "user_id", "contribution_id", "audio_key", "latitude", "longitude", "transcript"):
        assert forbidden not in response.text


def test_impact_endpoint_suppresses_small_cells_on_the_wire(impact_client, db_session):
    _seed(db_session, language="zu", campaign_name="support", count=4)
    body = impact_client.get("/impact").json()
    assert body["nodes"] == []
    assert body["suppressed_cell_count"] == 1


def test_impact_endpoint_is_also_served_under_the_api_prefix(impact_client, db_session):
    _seed(db_session, language="tn", campaign_name="support", count=5)
    prefixed = impact_client.get("/api/impact")
    assert prefixed.status_code == 200
    # generated_at is a real clock read and differs per call, so compare
    # the aggregate content rather than the whole envelope.
    assert prefixed.json()["nodes"] == impact_client.get("/impact").json()["nodes"]


def test_impact_endpoint_on_empty_database(impact_client):
    body = impact_client.get("/impact").json()
    assert body["verified_total"] == 0
    assert body["nodes"] == []
