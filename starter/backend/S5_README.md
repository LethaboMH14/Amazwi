# S5 — schema, migrations, reward ledger

**Cross-lane, pending Sbu's review.** Built under this session's loosened
lane rule (`BUILD_LOG.md`, 31 Aug ~23:40). Not a data-integrity/deployment
sign-off — that stays Sbu's per `05_BUILD.md` §2. See `HANDOVER_SBU.md`.

## What's here

- `app/models.py` — SQLAlchemy models for every record in
  `plan/02_TECH.md` §3, with the CHECK/UNIQUE constraints from §4, §8 and
  `content/SCHEMA.md` enforced at the database level, not just in
  application code.
- `alembic/` — real Alembic migrations. `alembic/versions/*_initial_schema.py`
  creates all 11 tables. Its `downgrade()` has a manual addition beyond
  what autogenerate produced — see the comment in that file for why
  (autogenerate doesn't drop PostgreSQL ENUM types, which breaks
  downgrade→upgrade cycles otherwise; this is exactly Gate H's "demo
  survives a reset, twice" requirement).
- `app/ledger.py` — the reward-ledger service functions needed to make
  §8's six required invariants real: `credit_reward`, `request_cash_out`,
  `apply_payment_callback`, `available_balance_cents`.
- `app/resolver.py` — §5's assignment invariants (no-self-verification,
  expired/voided-audio rejection) and the resolver pseudocode implemented
  verbatim: `create_assignment()`, `resolve_contribution()`. Terminal
  resolution persists contribution state, its EligibilityDecision and a
  corpus-eligible reward in one transaction, so a failed reward cannot
  strand a decision that prevents a later retry.
- `tests/conftest.py` — a real Postgres fixture with two backends: an
  external `AMAZWI_TEST_DATABASE_URL` (used by CI's `postgres:16` service
  container, or your own local Postgres install) takes priority when set;
  otherwise falls back to an embedded PostgreSQL 16 via `pgserver` for
  zero-setup local dev. Not SQLite either way — matches the stack table's
  stated `PostgreSQL 16` exactly.
- `tests/test_migrations.py`, `test_schema_constraints.py`,
  `test_ledger_invariants.py`, `test_assignment_invariants.py`,
  `test_resolver.py` — 40 new tests, all run against real Postgres, 0
  mocks.

## Not here (deliberately, not an oversight)

- The MoMo provider adapter itself (§9) — real external-API unknowns,
  separate piece of work.
- Random eligible-cohort selection for assignments. `create_assignment()`
  enforces no-self-verification, but it deliberately takes the selected
  verifier from a future dispatcher rather than inventing cohort logic
  before §7/§10 exist.
- Consent enforcement (§10) and audio storage (§7).
- Any FastAPI endpoint wiring — `app/main.py` is untouched.

## Running the tests

```bash
cd starter/backend
pip install -r requirements.txt
pytest tests/ -v
```

No Docker or system Postgres install needed — `pgserver` downloads/runs a
real embedded PostgreSQL 16 binary automatically on first use, deleted
after each test session (`tests/conftest.py`'s `pg_server` fixture,
`cleanup_mode="delete"`).

## Running migrations against a real (non-test) database

```bash
cd starter/backend
set AMAZWI_DATABASE_URL=postgresql://user:pass@host/dbname   # Windows
export AMAZWI_DATABASE_URL=postgresql://user:pass@host/dbname # bash
python -m alembic upgrade head
```

If `AMAZWI_DATABASE_URL` is unset, `alembic.ini`'s placeholder
(`driver://user:pass@localhost/dbname`) is used and will fail to connect
on purpose — nobody should accidentally migrate a default local database
with no override.

## A real bug this caught

Alembic's `revision --autogenerate` produced a `downgrade()` that drops
tables using PostgreSQL ENUM-typed columns but never drops the ENUM types
themselves. A plain `upgrade → downgrade → upgrade` cycle against a real
Postgres instance failed on the second `upgrade` with `type "payment_state"
already exists`. Fixed by adding explicit `sa.Enum(...).drop(...)` calls to
`downgrade()` — see the comment in
`alembic/versions/a3ea8e6c052e_initial_schema.py`. Caught by
`test_migrations.py::test_downgrade_then_upgrade_roundtrip_succeeds`, run
against the real engine — this would not have been caught by a
mocked/SQLite test.
