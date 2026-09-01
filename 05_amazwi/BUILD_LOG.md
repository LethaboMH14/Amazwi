# AMAZWI — BUILD LOG

### [01 Sep ~18:22] — Jcode · Plan 02 Tasks 11–12 · deterministic tournament and budget/Kaggle slice

**VERIFIED**
- Implemented deterministic tournament evidence types, candidate ranking, exact ASR gates, exact QUALITY_RISK and MISSION_RANKING gates, stable reason-code ordering, and advisory no-alias-mutation decisions.
- Implemented atomic canonical JSON GPU ledger with 60-hour aggregate cap, 30-hour account cap, locked phase caps (6/8/16/16/8/6), duplicate/hash/input checks, reservation completion, fsync, and replace.
- Added pinned Kaggle requirements, budget metadata, CPU-safe no-download entry points, synthetic fixtures, and tests. Targeted suite run twice: **8 passed** each run. Four `--help` paths and `reserve_run.py --show` completed without GPU, network, provider, or model execution.
- No dataset/model download, GPU reservation, Kaggle submission, provider call, or model-result claim was made.

**REMAINING GAPS**
- Kaggle training/evaluation/package entry points are intentionally safe scaffolds, not resource-backed training or artifact packaging implementations.
- Plan 02 tabular challengers, evidence/model cards, and backend Stage 4–6 acceptance remain open.

---

### [01 Sep ~18:08] — Jcode · Plan 02 ML progress checkpoint · governed primitives and external preflight

**VERIFIED**
- The initial `starter/ml` package is now present with canonical manifest hashing, deterministic speaker-group splits, ASR metric primitives, an external dataset registry, and revision/task-scoped download preflight.
- The corrected ML test suite passes **19/19** with `cd starter\ml && python -m pytest -q`; Python compilation also passes.
- Added CPU-safe deterministic tournament gates, strict ASR artefact/evaluation-manifest checks, the account/aggregate/phase budget ledger, locked Kaggle budget metadata, and no-network entry-point help surfaces. The expanded ML suite passes **28/28**; explicit module compilation and all four script help paths pass.
- No external download, network access, provider call, GPU, or model result was used.

**STATUS / NEXT**
- This closes only the first governed Plan 02 implementation slice. Tournament promotion gates, the 60-hour budget ledger, tabular evaluation, evidence/model cards, Kaggle entry points, and backend Stage 4–6 acceptance remain open.
- Task 02 is therefore in progress, not complete. Continue with deterministic CPU-safe tournament and budget controls before any resource-backed run.

---

### [01 Sep ~17:55] — Jcode · Plan 02 ML first checkpoint · manifest/splits/metrics slice

**DID**
- Added synthetic-only `starter/ml` package scaffolding, pinned CPU requirements, canonical manifest models and hashing, immutable writes, deterministic speaker-group splits, and fixture-driven tests.
- Added deterministic ASR metric APIs and tests; ant corrected the metric implementation and expectations for standard CER and required slice ordering during this checkpoint.

**VERIFIED / BLOCKED**
- The metric implementation and expectations were corrected, and the combined first-slice validation is recorded above. Generated `__pycache__` files were removed.
- No datasets, providers, network downloads, GPU, model training, or model-result claims were made. Tournament, budget/Kaggle, tabular, and evidence tasks remain open.

**NEXT**
- Rerun `cd starter\ml && C:\Python311\python.exe -m pytest tests\test_manifest.py tests\test_splits.py tests\test_metrics.py -q` in a stable process before treating this slice as green.

---

### [01 Sep 16:20] — Jcode · Plan 02 continuation · external, tournament, and budget slice

**IMPLEMENTED**
- Added reviewed external dataset registry with canonical SHA-256 hashing.
- Added metadata-only preflight evidence and a download gate rejecting missing, mismatched, prohibited, blocked, or stale approvals before network-client import.
- Added direct-run-safe preflight and download CLIs. Ungated dry-run is designed to exit 2 with `PREFLIGHT_REQUIRED`.
- Added deterministic tournament ranking and ASR/tabular promotion gates.
- Added atomic 60-hour budget controls with 30-hour account caps, phase caps, duplicate-run checks, valid hashes, and completed-run actual-hour accounting.
- Added CPU-safe Kaggle entry-point help contracts and pinned Kaggle requirements.

**VALIDATION**
- Focused external, budget, tournament, and Kaggle tests: **18 passed**.
- Full CPU-safe ML suite: **28 passed**.
- No network, datasets, GPU, provider, Kaggle run, deployment, or model download was performed.
- `metrics.py` and its tests were not edited.

**REMAINING GAPS**
- Evidence/model-card generation and tabular challenger implementation remain for later slices. A clean captured CLI exit-2 transcript remains to be recorded because the direct command was interrupted by the Windows command wrapper.
