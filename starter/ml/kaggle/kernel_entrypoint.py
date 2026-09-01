"""Kaggle kernel entrypoint for the AMAZWI overnight ASR fine-tune.

Runs entirely inside the Kaggle GPU environment against real, tested repo
code bundled directly alongside this script (amazwi_ml_bundle/, reserve_run.py,
train_asr.py, budget.json, preflight_swivuriso.json -- no git clone, since the
source GitHub repo is private and Kaggle's environment has no credentials for
it). Downloads the isiZulu ("zul") and Setswana ("tsn") DEV splits of the
approved Swivuriso dataset (dsfsi-anv/za-african-next-voices-compressed) --
not the full ~3,000 hour corpus -- builds a real canonical manifest via the
bundled amazwi_ml.manifest, reserves the GPU-hour budget, then runs the
bundled, gated train_asr.py. Nothing here bypasses a gate; it drives the same
gates non-interactively.

Scope is deliberately bounded for one overnight run: DEV splits only
(~683MB, ~8,000 clips across both languages), not train (which is 12GB+
combined) -- a sane amount to actually fine-tune on and evaluate within a
single GPU session, not a production-scale training run.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

INPUT_DATASET = Path("/kaggle/input/amazwi-ml-support-files")
DATASET_REPO = "dsfsi-anv/za-african-next-voices-compressed"
LANGUAGES = ["zul", "tsn"]
SPLIT = "dev"  # bounded overnight scope; NOT train (12GB+ combined)
CANDIDATE = "whisper-large-v3-turbo-peft"
MODEL_REVISION = "openai/whisper-large-v3-turbo"


def sh(cmd: list[str], cwd: Path | None = None) -> None:
    # Running kaggle/*.py as a script (not `python -m`) puts the script's own
    # directory on sys.path[0], not cwd -- amazwi_ml (which lives directly
    # under starter/ml) is invisible without PYTHONPATH set explicitly.
    # Caught this the hard way: the existing test suite only ever subprocess-
    # invokes these scripts with --help, which exits before the import runs,
    # so this bug was never exercised until this dry-run.
    print("+", " ".join(cmd), flush=True)
    env = os.environ.copy()
    if cwd is not None:
        env["PYTHONPATH"] = str(cwd) + os.pathsep + env.get("PYTHONPATH", "")
    subprocess.run(cmd, cwd=cwd, check=True, env=env)


def main() -> int:
    # /kaggle/input is read-only; reserve_run.py needs to write budget.json,
    # so stage everything into a writable working copy first.
    ml_dir = Path("/kaggle/working/ml")
    if ml_dir.exists():
        shutil.rmtree(ml_dir)
    shutil.copytree(INPUT_DATASET, ml_dir)
    zip_path = ml_dir / "amazwi_ml.zip"
    if zip_path.exists() and not (ml_dir / "amazwi_ml" / "__init__.py").exists():
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(ml_dir)
    print("Staged working files:", sorted(p.name for p in ml_dir.iterdir()), flush=True)

    sh([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-kaggle.txt"], cwd=ml_dir)

    sys.path.insert(0, str(ml_dir))
    # NOTE: amazwi_ml.manifest.ManifestRecord is a portable, hash-only format
    # (audio_sha256, no local path) -- it is the governance/audit artifact,
    # not what train_asr.py reads. train_asr.py's own _records()/validate_
    # training_inputs() expect a plain {"records":[{split, excluded, text,
    # audio_path}, ...]} file and hash *that exact file*. Build the format
    # the trainer actually validates against; build the canonical governance
    # manifest as a separate, additional audit artifact below.
    import hashlib

    import soundfile as sf
    from amazwi_ml.manifest import ManifestRecord, build_manifest, write_immutable_manifest
    from datasets import load_dataset  # noqa: E402
    from huggingface_hub import dataset_info  # noqa: E402

    # Swivuriso is a gated HF dataset -- needs an HF token. Read it from a
    # Kaggle Secret (added via the kernel editor's Add-ons > Secrets, never
    # typed into this script or committed anywhere) rather than embedding a
    # token in code. Fails loudly and specifically if it's not attached,
    # rather than proceeding unauthenticated and hitting a confusing
    # DatasetNotFoundError deep inside `datasets`.
    try:
        from kaggle_secrets import UserSecretsClient

        hf_token = UserSecretsClient().get_secret("HF_TOKEN")
    except Exception as exc:  # noqa: BLE001 - want the real reason surfaced, not swallowed
        raise RuntimeError(
            "Could not read the HF_TOKEN Kaggle Secret. Attach it via this kernel's "
            "Add-ons > Secrets menu (label must be exactly HF_TOKEN) before running. "
            f"Underlying error: {exc}"
        ) from exc
    from huggingface_hub import login as hf_login

    hf_login(token=hf_token)

    info = dataset_info(DATASET_REPO, token=hf_token)
    exact_revision = info.sha
    print(f"Resolved exact dataset revision: {exact_revision}", flush=True)

    audio_dir = Path("/kaggle/working/audio")
    audio_dir.mkdir(parents=True, exist_ok=True)

    trainer_records: list[dict] = []
    governance_records: list[ManifestRecord] = []
    for lang in LANGUAGES:
        ds = load_dataset(DATASET_REPO, lang, split=SPLIT, revision=exact_revision, token=hf_token)
        for i, row in enumerate(ds):
            audio = row["audio"]
            out_path = audio_dir / f"{lang}_{SPLIT}_{i:06d}.wav"
            sf.write(str(out_path), audio["array"], audio["sampling_rate"])
            audio_sha = hashlib.sha256(out_path.read_bytes()).hexdigest()
            record_id = f"{lang}-{SPLIT}-{i:06d}"
            trainer_records.append(
                {
                    "record_id": record_id,
                    "text": row["transcript"],
                    "audio_path": str(out_path),
                    "split": "train",  # dev split used as the bounded overnight fine-tune set
                    "excluded": False,
                }
            )
            governance_records.append(
                ManifestRecord(
                    record_id=record_id,
                    source_id=str(row.get("audio_id", i)),
                    speaker_id=row.get("recorder_uuid"),
                    text=row["transcript"],
                    language=lang,
                    source_class="SWIVURISO_DEV_SPLIT",
                    split="train",
                    domain=row.get("domain"),
                    audio_sha256=audio_sha,
                    consent_version="swivuriso-cc-by-4.0",
                )
            )

    # Governance/audit artifact -- the immutable, hash-verified record of
    # exactly what data this run touched. Not read by train_asr.py directly.
    governance_manifest = build_manifest(
        governance_records,
        generated_at="__RUNTIME__",
        dataset_id="swivuriso-zul-tsn-dev",
        dataset_version="1",
        source_repository=DATASET_REPO,
        source_revision=exact_revision,
        licence="CC-BY-4.0",
        restrictions=("ASR_ONLY", "NO_TTS", "NO_VOICE_CLONING", "NO_SPEECH_SYNTHESIS", "NO_HUMAN_VOICE_REPLICATION"),
        allowed_tasks=("ASR_TRAINING", "ASR_EVALUATION"),
        language="zul+tsn",
    )
    governance_path = Path("/kaggle/working/governance_manifest.json")
    governance_sha = write_immutable_manifest(governance_manifest, governance_path)
    print(f"Governance manifest: {len(governance_records)} records, sha256={governance_sha}", flush=True)

    # The file train_asr.py actually reads and hash-checks.
    manifest_path = Path("/kaggle/working/manifest.json")
    manifest_path.write_text(
        json.dumps({"records": trainer_records}, indent=2, sort_keys=True), encoding="utf-8"
    )
    manifest_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    print(f"Trainer manifest: {len(trainer_records)} records, sha256={manifest_sha}", flush=True)

    preflight = ml_dir / "preflight_swivuriso.json"
    budget = ml_dir / "budget.json"
    run_id = f"kaggle-overnight-{exact_revision[:8]}"

    config = {"candidate": CANDIDATE, "model_revision": MODEL_REVISION, "epochs": 3, "batch_size": 8}
    config_path = Path("/kaggle/working/run_config.json")
    config_path.write_text(json.dumps(config, sort_keys=True), encoding="utf-8")
    config_sha = hashlib.sha256(config_path.read_bytes()).hexdigest()

    sh(
        [
            sys.executable,
            "reserve_run.py",
            "--ledger",
            str(budget),
            "--reserve",
            "--run-id",
            run_id,
            "--account-alias",
            "team-sonar-a",
            "--phase",
            "ISIZULU_ADAPTATION",
            "--requested-hours",
            "10",
            "--manifest-sha256",
            manifest_sha,
            "--config-sha256",
            config_sha,
        ],
        cwd=ml_dir,
    )

    sh(
        [
            sys.executable,
            "train_asr.py",
            "--candidate-id",
            CANDIDATE,
            "--manifest",
            str(manifest_path),
            "--manifest-sha256",
            manifest_sha,
            "--dataset-revision",
            exact_revision,
            "--preflight-evidence",
            str(preflight),
            "--model-revision",
            MODEL_REVISION,
            "--reservation",
            run_id,
            "--output-dir",
            "/kaggle/working/output",
            "--run-id",
            run_id,
            "--batch-size",
            "8",
            "--epochs",
            "3",
        ],
        cwd=ml_dir,
    )
    print("Training run complete. Checkpoint at /kaggle/working/output/checkpoint", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
