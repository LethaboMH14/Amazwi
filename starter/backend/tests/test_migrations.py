"""Migration integrity tests (S5). Runs Alembic's real upgrade/downgrade
against a real embedded PostgreSQL 16 instance -- caught a real bug during
authoring (see the note in alembic/versions/*_initial_schema.py's
downgrade()): autogenerate drops tables but not the PostgreSQL ENUM types
backing them, so a naive downgrade→upgrade cycle failed with "type ...
already exists". That's exactly the failure mode Gate H's demo-reset
requirement ("Judge-only demo survives a reset, twice") would hit live, so
this is tested here rather than left to be discovered at the event.
"""
from __future__ import annotations

import subprocess
import sys
import uuid
from pathlib import Path

import pytest
from sqlalchemy import inspect

BACKEND_ROOT = Path(__file__).resolve().parents[1]


def _run_alembic(*args: str, db_uri: str) -> None:
    import os

    env = os.environ.copy()
    env["AMAZWI_DATABASE_URL"] = db_uri
    result = subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=BACKEND_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"alembic {' '.join(args)} failed:\nstdout={result.stdout}\nstderr={result.stderr}"
    )


def _alembic_result(*args: str, db_uri: str):
    import os

    env = os.environ.copy()
    env["AMAZWI_DATABASE_URL"] = db_uri
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=BACKEND_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


@pytest.fixture()
def clean_db_uri(db_engine):
    """A DB with no tables/types at all -- alembic manages the schema
    itself here, unlike db_session which uses Base.metadata directly.
    Derives the URI from db_engine.url rather than pg_server.get_uri()
    directly, so this works whether db_engine is backed by the embedded
    pgserver or an external AMAZWI_TEST_DATABASE_URL (pg_server is None
    in the external-DB case -- see conftest.py)."""
    from sqlalchemy import text

    with db_engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
    return db_engine.url.render_as_string(hide_password=False)


def test_upgrade_creates_all_expected_tables(clean_db_uri, db_engine):
    _run_alembic("upgrade", "head", db_uri=clean_db_uri)
    inspector = inspect(db_engine)
    tables = set(inspector.get_table_names())
    expected = {
        "users", "consent_grants", "campaigns", "cards", "contributions",
        "assignments", "eligibility_decisions", "reward_events",
        "payment_attempts", "receipts", "audit_events", "alembic_version",
        "audio_objects", "verifier_qualifications", "campaign_reward_rules",
    }
    assert expected.issubset(tables), tables


def test_downgrade_then_upgrade_roundtrip_succeeds(clean_db_uri, db_engine):
    """The bug this test exists to catch: a downgrade that drops tables but
    leaves orphaned ENUM types breaks the very next upgrade."""
    _run_alembic("upgrade", "head", db_uri=clean_db_uri)
    _run_alembic("downgrade", "base", db_uri=clean_db_uri)

    inspector = inspect(db_engine)
    # After downgrade to base, no product tables should remain.
    remaining = set(inspector.get_table_names()) - {"alembic_version"}
    assert remaining == set(), f"downgrade left tables behind: {remaining}"

    # The actual regression check: re-upgrading must not fail on
    # "type ... already exists" from an orphaned ENUM.
    _run_alembic("upgrade", "head", db_uri=clean_db_uri)
    inspector = inspect(db_engine)
    assert "contributions" in inspector.get_table_names()


def test_downgrade_drops_all_three_enum_types(clean_db_uri, db_engine):
    from sqlalchemy import text

    _run_alembic("upgrade", "head", db_uri=clean_db_uri)
    _run_alembic("downgrade", "base", db_uri=clean_db_uri)

    with db_engine.connect() as conn:
        result = conn.execute(text("SELECT typname FROM pg_type WHERE typtype='e'"))
        remaining_enums = {row[0] for row in result}
    assert remaining_enums == set(), f"downgrade left enum types behind: {remaining_enums}"


def test_upgrade_preserves_valid_legacy_consent_scope(clean_db_uri, db_engine):
    from sqlalchemy import text

    _run_alembic("upgrade", "a3ea8e6c052e", db_uri=clean_db_uri)
    user_id = uuid.uuid4()
    consent_id = uuid.uuid4()
    with db_engine.begin() as conn:
        conn.execute(
            text(
                "INSERT INTO users (id, provider_subject, declared_languages, created_at) "
                "VALUES (:id, 'legacy-user', ARRAY['tn'], now())"
            ),
            {"id": user_id},
        )
        conn.execute(
            text(
                "INSERT INTO consent_grants "
                "(id, user_id, version, scope, granted_at) "
                "VALUES (:id, :user_id, 'legacy', 'RECORD_PROCESS_ROUND', now())"
            ),
            {"id": consent_id, "user_id": user_id},
        )
    _run_alembic("upgrade", "head", db_uri=clean_db_uri)
    with db_engine.connect() as conn:
        scope = conn.execute(
            text("SELECT scope::text FROM consent_grants WHERE id = :id"),
            {"id": consent_id},
        ).scalar_one()
    assert scope == "RECORD_PROCESS_ROUND"


def test_upgrade_rejects_invalid_legacy_consent_scope_before_conversion(clean_db_uri, db_engine):
    from sqlalchemy import text

    _run_alembic("upgrade", "a3ea8e6c052e", db_uri=clean_db_uri)
    user_id = uuid.uuid4()
    with db_engine.begin() as conn:
        conn.execute(
            text(
                "INSERT INTO users (id, provider_subject, declared_languages, created_at) "
                "VALUES (:id, 'invalid-legacy-user', ARRAY['tn'], now())"
            ),
            {"id": user_id},
        )
        conn.execute(
            text(
                "INSERT INTO consent_grants "
                "(id, user_id, version, scope, granted_at) "
                "VALUES (:id, :user_id, 'legacy', 'NOT_A_SCOPE', now())"
            ),
            {"id": uuid.uuid4(), "user_id": user_id},
        )
    result = _alembic_result("upgrade", "head", db_uri=clean_db_uri)
    assert result.returncode != 0
    assert "invalid scopes" in result.stderr
    with db_engine.connect() as conn:
        assert conn.execute(text("SELECT count(*) FROM consent_grants")).scalar_one() == 1


def _seed_reward_rule(db_engine):
    from sqlalchemy import text

    campaign_id = uuid.uuid4()
    rule_id = uuid.uuid4()
    with db_engine.begin() as conn:
        conn.execute(
            text(
                "INSERT INTO campaigns "
                "(id, name, language, budget_cents, funded_cents, committed_cents, provider_mode) "
                "VALUES (:id, 'Test', 'tn', 1000, 1000, 0, 'DEMO_PROVIDER')"
            ),
            {"id": campaign_id},
        )
        conn.execute(
            text(
                "INSERT INTO campaign_reward_rules "
                "(id, campaign_id, version, contribution_reward_cents, effective_from) "
                "VALUES (:id, :campaign_id, 'v1', 100, now())"
            ),
            {"id": rule_id, "campaign_id": campaign_id},
        )
    return campaign_id, rule_id


def test_reward_rule_financial_terms_cannot_be_updated_or_deleted(clean_db_uri, db_engine):
    from sqlalchemy import text

    _run_alembic("upgrade", "head", db_uri=clean_db_uri)
    campaign_id, rule_id = _seed_reward_rule(db_engine)
    with pytest.raises(Exception, match="campaign reward terms are immutable"):
        with db_engine.begin() as conn:
            conn.execute(
                text(
                    "UPDATE campaign_reward_rules "
                    "SET contribution_reward_cents = 200 WHERE id = :id"
                ),
                {"id": rule_id},
            )
    with pytest.raises(Exception, match="campaign reward rules cannot be deleted"):
        with db_engine.begin() as conn:
            conn.execute(
                text("DELETE FROM campaign_reward_rules WHERE id = :id"),
                {"id": rule_id},
            )
    assert campaign_id is not None


def test_reward_rule_retirement_is_one_way(clean_db_uri, db_engine):
    from sqlalchemy import text

    _run_alembic("upgrade", "head", db_uri=clean_db_uri)
    _, rule_id = _seed_reward_rule(db_engine)
    with db_engine.begin() as conn:
        conn.execute(
            text("UPDATE campaign_reward_rules SET retired_at = now() WHERE id = :id"),
            {"id": rule_id},
        )
    with pytest.raises(Exception, match="retired_at transition is immutable"):
        with db_engine.begin() as conn:
            conn.execute(
                text("UPDATE campaign_reward_rules SET retired_at = NULL WHERE id = :id"),
                {"id": rule_id},
            )
