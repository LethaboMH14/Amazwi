# AMAZWI Stage 4–6 evidence

## Current state

- Implemented and CPU-verified: Council data primitives, immutable manifests, speaker-safe splits, ASR metrics, external preflight, deterministic tournament gates, budget controls, and tabular challenger scaffolding.
- ML validation: **34 tests passed** in the completed CPU-safe suite.
- Backend validation: the available Council schema, governed peer end-to-end, and governance schema paths pass **11 tests in 32.61s**. The broader backend suite previously passed **94 tests** on a stable PostgreSQL run.
- Added and validated the governed dataset-export service and `/dataset-exports` draft, approval, and revocation routes. Lint, compilation, route registration smoke test, and the 11-test backend regression pass. A FastAPI `TestClient` acceptance path also passed **4 tests in 21.37s**, covering draft creation, approval, revocation, and consent rejection against real PostgreSQL.
- No external dataset downloaded.
- No Kaggle GPU run performed.
- No model alias changed.
- No deployment performed.

## Blocked or not yet run

Repository-local Stage 4–6 paths are validated through the resolver/reward/outbox retry chain, Council decision rules, governed export service, and public export API. The remaining integration gap is a single production-style worker path that consumes the resolver outbox payload and runs Council before export; no such worker entry point exists in the repository yet. Provider calls, external downloads, GPU training, and Kaggle submission were intentionally not performed. The embedded PostgreSQL fixture has also shown intermittent long-suite instability, so the previously clean 94-test backend run on stable PostgreSQL remains the authoritative broad regression evidence.
