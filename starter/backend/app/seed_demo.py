"""Deterministic demo seed: load real card content, fund campaigns, create
demo users. Idempotent -- safe to re-run between takes (the "never cut"
deterministic-reset requirement in 05_BUILD.md).

Usage:
    python -m app.seed_demo
    AMAZWI_ALLOW_DEMO_RESET=true python -m app.seed_demo --reset

Loads 05_amazwi/content/cards_isizulu.json and cards_setswana.json (repo
root, three levels up from this file) into real Card rows against
whatever AMAZWI_DATABASE_URL / AMAZWI_TEST_DATABASE_URL points at.

Not wired into any HTTP route on purpose -- run it explicitly before a
demo, not as an app-boot side effect. Reset is guarded, refuses databases
containing non-demo campaigns or exported contribution rows, and remains
structurally unavailable over HTTP.
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import Session

from app.db import get_engine
from app.models import (
    Campaign,
    CampaignRewardRule,
    Card,
    Assignment,
    AudioObject,
    AuditEvent,
    Contribution,
    ConsentGrant,
    ConsentScope,
    CouncilOutput,
    DatasetExportRow,
    EligibilityDecision,
    OutboxEvent,
    PaymentAttempt,
    Receipt,
    RewardEvent,
    User,
    VerifierQualification,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
CONTENT_DIR = REPO_ROOT / "05_amazwi" / "content"

# Deterministic UUIDs (uuid5 off a fixed namespace + stable name) so the seed
# is idempotent across runs and every device on the LAN can hard-code the
# same demo user/campaign ids if needed -- not because the ids are secret.
_NS = uuid5(NAMESPACE_URL, "amazwi.demo")


def _id(name: str):
    return uuid5(_NS, name)


LANGUAGES = {
    "zu": {"file": "cards_isizulu.json", "campaign_name": "AMAZWI Demo — isiZulu"},
    "tn": {"file": "cards_setswana.json", "campaign_name": "AMAZWI Demo — Setswana"},
}

REWARD_CENTS = 200  # R2.00 per contribution, matches the published rate in the plan
RESET_GUARD_ENV = "AMAZWI_ALLOW_DEMO_RESET"


def _now():
    return datetime.now(timezone.utc)


def _load_cards(filename: str) -> list[dict]:
    raw = json.loads((CONTENT_DIR / filename).read_text(encoding="utf-8"))
    return raw["hero_8"]


def _get_or_create_user(session: Session, key: str, *, provider_subject: str, declared_languages: list[str], display_name: str) -> User:
    user_id = _id(key)
    user = session.get(User, user_id)
    if user is not None:
        return user
    user = User(
        id=user_id,
        provider_subject=provider_subject,
        declared_languages=declared_languages,
        age_confirmed_at=_now(),
        principal_kind="HUMAN",
        roles=[],
        display_name=display_name,
    )
    session.add(user)
    session.flush()
    return user


def _grant_consent(session: Session, user: User, scopes: list[ConsentScope]) -> None:
    existing = {g.scope for g in session.query(ConsentGrant).filter_by(user_id=user.id, revoked_at=None)}
    for scope in scopes:
        if scope in existing:
            continue
        session.add(ConsentGrant(user_id=user.id, version="2026-09-01", scope=scope, granted_at=_now()))


def _get_or_create_campaign(session: Session, key: str, *, name: str, language: str) -> Campaign:
    campaign_id = _id(key)
    campaign = session.get(Campaign, campaign_id)
    if campaign is not None:
        return campaign
    campaign = Campaign(
        id=campaign_id,
        name=name,
        language=language,
        budget_cents=100_000,  # R1,000 demo ceiling -- comfortably above anything a live demo will spend
        funded_cents=100_000,
        committed_cents=0,
        provider_mode="DEMO_PROVIDER",
    )
    session.add(campaign)
    session.flush()

    rule = session.query(CampaignRewardRule).filter_by(campaign_id=campaign.id, retired_at=None).one_or_none()
    if rule is None:
        session.add(
            CampaignRewardRule(
                campaign_id=campaign.id,
                version="1",
                contribution_reward_cents=REWARD_CENTS,
                effective_from=_now(),
            )
        )
    return campaign


def _upsert_card(session: Session, campaign: Campaign, raw: dict) -> None:
    card_id = _id(f"card:{raw['id']}")
    card = session.get(Card, card_id)
    if card is not None:
        # Content may have been re-reviewed since the last seed run --
        # keep the DB in sync with the JSON, which is the source of truth.
        card.target = raw["target"]
        card.blocked_words = raw["blocked_words"]
        card.accepted_answers = raw["accepted_answers"]
        card.distractors = raw["distractors"]
        card.active = raw.get("active", True)
        return
    session.add(
        Card(
            id=card_id,
            language=raw["language"],
            target=raw["target"],
            blocked_words=raw["blocked_words"],
            accepted_answers=raw["accepted_answers"],
            distractors=raw["distractors"],
            campaign_id=campaign.id,
            active=raw.get("active", True),
        )
    )


def _reset_demo_state(session: Session) -> None:
    """Return a demo-only database to its seeded, pre-take baseline.

    This is deliberately CLI-only and requires an explicit environment guard.
    It refuses mixed/non-demo campaign databases and preserves seeded content,
    identities, consents, qualifications, campaigns and reward rules.
    """
    if os.environ.get(RESET_GUARD_ENV, "").lower() != "true":
        raise RuntimeError(f"demo reset requires {RESET_GUARD_ENV}=true")

    non_demo_campaigns = session.scalar(
        select(func.count()).select_from(Campaign).where(Campaign.provider_mode != "DEMO_PROVIDER")
    )
    if non_demo_campaigns:
        raise RuntimeError("demo reset refused: non-demo campaigns are present")

    exported_rows = session.scalar(
        select(func.count()).select_from(DatasetExportRow).where(DatasetExportRow.contribution_id.is_not(None))
    )
    if exported_rows:
        raise RuntimeError("demo reset refused: dataset export rows reference run state")

    audio_keys = session.scalars(select(AudioObject.object_key)).all()
    audio_root = Path(os.environ.get("AMAZWI_PRIVATE_AUDIO_ROOT") or ".private_audio")
    for object_key in audio_keys:
        audio_path = audio_root / object_key
        if audio_path.is_file():
            audio_path.unlink()

    # Delete dependants before their parent contribution. Generic outbox/audit
    # rows are transient demo evidence and must not drift between judge takes.
    for model in (
        CouncilOutput,
        OutboxEvent,
        Receipt,
        RewardEvent,
        EligibilityDecision,
        Assignment,
        AudioObject,
        PaymentAttempt,
        AuditEvent,
        Contribution,
    ):
        session.execute(delete(model))
    session.execute(update(Campaign).values(committed_cents=0))


def seed(*, reset: bool = False) -> None:
    engine = get_engine()
    with Session(engine) as session:
        if reset:
            _reset_demo_state(session)
        for lang_code, meta in LANGUAGES.items():
            campaign = _get_or_create_campaign(session, f"campaign:{lang_code}", name=meta["campaign_name"], language=lang_code)

            speaker = _get_or_create_user(
                session, f"speaker:{lang_code}",
                provider_subject=f"demo-speaker-{lang_code}",
                declared_languages=[lang_code],
                display_name=f"Demo Speaker ({lang_code})",
            )
            _grant_consent(session, speaker, [ConsentScope.RECORD_PROCESS_ROUND, ConsentScope.ASSIGNED_VERIFIER_PLAYBACK])

            for n in (1, 2):
                verifier = _get_or_create_user(
                    session, f"verifier:{lang_code}:{n}",
                    provider_subject=f"demo-verifier-{lang_code}-{n}",
                    declared_languages=[lang_code],
                    display_name=f"Demo Verifier {n} ({lang_code})",
                )
                _grant_consent(session, verifier, [ConsentScope.ASSIGNED_VERIFIER_PLAYBACK])
                existing_qual = session.query(VerifierQualification).filter_by(
                    user_id=verifier.id, language=lang_code, revoked_at=None
                ).one_or_none()
                if existing_qual is None:
                    session.add(
                        VerifierQualification(
                            user_id=verifier.id,
                            language=lang_code,
                            qualified_at=_now(),
                            # reviewed_by must differ from user_id (CHECK constraint) --
                            # the speaker reviews the verifier qualification for this
                            # demo seed; this is not a real-world review workflow.
                            reviewed_by=speaker.id,
                        )
                    )

            for raw_card in _load_cards(meta["file"]):
                _upsert_card(session, campaign, raw_card)

        session.commit()

    print("Seed complete:")
    for lang_code, meta in LANGUAGES.items():
        print(f"  {lang_code}: campaign={_id(f'campaign:{lang_code}')} speaker={_id(f'speaker:{lang_code}')}")
        for n in (1, 2):
            print(f"        verifier{n}={_id(f'verifier:{lang_code}:{n}')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the local AMAZWI demo database")
    parser.add_argument(
        "--reset",
        action="store_true",
        help=f"clear transient demo run state first (requires {RESET_GUARD_ENV}=true)",
    )
    seed(reset=parser.parse_args().reset)
