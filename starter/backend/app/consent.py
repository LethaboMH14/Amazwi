from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AuditEvent, ConsentGrant, ConsentScope, User


class ConsentRequiredError(Exception):
    def __init__(self, scope: ConsentScope):
        self.scope = scope
        super().__init__(f"active consent required: {scope.value}")


class ConsentAlreadyRevokedError(Exception):
    def __init__(self, scope: ConsentScope):
        self.scope = scope
        super().__init__(f"consent already revoked: {scope.value}")


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def grant_scopes(
    session: Session,
    user_id: UUID,
    version: str,
    scopes: list[ConsentScope],
    actor_id: UUID,
) -> list[ConsentGrant]:
    session.execute(select(User.id).where(User.id == user_id).with_for_update()).scalar_one()
    grants: list[ConsentGrant] = []
    for scope in dict.fromkeys(scopes):
        grant = session.scalar(
            select(ConsentGrant)
            .where(
                ConsentGrant.user_id == user_id,
                ConsentGrant.scope == scope,
                ConsentGrant.revoked_at.is_(None),
            )
            .with_for_update()
        )
        if grant is None:
            grant = ConsentGrant(
                user_id=user_id,
                version=version,
                scope=scope,
                granted_at=_utcnow(),
            )
            session.add(grant)
            session.flush()
        grants.append(grant)
    return grants


def require_active_scope(session: Session, user_id: UUID, scope: ConsentScope) -> ConsentGrant:
    grant = session.scalar(
        select(ConsentGrant).where(
            ConsentGrant.user_id == user_id,
            ConsentGrant.scope == scope,
            ConsentGrant.revoked_at.is_(None),
        )
    )
    if grant is None:
        raise ConsentRequiredError(scope)
    return grant


def revoke_scope(
    session: Session,
    user_id: UUID,
    scope: ConsentScope,
    actor_id: UUID,
    reason: str,
) -> ConsentGrant:
    grant = session.scalar(
        select(ConsentGrant)
        .where(
            ConsentGrant.user_id == user_id,
            ConsentGrant.scope == scope,
            ConsentGrant.revoked_at.is_(None),
        )
        .with_for_update()
    )
    if grant is None:
        raise ConsentAlreadyRevokedError(scope)
    grant.revoked_at = _utcnow()
    session.add(
        AuditEvent(
            actor_id=actor_id,
            action="CONSENT_REVOKED",
            entity_type="ConsentGrant",
            entity_id=str(grant.id),
            event_metadata=json.dumps({"scope": scope.value, "reason": reason}),
            created_at=_utcnow(),
        )
    )
    session.flush()
    return grant
