from datetime import datetime, timezone
import hashlib
import uuid

import pytest
from fastapi.testclient import TestClient

from app.audio import get_audio_store
from app.db import get_session
from app.identity import AuthenticatedIdentity, get_current_identity
from app.main import app
from app.models import Campaign, CampaignRewardRule, Card, ConsentGrant, ConsentScope, User


@pytest.fixture
def audio_api_context(db_session, tmp_path):
    now = datetime.now(timezone.utc)
    speaker = User(id=uuid.uuid4(), provider_subject="audio-api-speaker", declared_languages=["tn"], age_confirmed_at=now, created_at=now)
    campaign = Campaign(id=uuid.uuid4(), name="Audio API", language="tn", budget_cents=1000, funded_cents=1000, committed_cents=0, provider_mode="DEMO_PROVIDER")
    rule = CampaignRewardRule(id=uuid.uuid4(), campaign_id=campaign.id, version="v1", contribution_reward_cents=100, effective_from=now)
    card = Card(id=uuid.uuid4(), language="tn", target="kgomo", blocked_words=["a", "b", "c", "d"], accepted_answers=["kgomo", "kgomo"], distractors=["x", "y", "z"], campaign_id=campaign.id, active=True)
    db_session.add_all([speaker, campaign, rule, card])
    db_session.flush()
    db_session.add(ConsentGrant(user_id=speaker.id, version="2026-09-01", scope=ConsentScope.RECORD_PROCESS_ROUND))
    db_session.expire_on_commit = False
    db_session.commit()
    store = __import__("app.storage", fromlist=["LocalAudioObjectStore"]).LocalAudioObjectStore(tmp_path, secret=b"api-audio-secret")
    return speaker, card, store


@pytest.fixture
def audio_client(db_session, audio_api_context):
    speaker, _, store = audio_api_context

    def override_session():
        yield db_session

    app.dependency_overrides[get_session] = override_session
    app.dependency_overrides[get_current_identity] = lambda: AuthenticatedIdentity(speaker.id, speaker.provider_subject)
    app.dependency_overrides[get_audio_store] = lambda: store
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_contribution_api_requires_round_consent(db_session, audio_api_context):
    speaker, card, _ = audio_api_context
    db_session.query(ConsentGrant).filter(ConsentGrant.user_id == speaker.id).delete()
    db_session.commit()
    app.dependency_overrides[get_session] = lambda: db_session
    app.dependency_overrides[get_current_identity] = lambda: AuthenticatedIdentity(speaker.id, speaker.provider_subject)
    with TestClient(app) as client:
        response = client.post("/contributions", json={"card_id": str(card.id)})
    app.dependency_overrides.clear()
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "CONSENT_REQUIRED"


def test_audio_api_upload_and_finalise(audio_client, audio_api_context, db_session):
    _, card, _ = audio_api_context
    created = audio_client.post("/contributions", json={"card_id": str(card.id)})
    assert created.status_code == 201
    contribution_id = created.json()["id"]
    upload = audio_client.post(f"/contributions/{contribution_id}/audio/uploads")
    assert upload.status_code == 200
    audio_id = upload.json()["audio_object_id"]
    body = b"voice"
    uploaded = audio_client.put(f"/private-audio/uploads/{audio_id}", content=body)
    assert uploaded.status_code == 200
    finalised = audio_client.post(
        f"/contributions/{contribution_id}/audio/finalise",
        json={
            "sha256": hashlib.sha256(body).hexdigest(),
            "mime_type": "audio/webm",
            "codec": "opus",
            "duration_ms": 1000,
            "byte_length": len(body),
        },
    )
    assert finalised.status_code == 200, finalised.text
    assert finalised.json()["state"] == "AVAILABLE"
    playback = audio_client.post(f"/contributions/{contribution_id}/playback")
    assert playback.status_code == 200
    playback_path = playback.json()["url"]
    assert audio_client.get(playback_path).status_code == 200
    speaker, _, _ = audio_api_context
    db_session.query(ConsentGrant).filter(ConsentGrant.user_id == speaker.id).delete()
    db_session.commit()
    assert audio_client.get(playback_path).status_code == 403
