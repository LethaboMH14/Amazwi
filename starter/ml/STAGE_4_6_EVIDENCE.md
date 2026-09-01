# AMAZWI Stage 4–6 evidence

## Current state

- Implemented and CPU-verified: Council data primitives, immutable manifests, speaker-safe splits, ASR metrics, external preflight, deterministic tournament gates, budget controls, and tabular challenger scaffolding.
- ML validation: **34 tests passed** in the completed CPU-safe suite.
- Backend validation: the available Council schema, governed peer end-to-end, and governance schema paths pass **11 tests in 32.61s**. The broader backend suite previously passed **94 tests** on a stable PostgreSQL run.
- Added and validated the governed dataset-export service and `/dataset-exports` draft, approval, and revocation routes. Lint, compilation, route registration smoke test, and the 11-test backend regression pass.
- No external dataset downloaded.
- No Kaggle GPU run performed.
- No model alias changed.
- No deployment performed.

## Blocked or not yet run

Backend Stage 4–6 end-to-end acceptance still requires a stable PostgreSQL service run covering resolver, reward, outbox, Council, approved export, and evidence linkage. Provider calls, external downloads, GPU training, and Kaggle submission were intentionally not performed.
