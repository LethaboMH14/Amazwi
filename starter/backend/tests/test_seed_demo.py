from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models import Card, Campaign, CampaignRewardRule, ConsentGrant, Contribution, User, VerifierQualification
from app import seed_demo


def test_seed_demo_is_idempotent(db_engine, monkeypatch):
    monkeypatch.setenv("AMAZWI_DATABASE_URL", str(db_engine.url))
    seed_demo.get_engine.cache_clear()
    seed_demo.seed()
    seed_demo.seed()

    # Scope every assertion to the seed's own deterministic ids rather than
    # counting whole tables -- table-wide counts are fragile against the
    # full suite, where other tests may leave rows in the same shared
    # database without a rolled-back transaction (confirmed: exact-count
    # assertions here flaked 7 vs 6 on User when run after the full suite,
    # even against a freshly-recreated database, because this test's own
    # fixture doesn't isolate per-test). Scoped ids are correct regardless
    # of what else exists in the table.
    speaker_ids = [seed_demo._id(f"speaker:{lang}") for lang in seed_demo.LANGUAGES]
    verifier_ids = [
        seed_demo._id(f"verifier:{lang}:{n}")
        for lang in seed_demo.LANGUAGES
        for n in (1, 2)
    ]
    campaign_ids = [seed_demo._id(f"campaign:{lang}") for lang in seed_demo.LANGUAGES]
    card_ids = [
        seed_demo._id(f"card:{raw['id']}")
        for lang, meta in seed_demo.LANGUAGES.items()
        for raw in seed_demo._load_cards(meta["file"])
    ]

    from app.db import get_engine
    with get_engine().connect() as conn:
        assert conn.execute(
            select(func.count()).select_from(Card).where(Card.id.in_(card_ids))
        ).scalar_one() == 16
        assert conn.execute(
            select(func.count()).select_from(Campaign).where(Campaign.id.in_(campaign_ids))
        ).scalar_one() == 2
        assert conn.execute(
            select(func.count()).select_from(CampaignRewardRule).where(
                CampaignRewardRule.campaign_id.in_(campaign_ids)
            )
        ).scalar_one() == 2
        assert conn.execute(
            select(func.count()).select_from(User).where(User.id.in_(speaker_ids + verifier_ids))
        ).scalar_one() == 6
        assert conn.execute(
            select(func.count()).select_from(VerifierQualification).where(
                VerifierQualification.user_id.in_(verifier_ids)
            )
        ).scalar_one() == 4
        # 2 scopes/speaker (RECORD_PROCESS_ROUND, ASSIGNED_VERIFIER_PLAYBACK) x 2
        # languages = 4, + 1 scope/verifier x 4 verifiers = 4. Total 8, not 10 --
        # RETAIN_MODEL_DEVELOPMENT is not granted here because resolver.py only
        # requires RECORD_PROCESS_ROUND for CORPUS_ELIGIBLE (checked directly);
        # RETAIN_MODEL_DEVELOPMENT gates dataset export only (app/datasets.py),
        # a separate, non-golden-path feature. Verified against real Postgres.
        assert conn.execute(
            select(func.count()).select_from(ConsentGrant).where(
                ConsentGrant.user_id.in_(speaker_ids + verifier_ids)
            )
        ).scalar_one() == 8
        # Codex's richer constraint check (all three array constraints, not
        # just blocked_words), kept and scoped to the seed's own card ids.
        bad = conn.execute(
            select(func.count()).select_from(Card).where(
                Card.id.in_(card_ids),
                (func.cardinality(Card.blocked_words) != 4)
                | (func.cardinality(Card.accepted_answers) < 2)
                | (func.cardinality(Card.distractors) != 3),
            )
        ).scalar_one()
        assert bad == 0


def test_reset_returns_demo_to_known_baseline(db_engine, monkeypatch):
    monkeypatch.setenv("AMAZWI_DATABASE_URL", str(db_engine.url))
    monkeypatch.setenv(seed_demo.RESET_GUARD_ENV, "true")
    seed_demo.get_engine.cache_clear()
    seed_demo.seed(reset=True)

    campaign_id = seed_demo._id("campaign:zu")
    speaker_id = seed_demo._id("speaker:zu")
    card_id = seed_demo._id("card:zu-001")
    with Session(seed_demo.get_engine()) as session:
        rule = session.scalar(
            select(CampaignRewardRule).where(CampaignRewardRule.campaign_id == campaign_id)
        )
        contribution = Contribution(
            speaker_id=speaker_id,
            card_id=card_id,
            declared_language="zu",
            reward_rule_id=rule.id,
        )
        session.add(contribution)
        session.get(Campaign, campaign_id).committed_cents = 200
        session.commit()
        contribution_id = contribution.id

    seed_demo.seed(reset=True)

    # A separate connection proves reset state was committed, while seeded
    # identities/content/campaigns remain available for the next take.
    with seed_demo.get_engine().connect() as conn:
        assert conn.scalar(
            select(func.count()).select_from(Contribution).where(Contribution.id == contribution_id)
        ) == 0
        assert conn.scalar(select(Campaign.committed_cents).where(Campaign.id == campaign_id)) == 0
        assert conn.scalar(select(func.count()).select_from(Card).where(Card.id == card_id)) == 1
        assert conn.scalar(select(func.count()).select_from(User).where(User.id == speaker_id)) == 1


def test_reset_requires_explicit_guard(db_engine, monkeypatch):
    monkeypatch.setenv("AMAZWI_DATABASE_URL", str(db_engine.url))
    monkeypatch.delenv(seed_demo.RESET_GUARD_ENV, raising=False)
    seed_demo.get_engine.cache_clear()

    import pytest

    with pytest.raises(RuntimeError, match=seed_demo.RESET_GUARD_ENV):
        seed_demo.seed(reset=True)
