from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from fastapi import Header, HTTPException, status
from sqlalchemy.orm import Session

from app.models import User


@dataclass(frozen=True)
class AuthenticatedIdentity:
    user_id: UUID
    provider_subject: str


def get_current_identity(
    x_user_id: str | None = Header(default=None),
    x_provider_subject: str | None = Header(default=None),
) -> AuthenticatedIdentity:
    if not x_user_id or not x_provider_subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "AUTHENTICATION_REQUIRED"},
        )
    try:
        user_id = UUID(x_user_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "AUTHENTICATION_REQUIRED"},
        ) from exc
    return AuthenticatedIdentity(user_id=user_id, provider_subject=x_provider_subject)


def require_identity_user(session: Session, identity: AuthenticatedIdentity) -> User:
    """Resolve the header identity to its persisted provider subject.

    The development header adapter is intentionally small, but it must not
    allow a caller to pair another user's UUID with an arbitrary subject.
    Production host authentication can replace the adapter while retaining
    this invariant at every route boundary.
    """
    user = session.get(User, identity.user_id)
    if user is None or user.provider_subject != identity.provider_subject:
        raise HTTPException(status_code=401, detail={"code": "AUTHENTICATION_REQUIRED"})
    return user
