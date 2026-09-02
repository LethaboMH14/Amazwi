# Demo runbook — local golden path

Written 2 September 2026. Cross-lane (backend), **pending Sbu's review**.

## ⚠️ The trap: the test suite will wipe your demo

`tests/conftest.py`'s `db_session` fixture runs

```sql
DROP SCHEMA public CASCADE; CREATE SCHEMA public;
```

**per test**, against whatever `AMAZWI_TEST_DATABASE_URL` points at. If the
demo backend points at that same database, then running `pytest` — for any
reason, at any point — destroys every seeded card, user, contribution and
reward event.

This actually happened while building the arcade layer: the dashboard went
from full to empty, and the API started returning `401
AUTHENTICATION_REQUIRED` because the seeded user the frontend authenticates
as no longer existed. The 401 was the symptom; the wipe was the cause.

**So the demo and the tests must not share a database.** Two names, one
server:

| Database | Used by | Safe to destroy |
|---|---|---|
| `postgres` (or whatever `AMAZWI_TEST_DATABASE_URL` names) | `pytest` | Yes — it is dropped per test by design |
| `amazwi_demo` | the demo backend | **No** — this is the demo world |

## One-time setup

```bash
psql "$AMAZWI_TEST_DATABASE_URL" -c "CREATE DATABASE amazwi_demo"
```

No `psql` on the machine? The same thing from Python:

```bash
python -c "import os;from sqlalchemy import create_engine,text;u=os.environ['AMAZWI_TEST_DATABASE_URL'];e=create_engine(u,isolation_level='AUTOCOMMIT');c=e.connect();c.execute(text('CREATE DATABASE amazwi_demo'))"
```

## Bring the demo up

From `starter/backend`, with `AMAZWI_DATABASE_URL` pointed at the **demo**
database (note the `amazwi_demo` suffix, not `postgres`):

```bash
export AMAZWI_DATABASE_URL="postgresql://USER:PASS@localhost:5432/amazwi_demo"
export AMAZWI_AUDIO_TOKEN_SECRET="local-demo-secret-not-for-production-32chars"
export AMAZWI_ALLOW_DEMO_SEED=true
python -m alembic upgrade head
python -m app.seed_demo
python -m app.seed_activity
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

`seed_demo` creates the static world — cards, campaigns, users, consents.
`seed_activity` creates the history that makes the dashboard worth looking
at, by driving the **real resolver and the real matcher**. It never writes
an outcome directly, which is why it is safe to show a judge: the 22 paid
clips and 3 refusals on screen are the resolver's own decisions.

Both are idempotent (uuid5 ids), so re-running them between takes is a
no-op rather than a pile-up.

Then the frontend, from `starter/frontend`:

```bash
VITE_USER_ID=361730a6-0b81-5eb6-b0bf-f79e1c6c7078 VITE_PROVIDER_SUBJECT=demo-speaker-zu API_PROXY_TARGET=http://127.0.0.1:8000 npx vite --host
```

### Why both env vars, and why exported

`api/client.ts` reads `import.meta.env.VITE_*`, which Vite loads from
`.env`. But `vite.config.ts`'s proxy reads `process.env.VITE_*`, which Vite
does **not** populate from `.env`. The proxy attaches the identity headers
that `<audio>` elements cannot set for themselves, so if these are only in
`.env` and never exported, verifier playback fails while everything else
appears to work. Export them in the shell that starts Vite.

## Seeded identities

| Role | Subject | UUID |
|---|---|---|
| Speaker (zu) | `demo-speaker-zu` | `361730a6-0b81-5eb6-b0bf-f79e1c6c7078` |
| Verifier 1 (zu) | `demo-verifier-zu-1` | `043d85b2-1548-5648-ac23-f6564ac651b0` |
| Verifier 2 (zu) | `demo-verifier-zu-2` | `26c3e36e-3471-5d86-ad68-78d7e508a249` |
| Speaker (tn) | `demo-speaker-tn` | `e781ec83-23b7-55d5-94d8-571333960205` |
| Verifier 1 (tn) | `demo-verifier-tn-1` | `55874197-4d33-5261-bd97-7db963650e1f` |
| Verifier 2 (tn) | `demo-verifier-tn-2` | `e7bcb18f-b69a-5442-b1b5-9b8e657f591a` |

Deterministic uuid5 — stable across re-seeds. Each demo device runs its own
Vite process with its own identity pair, so the speaker phone and the two
verifier laptops each present as a different person.

**These are not secrets.** The `demo_header` adapter is development-only
and carries no signature; `app/identity.py` pairs the UUID against the
persisted provider subject, which stops casual impersonation but is not
authentication. Never point this at a production identity, and never
describe it on stage as a security control. (Plan 04 Task 2 is the real
fix and is still open.)

## Check it is actually up

```bash
curl -s localhost:8000/health
curl -s -H "X-User-ID: 361730a6-0b81-5eb6-b0bf-f79e1c6c7078" -H "X-Provider-Subject: demo-speaker-zu" localhost:8000/arcade
```

A `401` here almost always means the demo database was wiped — re-run the
seed steps. Confirm with:

```bash
python -c "import os;from sqlalchemy import create_engine,text;e=create_engine(os.environ['AMAZWI_DATABASE_URL']);c=e.connect();print('users',c.execute(text('select count(*) from users')).scalar())"
```

Expect 13 users and 25 contributions after both seeders have run.

## What the seeded world shows

- 22 contributions paid, **3 refused because the two peers disagreed**
- R44.00 in `reward_events`
- A leaderboard across 5 isiZulu and 4 Setswana contributors

The 3 refusals are deliberate and worth pointing at during the demo: they
are the branch that protects the campaign budget, and they are real
resolver output rather than a fixture asserting a result.
