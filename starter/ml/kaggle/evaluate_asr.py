"""Gated ASR evaluation entry point with lazy heavyweight dependencies."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def parse_evaluate_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gated ASR evaluation entry point; execution requires explicit approvals"
    )
    parser.add_argument("--seed", type=int, default=20260901)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--dataset-revision", required=True)
    parser.add_argument("--preflight-evidence", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--model-revision", required=True)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--reservation", "--budget-reservation", dest="reservation")
    return parser.parse_args(argv)


def validate_evaluation_inputs(args: argparse.Namespace) -> None:
    if not args.checkpoint.exists():
        raise ValueError("checkpoint is required")
    if not args.manifest.is_file():
        raise ValueError("manifest file is required")
    expected_hash = args.manifest_sha256.strip().lower()
    if len(expected_hash) != 64 or any(char not in "0123456789abcdef" for char in expected_hash):
        raise ValueError("manifest sha256 must be a 64-character hexadecimal digest")
    if _sha256(args.manifest) != expected_hash:
        raise ValueError("manifest sha256 does not match file")
    if args.dataset_revision.strip().lower() in {"main", "master", "latest"}:
        raise ValueError("an immutable dataset revision is required")
    if not args.preflight_evidence.is_file():
        raise ValueError("preflight evidence is required")
    if not args.model_revision.strip():
        raise ValueError("model revision is required")
    if args.seed < 0:
        raise ValueError("seed must be non-negative")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_evaluation(args: argparse.Namespace) -> Path:
    """Generate predictions and governed ASR metrics from a saved checkpoint."""
    validate_evaluation_inputs(args)
    value = json.loads(args.manifest.read_text(encoding="utf-8"))
    rows = value.get("records", value) if isinstance(value, dict) else value
    eval_rows = [row for row in rows if row.get("split") in {"dev", "test", "evaluation"} and not row.get("excluded")]
    if not eval_rows:
        raise ValueError("manifest has no included evaluation records")
    if any(not row.get("text") or not row.get("audio_path") for row in eval_rows):
        raise ValueError("every evaluation record requires text and audio_path")
    missing = [row["audio_path"] for row in eval_rows if not Path(row["audio_path"]).is_file()]
    if missing:
        raise ValueError(f"audio files are missing: {missing[0]}")

    try:
        import torch
        from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
    except ImportError as exc:
        raise RuntimeError(
            "Kaggle evaluation dependencies are required; install requirements-kaggle.txt"
        ) from exc

    processor = AutoProcessor.from_pretrained(args.checkpoint)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(args.checkpoint)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()
    predictions = []
    from amazwi_ml.metrics import AsrCase, TokenSpan, evaluate_asr

    for row in eval_rows:
        import soundfile as sf

        audio, sample_rate = sf.read(row["audio_path"])
        inputs = processor(audio, sampling_rate=sample_rate, return_tensors="pt")
        inputs = {key: value.to(device) for key, value in inputs.items()}
        with torch.no_grad():
            generated = model.generate(**inputs)
        hypothesis = processor.batch_decode(generated, skip_special_tokens=True)[0]
        predictions.append({"case_id": row["record_id"], "reference": row["text"], "hypothesis": hypothesis})

    cases = [
        AsrCase(
            case_id=item["case_id"],
            reference=item["reference"],
            hypothesis=item["hypothesis"],
            language=str(row.get("language", "unknown")),
            speaker_id=str(row.get("speaker_id", "unknown")),
            domain=str(row.get("domain", "unknown")),
            acoustic_condition=str(row.get("acoustic_condition", "unknown")),
            spans=tuple(TokenSpan(**span) for span in row.get("spans", [])),
        )
        for item, row in zip(predictions, eval_rows)
    ]
    report = evaluate_asr(cases)
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    predictions_path = output / "predictions.json"
    metrics_path = output / "metrics.json"
    predictions_path.write_text(json.dumps(predictions, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    metrics_path.write_text(
        json.dumps(
            {
                "run_id": args.run_id,
                "candidate_id": args.model_revision,
                "evaluation_manifest_sha256": args.manifest_sha256,
                "prediction_sha256": _sha256(predictions_path),
                "case_count": report.case_count,
                "slices": [slice_.__dict__ for slice_ in report.slices],
            },
            sort_keys=True,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return metrics_path


def main(argv=None) -> int:
    args = parse_evaluate_args(argv)
    run_evaluation(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
