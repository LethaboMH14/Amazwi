"""Read-only aggregate coverage endpoint.

Deliberately unauthenticated: every field it returns is an aggregate
that has already passed `app.impact`'s minimum-cell-size suppression,
and no personal, per-contribution, geographic or audio field is present.
It is a read-only view over published totals, not a user resource.
"""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api_types import ImpactResponse
from app.db import get_session
from app.impact import build_coverage

router = APIRouter(tags=["impact"])


@router.get("/impact", response_model=ImpactResponse)
@router.get("/api/impact", response_model=ImpactResponse, include_in_schema=False)
def impact(session: Session = Depends(get_session)) -> ImpactResponse:
    return build_coverage(session, datetime.now(timezone.utc))
