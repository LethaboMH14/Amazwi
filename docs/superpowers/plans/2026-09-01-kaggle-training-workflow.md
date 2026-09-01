# Kaggle ASR Training Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans (recommended). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace placeholder Kaggle entry points with gated, reproducible ASR training, evaluation, and packaging workflows for Lethabo and Sbu.

**Architecture:** Keep repository-local validation CPU-safe. Training and evaluation validate immutable manifests, exact model/data revisions, and budget reservations before importing heavyweight model code. Kaggle kernels perform GPU work and emit hashes consumed by the existing evidence and tournament modules.

**Tech Stack:** Python 3.11+, argparse, JSON/SHA-256, existing `amazwi_ml` manifest/external/budget/metrics/evidence/tournament modules, Hugging Face Transformers/PEFT on Kaggle only, pytest.

## Global Constraints

- Lethabo uses `team-sonar-a`; Sbu uses `team-sonar-b`; each is capped at 30 GPU hours and aggregate usage is capped at 60 hours.
- Swivuriso is ASR-only; TTS, voice cloning, voice synthesis, and human-voice replication are prohibited.
- Training requires exact immutable dataset/model revisions, approved preflight evidence, immutable manifest hash, and valid budget reservation.
- Credentials remain in local Kaggle configuration or environment and never enter source control, logs, prompts, or chat.
- No model alias, production rule, deployment, payment, campaign launch, or external download occurs implicitly.
- CPU tests must run without Kaggle-only GPU dependencies.

---

### Task 1: Define gated run configuration and refusal tests

**Files:** Modify `starter/ml/kaggle/train_asr.py`, `starter/ml/kaggle/evaluate_asr.py`, and `starter/ml/tests/test_kaggle_scripts.py`.

**Interfaces:** `parse_train_args(argv)`, `validate_run_inputs(args)`, and `parse_evaluate_args(argv)` must reject missing manifest, hash, model revision, reservation, unsupported candidate, and prohibited task before heavyweight imports.

- [ ] Add failing tests for each refusal and successful help parsing.
- [ ] Run `cd starter/ml && python -m pytest tests/test_kaggle_scripts.py -q` and record failures.
- [ ] Implement parsers and SHA-256/reservation validation.
- [ ] Re-run focused tests and all entry-point help commands.
- [ ] Commit `ML: gate Kaggle ASR run inputs`.

### Task 2: Implement real Kaggle training and evaluation adapters

**Files:** Modify `starter/ml/kaggle/train_asr.py`, `starter/ml/kaggle/evaluate_asr.py`, `starter/ml/requirements-kaggle.txt`; create `starter/ml/kaggle/run_config.example.json`.

**Interfaces:** `run_training(args) -> Path` and `run_evaluation(args) -> Path` load approved inputs only after validation, use explicit seeds, save checkpoints/predictions/metrics/logs, and preserve evaluation-manifest hashes.

- [ ] Add failing adapter tests with tiny local fixtures and mocked model boundaries.
- [ ] Implement lazy Kaggle-only Transformers/PEFT imports, dataset column mapping, deterministic seeding, checkpoint saving, and output paths.
- [ ] Implement evaluation through `amazwi_ml.metrics.evaluate_asr` with unchanged-manifest verification.
- [ ] Run CPU-safe tests without model downloads or GPU execution.
- [ ] Commit `ML: add gated Kaggle ASR adapters`.

### Task 3: Implement reproducible packaging and ledger completion

**Files:** Modify `starter/ml/kaggle/package_run.py`, `starter/ml/kaggle/reserve_run.py`, and `starter/ml/tests/test_kaggle_scripts.py`.

**Interfaces:** `package_run(paths, output) -> str` writes canonical artefact hashes; reserve and completion commands call the existing budget helpers only with explicit inputs.

- [ ] Add failing tests for missing artefacts, duplicate reservations, and deterministic package hashes.
- [ ] Implement canonical packaging and atomic ledger transitions.
- [ ] Run the full ML suite and safe CLI checks.
- [ ] Commit `ML: package governed Kaggle run evidence`.

### Task 4: Prepare dual run records and Sbu handoff

**Files:** Create `starter/ml/runs/README.md`; modify the Sbu handoff and `starter/ml/STAGE_4_6_EVIDENCE.md`.

**Interfaces:** Run records contain account alias, candidate, exact data/model revisions, manifest/config hashes, reservation ID, output location, and status, with no credentials.

- [ ] Add blocked-state run-record templates.
- [ ] Record Lethabo as `team-sonar-a` and Sbu as `team-sonar-b`; leave exact revisions blocked until preflight evidence exists.
- [ ] Run documentation/hash checks and commit `Docs: prepare dual Kaggle run records`.

### Task 5: End-to-end acceptance and launch gate

**Files:** Modify `starter/ml/tests/test_kaggle_scripts.py` and `starter/ml/STAGE_4_6_EVIDENCE.md`; modify backend E2E tests only for worker/export evidence.

- [ ] Run the full ML suite and safe CLI checks.
- [ ] Verify ungated download exits 2 with `PREFLIGHT_REQUIRED`.
- [ ] Run backend public export/Council checks against PostgreSQL.
- [ ] Confirm no credentials or generated checkpoints are tracked.
- [ ] Launch a Kaggle kernel only after exact revision, licence, model, manifest, and reservation gates pass.
- [ ] Commit evidence only and push through a fast-forward-safe branch update.

## Review gates

- Never spend GPU hours on placeholder code.
- Every changed public output has a test and an evidence entry.
- Missing external approval remains `BLOCKED`.
- Never force-push the diverged `main` branch.
