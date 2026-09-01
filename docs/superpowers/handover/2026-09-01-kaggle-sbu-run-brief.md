# Urgent Sbu Kaggle run brief

## Objective
Run an independent ASR comparator for AMAZWI using the same immutable manifest and held-out speaker-safe evaluation split as Lethabo's primary run. Do not use this repository's placeholder `train_asr.py` as a real trainer.

## Ownership
- Kaggle budget alias: `team-sonar-b` unless the coordinator confirms otherwise.
- Budget ceiling: 30 GPU hours for this account, 60 hours aggregate across both accounts.
- Suggested allocation: 24 hours training, 4 hours evaluation, 2 hours packaging/reproducibility.
- Report only Kaggle notebook/run URL, status, GPU hours, manifest SHA-256, checkpoint SHA-256, prediction SHA-256, and metric-report SHA-256.

## Model and data
- Comparator: `w2v-bert-2-african` or XLS-R, whichever is available and approved in the Kaggle environment.
- Task: ASR only. No TTS, voice cloning, voice synthesis, or human-voice replication.
- Dataset: Swivuriso / ZA-African Next Voices, exact immutable Hugging Face revision only. Do not use floating `main`.
- Use only a reviewed exact revision, licence/restrictions evidence, speaker-safe train/dev/test manifests, and an approved model licence.
- Keep the evaluation manifest untouched and identical to Lethabo's run.

## Required preflight
1. Confirm Kaggle account and GPU quota.
2. Record exact dataset revision, registry hash, licence/restrictions, and model revision.
3. Confirm `RETAIN_MODEL_DEVELOPMENT`/dataset terms are approved for the selected data.
4. Reserve the run in the shared budget ledger before training.
5. Stop if any exact revision, licence, manifest, or budget reservation is missing.

## Execution
- Use a real executable Kaggle notebook or script, not a CLI stub that only parses arguments.
- Pin the environment and seed.
- Save immutable train/dev/evaluation manifest hashes.
- Save checkpoint, predictions, metrics, logs, and environment lock.
- Evaluate WER, CER, embedded-span error, language slices, domain/acoustic slices, and code-switch slices.
- Do not promote or change any production alias from the notebook.

## Handoff
Start only after the above gates pass. If blocked, report the exact blocker rather than downloading or training. Coordinate with Lethabo so both runs use the same evaluation manifest and comparable metrics.
