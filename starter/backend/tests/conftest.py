"""Shared pytest fixtures for backend tests that need a real database.

Real PostgreSQL 16, not SQLite -- SQLite has no native ARRAY type and
weaker CHECK-constraint parity, so a SQLite-backed suite would silently
pass things that fail against the real engine these models are written
for (see app/models.py's ARRAY/CHECK constraints, and the ENUM-drop bug
this project's migration test caught -- that bug is invisible on SQLite).

Two ways to point at a real Postgres, checked in this order:

1. AMAZWI_TEST_DATABASE_URL env var, if set -- used as-is. This is how
   CI points tests at a `postgres:` service container, and how a local
   dev machine with its own PostgreSQL install (e.g. a standard install
   listening on 5432) can run the suite against that instead of spinning
   up an embedded server every run.
2. Otherwise, an embedded PostgreSQL 16 via `pgserver` -- no install
   needed, but downloads/starts a real Postgres binary per test session,
   which is slower and, on some CI runners, has been observed to be less
   reliable than a plain service container (binary download step depends
   on network access from the runner; a `postgres:` service container has
   no such dependency). Kept as the zero-setup default for local dev.

Session-scoped engine either way: one server/connection pool for the
whole test run, but each test gets a clean schema via a function-scoped
fixture that creates/drops all tables per test.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.models import Base

_PGDATA = Path(__file__).parent / ".pgdata_test"

_EXTERNAL_DB_URL = os.environ.get("AMAZWI_TEST_DATABASE_URL")


@pytest.fixture(scope="session")
def pg_server():
    """Only used when AMAZWI_TEST_DATABASE_URL is not set. Yields None
    when an external URL is in use, so db_engine below has a single
    consistent dependency chain either way."""
    if _EXTERNAL_DB_URL:
        yield None
        return

    import pgserver  # imported lazily: not needed at all when an
    # external DB URL is supplied, so a machine that only has a real
    # Postgres install and never installed the `pgserver` package can
    # still run the suite via AMAZWI_TEST_DATABASE_URL.

    if _PGDATA.exists():
        shutil.rmtree(_PGDATA, ignore_errors=True)
    server = pgserver.get_server(str(_PGDATA), cleanup_mode="delete")
    yield server
    server.cleanup()
    shutil.rmtree(_PGDATA, ignore_errors=True)


@pytest.fixture(scope="session")
def db_engine(pg_server):
    db_url = _EXTERNAL_DB_URL or pg_server.get_uri()
    engine = create_engine(db_url)
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
