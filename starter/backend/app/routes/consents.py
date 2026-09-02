from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Iterator

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api_types import ConsentGrantRequest, ConsentState
from app.consent import (
    ConsentAlreadyRevokedError,
    grant_scopes,
    revoke_scope,
)
from app.db import get_session
from app.identity import AuthenticatedIdentity, get_current_identity, require_identity_user
from app.models import ConsentGrant, ConsentScope, User


router = APIRouter(prefix="/consents", tags=["consent"])


def _state(grant: ConsentGrant) -> ConsentState:
    return ConsentState(
        scope=grant.scope,
        version=grant.version,
        granted_at=grant.granted_at,
        revoked_at=grant.revoked_at,
    )


def _require_user(session: Session, identity: AuthenticatedIdentity) -> User:
    return require_identity_user(session, identity)


@contextmanager
def _transaction(session: Session) -> Iterator[None]:
    transaction = session.begin_nested() if session.in_transaction() else session.begin()
    with transaction:
        yield


@router.post("", response_model=list[ConsentState], status_code=status.HTTP_201_CREATED)
def create_consent(
    request: ConsentGrantRequest,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
) -> list[ConsentState]:
    with _transaction(session):
        _require_user(session, identity)
        grants = grant_scopes(
            session,
            identity.user_id,
            request.version,
            request.scopes,
            identity.user_id,
        )
    session.commit()
    return [_state(grant) for grant in grants]


@router.get("/me", response_model=list[ConsentState])
def get_my_consents(
    session: Session = Depends(get_session),
    identity: AuthenticatedIdentity = Depends(get_current_identity),
) -> list[ConsentState]:
    _require_user(session, identity)
    grants = session.scalars(
        select(ConsentGrant)
        .where(ConsentGrant.user_id == identity.user_id)
        .order_by(ConsentGrant.granted_at)
    ).all()
    return [_state(grant) for grant in grants]


@router.post("/{scope}/revoke", response_model=ConsentState)
def revoke_consent(
    scope: ConsentScope,
    reason: str = "user request",
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
) -> ConsentState:
    try:
        with _transaction(session):
            _require_user(session, identity)
            grant = revoke_scope(
                session,
                identity.user_id,
                scope,
                identity.user_id,
                reason,
            )
        session.commit()
    except ConsentAlreadyRevokedError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "CONSENT_ALREADY_REVOKED", "scope": exc.scope.value},
        ) from exc
    return _state(grant)
