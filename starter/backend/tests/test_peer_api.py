from datetime import datetime, timezone
import uuid

import pytest
from fastapi.testclient import TestClient

from app.cohorts import select_next_verifier
from app.db import get_session
from app.identity import AuthenticatedIdentity, get_current_identity
from app.main import app
from app.models import Campaign, CampaignRewardRule, Card, ConsentGrant, ConsentScope, Contribution, ContributionState, User, VerifierQualification


@pytest.fixture
def peer_context(db_session):
    now = datetime.now(timezone.utc)
    speaker = User(id=uuid.uuid4(), provider_subject="peer-speaker", declared_languages=["tn"], created_at=now)
    verifier = User(id=uuid.uuid4(), provider_subject="peer-verifier", declared_languages=["tn"], age_confirmed_at=now, created_at=now)
    campaign = Campaign(id=uuid.uuid4(), name="Peer", language="tn", budget_cents=1000, funded_cents=1000, committed_cents=0, provider_mode="DEMO_PROVIDER")
    rule = CampaignRewardRule(id=uuid.uuid4(), campaign_id=campaign.id, version="v1", contribution_reward_cents=100, effective_from=now)
    card = Card(id=uuid.uuid4(), language="tn", target="kgomo", blocked_words=["a", "b", "c", "d"], accepted_answers=["kgomo", "kgomo"], distractors=["x", "y", "z"], campaign_id=campaign.id, active=True)
    contribution = Contribution(id=uuid.uuid4(), speaker_id=speaker.id, card_id=card.id, declared_language="tn", state=ContributionState.OPEN, reward_rule_id=rule.id, created_at=now)
    db_session.add_all([speaker, verifier, campaign])
    db_session.flush()
    db_session.add(rule)
    db_session.flush()
    db_session.add(card)
    db_session.flush()
    db_session.add(contribution)
    db_session.flush()
    db_session.add_all([
        ConsentGrant(user_id=speaker.id, version="v1", scope=ConsentScope.ASSIGNED_VERIFIER_PLAYBACK),
        VerifierQualification(user_id=verifier.id, language="tn", qualified_at=now, reviewed_by=speaker.id),
    ])
    db_session.expire_on_commit = False
    db_session.commit()
    return speaker, verifier, contribution


@pytest.fixture
def peer_client(db_session, peer_context):
    _, verifier, _ = peer_context
    app.dependency_overrides[get_session] = lambda: db_session
    app.dependency_overrides[get_current_identity] = lambda: AuthenticatedIdentity(verifier.id, verifier.provider_subject)
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_peer_api_assigns_only_authenticated_qualified_verifier(peer_client, peer_context):
    _, _, contribution = peer_context
    response = peer_client.get(f"/assignments/next?contribution_id={contribution.id}&language=tn")
    assert response.status_code == 200
    assert response.json()["contribution_id"] == str(contribution.id)


def test_peer_api_answer_rejects_duplicate_and_records_exact_match(peer_client, peer_context, db_session):
    _, _, contribution = peer_context
    assignment = peer_client.get(f"/assignments/next?contribution_id={contribution.id}&language=tn").json()
    answer = peer_client.post(f"/assignments/{assignment['id']}/answer", json={"answer_text": " KGOMO ", "violation_vote": False, "user_id": str(uuid.uuid4())})
    assert answer.status_code == 200
    repeated = peer_client.post(f"/assignments/{assignment['id']}/answer", json={"answer_text": "kgomo"})
    assert repeated.status_code == 409


def test_peer_result_is_pending_until_authoritative_decision(peer_context, db_session):
    speaker, _, contribution = peer_context
    app.dependency_overrides[get_session] = lambda: db_session
    app.dependency_overrides[get_current_identity] = lambda: AuthenticatedIdentity(speaker.id, speaker.provider_subject)
    with TestClient(app) as client:
        response = client.get(f"/contributions/{contribution.id}/result")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["status"] == "PENDING"
