from __future__ import annotations

import random
import secrets
import uuid

from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.consent import require_active_scope
from app.models import (
    Assignment,
    ConsentScope,
    Contribution,
    User,
    VerifierQualification,
)


def select_next_verifier(
    session: Session,
    contribution_id: uuid.UUID,
    language: str,
    rng: random.Random | secrets.SystemRandom,
    candidate_id: uuid.UUID | None = None,
) -> User | None:
    contribution = session.get(Contribution, contribution_id)
    if contribution is None:
        return None
    try:
        require_active_scope(session, contribution.speaker_id, ConsentScope.ASSIGNED_VERIFIER_PLAYBACK)
    except Exception:
        return None
    already_assigned = exists(
        select(Assignment.id).where(
            Assignment.contribution_id == contribution_id,
            Assignment.verifier_id == User.id,
        )
    )
    candidates = session.scalars(
        select(User)
        .join(VerifierQualification, VerifierQualification.user_id == User.id)
        .where(
            User.id != contribution.speaker_id,
            User.id == candidate_id if candidate_id is not None else True,
            User.age_confirmed_at.is_not(None),
            VerifierQualification.language == language,
            VerifierQualification.revoked_at.is_(None),
            ~already_assigned,
        )
        .order_by(User.id)
    ).all()
    return rng.choice(candidates) if candidates else None
