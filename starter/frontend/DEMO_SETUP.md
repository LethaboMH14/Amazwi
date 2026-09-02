# Running the demo locally — the two things that block it

Found 2 Sep 2026 by actually walking the flow in a browser rather than trusting the tests. Both were invisible to the test suite because the tests stub the API.

## 1. The `/api` proxy rewrite (fixed in `vite.config.ts`)

The backend mounts its routes at the **root** — `/consents`, `/contributions`, `/assignments`, `/impact`, `/ops` — not under `/api`. The dev proxy was forwarding `/api/consents` verbatim, so the backend 404'd **every authenticated call**.

This stayed hidden for a long time because the backend *also* serves `/api/health` as a special case. So the one endpoint anyone smoke-tests was the one endpoint that worked, while the entire consent → record → verify → result flow was dead. The symptom at the UI was simply that **Continue did nothing** — no error, no navigation.

Already fixed. Do not remove the `rewrite` line.

## 2. A demo identity (`.env.local`, gitignored — you must create it)

`src/api/client.ts` only sends the `X-User-ID` / `X-Provider-Subject` headers the backend requires when these Vite env vars are set. Without them every authenticated route returns `401 AUTHENTICATION_REQUIRED`.

Create `starter/frontend/.env.local`:

```
VITE_USER_ID=361730a6-0b81-5eb6-b0bf-f79e1c6c7078
VITE_PROVIDER_SUBJECT=demo-speaker-zu
```

These are **not secrets** — they are rows created by `python -m app.seed_demo`, which uses deterministic `uuid5`, so the values are stable across re-seeds. The `demo_header` auth adapter is development-only; the real Mini App host replaces it.

### The seeded identities

| Subject | User ID | Use on |
|---|---|---|
| `demo-speaker-zu` | `361730a6-0b81-5eb6-b0bf-f79e1c6c7078` | the speaker phone (isiZulu) |
| `demo-speaker-tn` | `e781ec83-23b7-55d5-94d8-571333960205` | the speaker phone (Setswana) |
| `demo-verifier-zu-1` | `043d85b2-1548-5648-ac23-f6564ac651b0` | verifier laptop 1 |
| `demo-verifier-zu-2` | `26c3e36e-3471-5d86-ad68-78d7e508a249` | verifier laptop 2 |
| `demo-verifier-tn-1` | `55874197-4d33-5261-bd97-7db963650e1f` | verifier laptop 1 (Setswana) |
| `demo-verifier-tn-2` | `e7bcb18f-b69a-5442-b1b5-9b8e657f591a` | verifier laptop 2 (Setswana) |

**Each demo device runs its own frontend process with its own identity** — that is the design, and it is why `vite.config.ts` also injects the same headers at the proxy level: browser media elements (`<audio src=...>`) cannot attach headers, so private audio playback depends on the proxy carrying the identity instead.

⚠️ The proxy-injected headers read `process.env`, **not** `.env.local`. Vite loads `.env.local` into `import.meta.env` for client code only; `vite.config.ts` runs in Node beforehand. For the verifier devices, where audio playback matters, export them in the shell:

```bash
VITE_USER_ID=043d85b2-1548-5648-ac23-f6564ac651b0 VITE_PROVIDER_SUBJECT=demo-verifier-zu-1 npm run dev
```

## Seeding

```bash
cd starter/backend
AMAZWI_DATABASE_URL="postgresql://postgres:@127.0.0.1:54730/postgres" \
AMAZWI_MODE=DEMO AMAZWI_PRIVATE_AUDIO_ROOT=".private_audio" \
AMAZWI_AUDIO_SIGNING_KEY="demo-signing-key" AMAZWI_AUTH_BACKEND="demo_header" \
AMAZWI_RATE_LIMIT_BACKEND="in_memory" \
python -m app.seed_demo
```

Port `54730` is whatever the running pgserver instance is on — check the backend process's own `AMAZWI_DATABASE_URL`, do not assume this number.

**Verified 2 Sep 2026:** running it twice leaves counts unchanged (16 cards / 2 campaigns / 6 users) — genuinely idempotent, not just intended to be. All 16 cards satisfy the CHECK constraints (`blocked_words` = 4, `accepted_answers` ≥ 2, `distractors` = 3), including `ntlo` with its three native-reviewed accepted forms.
