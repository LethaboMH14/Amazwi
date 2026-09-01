from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.models import ConsentScope


class ConsentGrantRequest(BaseModel):
    version: str = Field(min_length=1, max_length=64)
    scopes: list[ConsentScope] = Field(min_length=1)


class ConsentState(BaseModel):
    scope: ConsentScope
    version: str
    granted_at: datetime
    revoked_at: datetime | None
