# Generic starter

React PWA + FastAPI + a swappable payment-provider adapter, with CI. No product concept lives here — this is scaffolding only, wired up before the event so Gate A (`../05_amazwi/plan/05_BUILD.md` §4) starts from a running shell instead of an empty one.

## Layout

```
starter/
  frontend/   React 18 + TypeScript + Vite PWA shell
  backend/    FastAPI app, health check, provider adapter interface
```

## Provider adapter

`backend/app/provider.py` defines `PaymentProvider` (Protocol) with `DemoProvider` (in-memory, always succeeds) as the only implementation checked in here. A real MoMo adapter is added during the event once sandbox access is confirmed (P0 S1).

## Host bridge adapter

`frontend/src/hostBridge.ts` — same pattern as the payment adapter, applied to the mini-app-shell integration. `createHostBridge()` returns `StandaloneBridge` (no-op, used in local dev and outside any host WebView) or `CommunityDocBridge` (a keep-alive heartbeat, sent every 45s).

⚠️ **`CommunityDocBridge`'s wire protocol is transcribed from a community-authored integration article, not a confirmed organiser specification** — see `../05_amazwi/research/B_MOMO_API.md` and the explicit warning in `../05_amazwi/plan/02_TECH.md` ("do not hard-code an unverified public-doc assumption as platform truth"). It exists so the app doesn't silently drop the host session during a long interaction (reading a card, recording) if that protocol turns out to be right — and it's swappable for whatever the mentors confirm on day one without touching anything that calls `HostBridge`.

7 tests cover the heartbeat timing, the `START_JOURNEY` handoff, and that `notify('DONE')` actually stops the interval — the failure mode that matters here is a heartbeat that keeps firing (or stops firing) after the round ends.

## Running

```bash
# backend
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload

# frontend
cd frontend && npm install && npm run dev

# If the backend is elsewhere during local development:
# API_PROXY_TARGET=http://127.0.0.1:8000 npm run dev
```

## Verified (31 Aug, this session)

- Backend: `pytest` — 2/2 pass, run in a clean venv
- Frontend: `npm test` (vitest) — 7/7 pass; `npx tsc -b --noEmit` — clean; `npm run build` — succeeds, 144KB JS / 46.6KB gzipped

## CI

`.github/workflows/ci.yml` — backend job runs pytest; frontend job runs vitest + a strict typecheck.
