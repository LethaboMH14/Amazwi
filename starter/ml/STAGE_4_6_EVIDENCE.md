# AMAZWI Stage 4–6 evidence

## Current state

- Implemented and CPU-verified: Council data primitives, immutable manifests, speaker-safe splits, ASR metrics, external preflight, deterministic tournament gates, budget controls, and tabular challenger scaffolding.
- ML validation: **31 tests passed** before evidence tests; the evidence slice is being validated in the current checkpoint.
- No external dataset downloaded.
- No Kaggle GPU run performed.
- No model alias changed.
- No deployment performed.

## Blocked or not yet run

Backend Stage 4–6 end-to-end acceptance still requires a stable PostgreSQL service run covering resolver, reward, outbox, Council, approved export, and evidence linkage. Provider calls, external downloads, GPU training, and Kaggle submission were intentionally not performed.
