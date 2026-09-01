from datetime import datetime, timezone
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db import get_session
from app.identity import AuthenticatedIdentity, get_current_identity
from app.main import app
from app.models import ConsentGrant, User


@pytest.fixture
def users(db_session):
    authenticated = User(
        id=uuid.uuid4(),
        provider_subject="api-authenticated",
        declared_languages=["tn"],
        created_at=datetime.now(timezone.utc),
    )
    other = User(
        id=uuid.uuid4(),
        provider_subject="api-other",
        declared_languages=["tn"],
        created_at=datetime.now(timezone.utc),
    )
    db_session.add_all([authenticated, other])
    db_session.expire_on_commit = False
    db_session.commit()
    return authenticated, other


@pytest.fixture
def api_client(db_session, users):
    authenticated, _ = users

    def override_session():
        yield db_session

    app.dependency_overrides[get_session] = override_session
    app.dependency_overrides[get_current_identity] = lambda: AuthenticatedIdentity(
        user_id=authenticated.id,
        provider_subject=authenticated.provider_subject,
    )
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_consent_api_grants_scopes(api_client):
    response = api_client.post(
        "/consents",
        json={"version": "2026-09-01", "scopes": ["RECORD_PROCESS_ROUND"]},
    )
    assert response.status_code == 201
    assert response.json()[0]["scope"] == "RECORD_PROCESS_ROUND"


def test_consent_api_cannot_impersonate_another_user(api_client, db_session, users):
    authenticated, other = users
    response = api_client.post(
        "/consents",
        json={
            "version": "2026-09-01",
            "scopes": ["RECORD_PROCESS_ROUND"],
            "user_id": str(other.id),
        },
    )
    assert response.status_code == 201
    assert db_session.scalar(
        select(ConsentGrant).where(ConsentGrant.user_id == authenticated.id)
    )
    assert db_session.scalar(
        select(ConsentGrant).where(ConsentGrant.user_id == other.id)
    ) is None


def test_consent_api_rejects_mismatched_provider_subject(db_session, users):
    authenticated, other = users

    app.dependency_overrides[get_session] = lambda: db_session
    app.dependency_overrides[get_current_identity] = lambda: AuthenticatedIdentity(
        user_id=authenticated.id,
        provider_subject=other.provider_subject,
    )
    try:
        with TestClient(app) as client:
            response = client.post(
                "/consents",
                json={"version": "2026-09-01", "scopes": ["RECORD_PROCESS_ROUND"]},
            )
        assert response.status_code == 401
        assert response.json()["detail"]["code"] == "AUTHENTICATION_REQUIRED"
    finally:
        app.dependency_overrides.clear()


def test_consent_api_requires_identity():
    with TestClient(app) as client:
        response = client.post(
            "/consents",
            json={"version": "2026-09-01", "scopes": ["RECORD_PROCESS_ROUND"]},
        )
    assert response.status_code == 401


def test_consent_api_lists_and_revokes_a_scope(api_client):
    granted = api_client.post(
        "/consents",
        json={"version": "2026-09-01", "scopes": ["ASSIGNED_VERIFIER_PLAYBACK"]},
    )
    assert granted.status_code == 201

    listed = api_client.get("/consents/me")
    assert listed.status_code == 200
    assert listed.json()[0]["scope"] == "ASSIGNED_VERIFIER_PLAYBACK"

    revoked = api_client.post("/consents/ASSIGNED_VERIFIER_PLAYBACK/revoke")
    assert revoked.status_code == 200
    assert revoked.json()["revoked_at"] is not None

    repeated = api_client.post("/consents/ASSIGNED_VERIFIER_PLAYBACK/revoke")
    assert repeated.status_code == 409
    assert repeated.json()["detail"]["code"] == "CONSENT_ALREADY_REVOKED"
