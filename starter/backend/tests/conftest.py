"""Shared pytest fixtures for backend tests that need a real database.

Uses `pgserver` (embedded PostgreSQL 16, matching the stack table's stated
`PostgreSQL 16` exactly) rather than SQLite, so constraints, ARRAY columns,
ENUM types and transaction semantics are tested against the real engine
the product will actually run on -- a SQLite substitute would silently
pass tests that fail against real Postgres (e.g. SQLite has no native
ARRAY type or CHECK constraint enforcement parity).

Session-scoped: one embedded server for the whole test run (startup is not
free), but each test gets a clean schema via a function-scoped fixture that
creates/drops all tables per test.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import pgserver
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.models import Base

_PGDATA = Path(__file__).parent / ".pgdata_test"


@pytest.fixture(scope="session")
def pg_server():
    if _PGDATA.exists():
        shutil.rmtree(_PGDATA, ignore_errors=True)
    server = pgserver.get_server(str(_PGDATA), cleanup_mode="delete")
    yield server
    server.cleanup()
    shutil.rmtree(_PGDATA, ignore_errors=True)


@pytest.fixture(scope="session")
def db_engine(pg_server):
    engine = create_engine(pg_server.get_uri())
    yield engine
    engine.dispose()


@pytest.fixture()
def db_session(db_engine):
    """Fresh schema per test: drop everything, recreate from current
    models, yield a Session, then drop again. Slower than a rollback-based
    fixture but correctness-safe -- CHECK constraints and ENUM types are
    exactly what these tests are verifying, so re-running actual DDL per
    test is deliberate, not accidental overhead."""
    with db_engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
    Base.metadata.create_all(db_engine)
    session = Session(db_engine)
    try:
        yield session
    finally:
        session.close()
