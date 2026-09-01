# Kaggle ASR Training Workflow Design

## Goal
Replace the placeholder Kaggle ASR entry points with a gated, reproducible Whisper primary run and comparator run that can produce evidence without exposing credentials or changing production aliases.

## Approved experiment split
- Lethabo, `team-sonar-a`: Whisper Large V3 Turbo PEFT primary ASR run.
- Sbu, `team-sonar-b`: XLS-R or Wav2Vec-BERT comparator run.
- Both runs use the same immutable speaker-safe evaluation manifest and report WER, CER, embedded-span error, language/domain/acoustic/code-switch slices, and artefact hashes.
- The rule baseline remains CPU-only and consumes no GPU allocation.

## Data and governance gates
The runner requires a local manifest path and SHA-256, exact external dataset revision, registry/preflight evidence, model revision, and a valid budget reservation before training. Swivuriso is ASR-only. TTS, voice cloning, synthesis, human-voice replication, unrestricted production audio access, and floating dataset revisions are rejected. Credentials are read only from Kaggle's local configuration or environment and never written to the repository.

## Components
- `train_asr.py`: parse and validate run configuration, verify hashes and reservation, load an approved local/Kaggle-attached manifest, fine-tune the selected speech-recognition model, and write checkpoint/log/environment evidence.
- `evaluate_asr.py`: verify the unchanged evaluation manifest, load a checkpoint, calculate existing AMAZWI metrics and slices, and write canonical predictions and metric evidence.
- `package_run.py`: hash config, manifest, checkpoint, predictions, metrics, logs, and environment into an evidence index.
- `reserve_run.py`: display or create a ledger reservation without importing scientific runtimes for help mode.
- `tests/test_kaggle_scripts.py`: exercise validation, refusal paths, deterministic packaging, and help mode without GPU/network execution.

## Safety and failure handling
No external download or model download starts until all gates pass. Missing files, mismatched hashes, invalid reservations, unsupported candidates, or prohibited tasks fail closed with actionable errors. Training failures leave no promotion decision and never mutate aliases. GPU work is launched only through an explicitly approved Kaggle notebook after local CPU-safe checks pass.

## Acceptance
CPU tests must pass, CLI help must work on Windows, ungated downloads must return `PREFLIGHT_REQUIRED`, package hashes must be reproducible, and a real Kaggle run must publish only run metadata and hashes back to the repository. External/GPU execution remains separately labelled from repository-local validation.
