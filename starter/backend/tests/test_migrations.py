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


@pytest.fixture()
def clean_db_uri(pg_server, db_engine):
    """A DB with no tables/types at all -- alembic manages the schema
    itself here, unlike db_session which uses Base.metadata directly."""
    from sqlalchemy import text

    with db_engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
    return pg_server.get_uri()


def test_upgrade_creates_all_expected_tables(clean_db_uri, db_engine):
    _run_alembic("upgrade", "head", db_uri=clean_db_uri)
    inspector = inspect(db_engine)
    tables = set(inspector.get_table_names())
    expected = {
        "users", "consent_grants", "campaigns", "cards", "contributions",
        "assignments", "eligibility_decisions", "reward_events",
        "payment_attempts", "receipts", "audit_events", "alembic_version",
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
