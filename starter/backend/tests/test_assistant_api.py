from fastapi.testclient import TestClient
import pytest

from app.db import get_session
from app.main import app
from app.models import User


@pytest.fixture
def assistant_client(db_session):
    user = User(
        provider_subject="assistant-user",
        declared_languages=["en"],
        display_name="Assistant User",
    )
    db_session.add(user)
    db_session.commit()
    db_session.expire_on_commit = False
    app.dependency_overrides[get_session] = lambda: db_session
    with TestClient(app) as client:
        yield client, user
    app.dependency_overrides.clear()


def headers(user):
    return {"X-User-ID": str(user.id), "X-Provider-Subject": user.provider_subject}


def test_assistant_route_returns_allowlisted_navigation(assistant_client):
    client, user = assistant_client

    response = client.post("/assistant", json={"message": "take me to rewards"}, headers=headers(user))

    assert response.status_code == 200
    assert response.json()["intent"] == "NAVIGATE"
    assert response.json()["route"] == "/rewards"
    assert response.json()["provider"] == "deterministic"


def test_assistant_route_requires_persisted_identity(assistant_client):
    client, user = assistant_client

    response = client.post(
        "/api/assistant",
        json={"message": "open impact"},
        headers={"X-User-ID": str(user.id), "X-Provider-Subject": "wrong-subject"},
    )

    assert response.status_code == 401


def test_assistant_route_never_executes_payment_from_chat(assistant_client):
    client, user = assistant_client

    response = client.post(
        "/assistant",
        json={"message": "cash me out now"},
        headers=headers(user),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "PAYMENT_CONFIRMATION_REQUIRED"
    assert body["route"] is None
    assert body["advisory"] is True
