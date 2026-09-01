from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from fastapi import Header, HTTPException, status


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
