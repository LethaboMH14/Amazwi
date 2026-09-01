from pathlib import Path
import importlib.util
import subprocess
import sys

import pytest


ROOT = Path(__file__).parents[1]


def _load_entrypoint(name):
    path = ROOT / "kaggle" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"local_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


train_asr = _load_entrypoint("train_asr")
evaluate_asr = _load_entrypoint("evaluate_asr")


def test_kaggle_entrypoints_expose_help_without_side_effects():
    for name in ("reserve_run.py", "train_asr.py", "evaluate_asr.py", "package_run.py"):
        result = subprocess.run([sys.executable, str(ROOT / "kaggle" / name), "--help"], cwd=ROOT, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert "usage:" in result.stdout.lower()


def test_budget_json_declares_locked_allocations():
    import json
    data = json.loads((ROOT / "kaggle" / "budget.json").read_text(encoding="utf-8"))
    assert data["aggregate_cap_hours"] == 60
    assert data["account_cap_hours"] == 30
    assert data["phase_caps_hours"]["FIXED_TOURNAMENT"] == 8


def test_training_inputs_require_manifest_hash_model_revision_and_reservation(tmp_path):
    manifest = tmp_path / "evaluation.json"
    manifest.write_text("{}", encoding="utf-8")
    args = train_asr.parse_train_args(
        [
            "--candidate-id", "whisper-large-v3-turbo-peft",
            "--manifest", str(manifest),
            "--manifest-sha256", "a" * 64,
            "--dataset-revision", "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
            "--preflight-evidence", str(tmp_path / "preflight.json"),
            "--model-revision", "openai/whisper-large-v3-turbo",
            "--reservation", "reservation-1",
            "--output-dir", str(tmp_path / "out"),
            "--run-id", "run-1",
        ]
    )
    with pytest.raises(ValueError, match="manifest sha256"):
        train_asr.validate_training_inputs(args)


def test_evaluation_inputs_reject_missing_checkpoint(tmp_path):
    manifest = tmp_path / "evaluation.json"
    manifest.write_text("{}", encoding="utf-8")
    args = evaluate_asr.parse_evaluate_args(
        [
            "--manifest", str(manifest),
            "--manifest-sha256", "a" * 64,
            "--dataset-revision", "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
            "--preflight-evidence", str(tmp_path / "preflight.json"),
            "--checkpoint", str(tmp_path / "missing"),
            "--model-revision", "openai/whisper-large-v3-turbo",
            "--output-dir", str(tmp_path / "out"),
            "--run-id", "run-1",
        ]
    )
    with pytest.raises(ValueError, match="checkpoint"):
        evaluate_asr.validate_evaluation_inputs(args)


def test_evaluation_inputs_reject_manifest_hash_mismatch(tmp_path):
    manifest = tmp_path / "evaluation.json"
    manifest.write_text("{}", encoding="utf-8")
    checkpoint = tmp_path / "checkpoint"
    checkpoint.mkdir()
    args = evaluate_asr.parse_evaluate_args(
        [
            "--manifest", str(manifest),
            "--manifest-sha256", "a" * 64,
            "--dataset-revision", "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
            "--preflight-evidence", str(tmp_path / "preflight.json"),
            "--checkpoint", str(checkpoint),
            "--model-revision", "openai/whisper-large-v3-turbo",
            "--output-dir", str(tmp_path / "out"),
            "--run-id", "run-1",
        ]
    )
    with pytest.raises(ValueError, match="manifest sha256"):
        evaluate_asr.validate_evaluation_inputs(args)


def test_training_rejects_comparator_until_its_adapter_exists(tmp_path):
    manifest = tmp_path / "evaluation.json"
    manifest.write_text("[]", encoding="utf-8")
    args = train_asr.parse_train_args(
        [
            "--candidate-id", "xls-r-mms-comparator",
            "--manifest", str(manifest),
            "--manifest-sha256", "a" * 64,
            "--dataset-revision", "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
            "--preflight-evidence", str(tmp_path / "preflight.json"),
            "--model-revision", "facebook/wav2vec2-xls-r-300m",
            "--reservation", "reservation-1",
            "--output-dir", str(tmp_path / "out"),
            "--run-id", "run-1",
        ]
    )
    with pytest.raises(ValueError, match="supports whisper"):
        train_asr.validate_training_inputs(args)
