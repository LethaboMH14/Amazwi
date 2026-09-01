from datetime import datetime, timezone
import uuid

import pytest
from sqlalchemy import select

from app.consent import ConsentRequiredError, grant_scopes, require_active_scope, revoke_scope
from app.models import AuditEvent, ConsentGrant, ConsentScope, User


@pytest.fixture
def user(db_session):
    user = User(
        id=uuid.uuid4(),
        provider_subject="consent-user",
        declared_languages=["tn"],
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_grant_scopes_is_idempotent(db_session, user):
    first = grant_scopes(
        db_session,
        user.id,
        "2026-09-01",
        [ConsentScope.RECORD_PROCESS_ROUND],
        user.id,
    )
    second = grant_scopes(
        db_session,
        user.id,
        "2026-09-01",
        [ConsentScope.RECORD_PROCESS_ROUND],
        user.id,
    )
    assert [grant.id for grant in second] == [first[0].id]
    assert db_session.scalar(select(ConsentGrant).where(ConsentGrant.user_id == user.id).where(ConsentGrant.revoked_at.is_(None)))


def test_training_opt_out_does_not_remove_round_scope(db_session, user):
    grant_scopes(db_session, user.id, "2026-09-01", [ConsentScope.RECORD_PROCESS_ROUND], user.id)
    assert require_active_scope(db_session, user.id, ConsentScope.RECORD_PROCESS_ROUND)
    with pytest.raises(ConsentRequiredError):
        require_active_scope(db_session, user.id, ConsentScope.RETAIN_MODEL_DEVELOPMENT)


def test_revocation_preserves_audit_and_blocks_future_use(db_session, user):
    grant_scopes(db_session, user.id, "2026-09-01", [ConsentScope.ASSIGNED_VERIFIER_PLAYBACK], user.id)
    revoked = revoke_scope(
        db_session,
        user.id,
        ConsentScope.ASSIGNED_VERIFIER_PLAYBACK,
        user.id,
        "user request",
    )
    assert revoked.revoked_at is not None
    assert db_session.scalar(select(AuditEvent).where(AuditEvent.action == "CONSENT_REVOKED"))
    with pytest.raises(ConsentRequiredError):
        require_active_scope(db_session, user.id, ConsentScope.ASSIGNED_VERIFIER_PLAYBACK)
