"""Seed realistic demo *activity* by driving the real pipeline.

`seed_demo.py` creates the static world -- cards, campaigns, users,
consents. This module creates the history that makes a dashboard worth
looking at: contributions, peer answers, resolver decisions and rewards.

It does NOT hand-write outcomes. Every eligibility decision and every
reward row here is produced by `app.resolver.resolve_from_persisted_state`
reading two real peer answers, exactly as a live round would. That is the
point: the leaderboard a judge sees is the resolver's own output, so the
refusal branch (peers disagreed -> nobody is paid) appears on the
dashboard as naturally as the success branch.

Deterministic and idempotent: every id is uuid5 off a fixed name, so
re-running produces the same world rather than piling up new rows.

Demo-only, guarded by AMAZWI_ALLOW_DEMO_SEED -- mirroring the reset guard
in seed_demo.py. This must never be reachable from a production process.
"""
from __future__ import annotations

import os
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.models import (
    Assignment,
    AssignmentMode,
    AudioObject,
    AudioObjectState,
    Campaign,
    CampaignRewardRule,
    Card,
    ConsentGrant,
    ConsentScope,
    Contribution,
    ContributionState,
    User,
)
from app.matching import is_correct, normalise_answer
from app.resolver import resolve_from_persisted_state

SEED_GUARD_ENV = "AMAZWI_ALLOW_DEMO_SEED"
NAMESPACE = uuid.UUID("6f9619ff-8b86-d011-b42d-00cf4fc964ff")

# Extra demo contributors, so a leaderboard has more than one name on it.
# They are speakers only -- the two seeded verifiers per language remain
# the only qualified peers, which keeps "a speaker never verifies their
# own clip" intact without inventing new verifier qualifications.
EXTRA_CONTRIBUTORS: tuple[tuple[str, str], ...] = (
    ("Nomsa K.", "zu"),
    ("Sipho M.", "zu"),
    ("Ayanda D.", "zu"),
    ("Thandeka N.", "zu"),
    ("Kagiso P.", "tn"),
    ("Lerato S.", "tn"),
    ("Tumelo R.", "tn"),
)

# (language, card index, contributor index, peers_agree).
# contributor index -1 means the original seeded demo speaker.
# peers_agree=False is a genuine disagreement: the second peer types a
# real distractor, and the resolver refuses to pay. That branch is the
# one worth showing a judge, so it is deliberately in the fixture.
SCRIPT: tuple[tuple[str, int, int, bool], ...] = (
    ("zu", 0, -1, True),
    ("zu", 1, -1, True),
    ("zu", 2, -1, False),
    ("zu", 0, 0, True),
    ("zu", 1, 0, True),
    ("zu", 2, 0, True),
    ("zu", 3, 0, True),
    ("zu", 4, 0, True),
    ("zu", 0, 1, True),
    ("zu", 1, 1, True),
    ("zu", 2, 1, True),
    ("zu", 3, 1, False),
    ("zu", 0, 2, True),
    ("zu", 1, 2, True),
    ("zu", 0, 3, True),
    ("tn", 0, -1, True),
    ("tn", 1, -1, True),
    ("tn", 2, -1, False),
    ("tn", 0, 4, True),
    ("tn", 1, 4, True),
    ("tn", 2, 4, True),
    ("tn", 3, 4, True),
    ("tn", 0, 5, True),
    ("tn", 1, 5, True),
    ("tn", 0, 6, True),
)


def _uid(*parts: str) -> uuid.UUID:
    return uuid.uuid5(NAMESPACE, "|".join(parts))


def _user_by_subject(session: Session, subject: str) -> User:
    user = session.scalar(select(User).where(User.provider_subject == subject))
    if user is None:
        raise RuntimeError(f"run seed_demo first: missing user {subject}")
    return user


def _peers_for(session: Session, language: str) -> list[User]:
    """The two seeded, still-qualified verifiers for this language."""
    return [
        _user_by_subject(session, f"demo-verifier-{language}-1"),
        _user_by_subject(session, f"demo-verifier-{language}-2"),
    ]


def _ensure_contributors(session: Session, now: datetime) -> list[User]:
    """Create the extra demo contributors, idempotently."""
    out: list[User] = []
    for name, language in EXTRA_CONTRIBUTORS:
        slug = name.lower().replace(" ", "-").replace(".", "")
        subject = f"demo-contributor-{slug}"
        user = session.scalar(select(User).where(User.provider_subject == subject))
        if user is None:
            user = User(
                id=_uid("user", subject),
                provider_subject=subject,
                declared_languages=[language],
                display_name=name,
            )
            session.add(user)
            session.flush()
        # A contributor who never consented is correctly refused by the
        # resolver, so grant the same scope onboarding grants. Without
        # this the fixture silently produces 'consent not active' for
        # every clip -- which is the gate working, not a bug to route
        # around, so it is granted explicitly rather than bypassed.
        granted = {
            g.scope
            for g in session.scalars(
                select(ConsentGrant).where(
                    ConsentGrant.user_id == user.id,
                    ConsentGrant.revoked_at.is_(None),
                )
            ).all()
        }
        for scope in (
            ConsentScope.RECORD_PROCESS_ROUND,
            ConsentScope.ASSIGNED_VERIFIER_PLAYBACK,
        ):
            if scope not in granted:
                session.add(
                    ConsentGrant(
                        user_id=user.id,
                        version="2026-09-01",
                        scope=scope,
                        granted_at=now,
                    )
                )
        session.flush()
        out.append(user)
    return out


def _active_reward_rule(session: Session, language: str) -> CampaignRewardRule | None:
    """The rule a real contribution snapshots at creation time."""
    campaign = session.scalar(
        select(Campaign).where(Campaign.language == language).order_by(Campaign.name)
    )
    if campaign is None:
        return None
    return session.scalar(
        select(CampaignRewardRule)
        .where(
            CampaignRewardRule.campaign_id == campaign.id,
            CampaignRewardRule.retired_at.is_(None),
        )
        .order_by(CampaignRewardRule.effective_from.desc())
    )


def seed_activity(session: Session, *, now: datetime | None = None) -> dict[str, int]:
    now = now or datetime.now(timezone.utc)
    created = {"contributions": 0, "resolved": 0, "unresolved": 0, "skipped": 0}
    contributors = _ensure_contributors(session, now)

    for step, (language, card_index, contributor_index, agree) in enumerate(SCRIPT):
        cards = list(
            session.scalars(
                select(Card).where(Card.language == language).order_by(Card.target.asc())
            ).all()
        )
        if card_index >= len(cards):
            created["skipped"] += 1
            continue
        card = cards[card_index]

        speaker = (
            _user_by_subject(session, f"demo-speaker-{language}")
            if contributor_index < 0
            else contributors[contributor_index]
        )
        peers = [p for p in _peers_for(session, language) if p.id != speaker.id]
        if len(peers) < 2:
            created["skipped"] += 1
            continue

        contribution_id = _uid("contribution", language, str(card_index), str(speaker.id))
        if session.get(Contribution, contribution_id) is not None:
            created["skipped"] += 1
            continue

        rule = _active_reward_rule(session, language)
        if rule is None:
            created["skipped"] += 1
            continue

        created_at = now - timedelta(hours=len(SCRIPT) - step)
        session.add(
            Contribution(
                id=contribution_id,
                speaker_id=speaker.id,
                card_id=card.id,
                declared_language=language,
                state=ContributionState.OPEN,
                audio_key=f"demo/{contribution_id}",
                duration_ms=8_000,
                created_at=created_at,
                # Snapshotted at creation, exactly as the real route does:
                # the reward is fixed by the rule in force when the clip
                # was recorded, never the rule at payout time.
                reward_rule_id=rule.id,
            )
        )
        session.flush()

        session.add(
            AudioObject(
                id=_uid("audio", str(contribution_id)),
                contribution_id=contribution_id,
                object_key=f"demo/{contribution_id}",
                state=AudioObjectState.AVAILABLE,
                sha256="0" * 64,
                byte_length=8_000,
                mime_type="audio/webm",
                codec="opus",
                duration_ms=8_000,
            )
        )

        accepted = card.accepted_answers[0]
        # A disagreement types a real distractor, not a nonsense string --
        # that is what "I honestly heard something else" looks like, and
        # it is exactly what the resolver must refuse to pay for.
        answers = [accepted, accepted] if agree else [accepted, card.distractors[0]]

        for peer, answer in zip(peers[:2], answers):
            session.add(
                Assignment(
                    id=_uid("assignment", str(contribution_id), str(peer.id)),
                    contribution_id=contribution_id,
                    verifier_id=peer.id,
                    mode=AssignmentMode.PROFICIENT_VERIFIER,
                    answer_text=answer,
                    # Use the real matcher, exactly as routes/assignments.py
                    # does. Setting `matched` by hand here would make this
                    # fixture assert an outcome instead of deriving one --
                    # and the resolver reads `matched`, not the raw text.
                    answer_normalised=normalise_answer(answer),
                    matched=is_correct(answer, card.accepted_answers),
                    answered_at=created_at + timedelta(minutes=5),
                )
            )
        session.flush()
        created["contributions"] += 1

        # The real resolver decides. Nothing here sets an outcome.
        try:
            resolve_from_persisted_state(session, contribution_id)
            created["resolved"] += 1
        except Exception as exc:  # noqa: BLE001 -- reported, never swallowed
            created["unresolved"] += 1
            print(f"  ! {language} card {card_index}: {type(exc).__name__}: {exc}")

    session.commit()
    return created


def main() -> int:
    if os.environ.get(SEED_GUARD_ENV, "").lower() != "true":
        raise SystemExit(
            f"refusing to seed demo activity: set {SEED_GUARD_ENV}=true to confirm"
        )
    url = os.environ.get("AMAZWI_DATABASE_URL")
    if not url:
        raise SystemExit("AMAZWI_DATABASE_URL is required")
    engine = create_engine(url)
    with Session(engine) as session:
        result = seed_activity(session)
    print(
        "Activity seeded: "
        f"{result['contributions']} contributions, "
        f"{result['resolved']} resolved, "
        f"{result['unresolved']} unresolved, "
        f"{result['skipped']} skipped (already present)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
