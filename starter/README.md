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

## Running

```bash
# backend
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload

# frontend
cd frontend && npm install && npm run dev
```

## CI

`.github/workflows/ci.yml` lints and runs backend tests on push.
