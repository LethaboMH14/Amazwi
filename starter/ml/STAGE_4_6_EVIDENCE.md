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

Repository-local Stage 4–6 paths are validated through the resolver/reward/outbox retry chain, Council decision rules, governed export service, and public export API. The remaining integration gap is a production-style end-to-end worker test that consumes the resolver outbox payload and runs Council before export; the worker script exists, but that complete acceptance path is not yet wired into a test. Provider calls, external downloads, GPU training, and Kaggle submission were intentionally not performed. The embedded PostgreSQL fixture has also shown intermittent long-suite instability, so the previously clean 94-test backend run on stable PostgreSQL remains the authoritative broad regression evidence.

## Requirement-to-check matrix

| Requirement or public output | Concrete check | Observed result |
|---|---|---|
| Resolver, reward, outbox, and retry remain idempotent | `tests/test_council_data_e2e.py::test_resolver_reward_outbox_and_retry_are_idempotent` | Passed. One eligibility decision and one outbox event were observed, then claim and retry succeeded. |
| Council outputs are advisory and governed | Council schema, governance, and Council E2E tests in the backend acceptance suite | Passed. The suite covers specialist outputs, consent blocking, and authority-plane invariants. |
| Only eligible, available, opted-in AMAZWI rows can be exported | Direct export tests plus public API acceptance test | Passed. Corpus-eligible plus available audio and active model consent reached export; missing consent returned `422`. |
| Public export lifecycle is usable | FastAPI `TestClient` on `POST /dataset-exports`, `/approve`, and `/revoke` | Passed. Responses were `201 DRAFT`, `200 APPROVED` with manifest hash, and `200 REVOKED`. |
| ML manifest, split, metric, tournament, budget, tabular, and evidence contracts | `cd starter/ml && python -m pytest tests -q` | Passed: **34 tests**. |
| Kaggle entry points are safe to inspect without execution | All five entry-point `--help` commands and `reserve_run.py --show` | Passed. No reservation, download, model execution, or submission occurred. |
| Ungated external downloads are blocked | `download_external.py --dataset swivuriso --task ASR_TRAINING --dry-run` | Passed refusal: exit code `2`, `PREFLIGHT_REQUIRED`, before network access. |
| Backend public integration boundary | `tests/test_council_data_e2e.py`, Council schema, governed peer E2E, and governance schema tests | Passed: **15 tests** against real PostgreSQL. |
| Full prior backend regression | Stable PostgreSQL run of the broader backend suite | Passed: **94 tests**. The embedded local server is not used as equivalent evidence because it has intermittent long-suite resource instability. |
| Production Council worker path | Plan requires `starter/backend/scripts/run_council_worker.py` | Not yet acceptance-tested. The script exists, but no end-to-end test currently consumes the resolver event through that worker into export. |
| External/provider/GPU acceptance | Approved hosted dataset download, Kaggle GPU run, deployment, or alias change | Intentionally not run. No external dataset downloaded, no Kaggle GPU run, no deployment, and no model alias change. |
