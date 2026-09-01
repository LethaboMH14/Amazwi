"""Gated ASR training entry point.

Heavy Transformers imports are deliberately deferred until a validated Kaggle
run is explicitly requested.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path


CANDIDATES = (
    "whisper-large-v3-turbo-peft",
    "w2v-bert-2-african",
    "xls-r-mms-comparator",
)


def parse_train_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gated ASR training entry point; execution requires explicit approvals"
    )
    parser.add_argument("--candidate-id", choices=CANDIDATES, required=True)
    parser.add_argument("--seed", type=int, default=20260901)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--dataset-revision", required=True)
    parser.add_argument("--preflight-evidence", type=Path, required=True)
    parser.add_argument("--model-revision", required=True)
    parser.add_argument("--reservation", "--budget-reservation", dest="reservation", required=True)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=2)
    parser.add_argument("--learning-rate", type=float, default=1e-5)
    parser.add_argument("--epochs", type=float, default=3.0)
    parser.add_argument("--max-steps", type=int, default=-1)
    parser.add_argument("--resume-from-checkpoint")
    return parser.parse_args(argv)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_training_inputs(args: argparse.Namespace) -> None:
    if args.candidate_id not in CANDIDATES:
        raise ValueError("unsupported training candidate")
    if not args.manifest.is_file():
        raise ValueError("manifest file is required")
    if args.manifest_sha256 != _sha256(args.manifest):
        raise ValueError("manifest sha256 does not match")
    if args.dataset_revision.strip().lower() in {"main", "master", "latest"}:
        raise ValueError("an immutable dataset revision is required")
    if not args.preflight_evidence.is_file():
        raise ValueError("preflight evidence is required")
    if not args.model_revision.strip():
        raise ValueError("model revision is required")
    if not args.reservation.strip():
        raise ValueError("budget reservation is required")
    if args.seed < 0:
        raise ValueError("seed must be non-negative")


def _records(path: Path) -> list[dict]:
    value = json.loads(path.read_text(encoding="utf-8"))
    rows = value.get("records", value) if isinstance(value, dict) else value
    if not isinstance(rows, list) or not rows:
        raise ValueError("manifest must contain a non-empty records list")
    return rows


def run_training(args: argparse.Namespace) -> Path:
    """Run a real Kaggle-side speech fine-tune after all gates pass.

    The heavyweight imports are intentionally inside this function so local
    help, refusal tests, and documentation checks remain CPU-safe.
    """
    validate_training_inputs(args)
    rows = _records(args.manifest)
    train_rows = [row for row in rows if row.get("split") == "train" and not row.get("excluded")]
    if not train_rows:
        raise ValueError("manifest has no included train records")
    if any(not row.get("text") or not row.get("audio_path") for row in train_rows):
        raise ValueError("every train record requires text and audio_path")
    missing = [row["audio_path"] for row in train_rows if not Path(row["audio_path"]).is_file()]
    if missing:
        raise ValueError(f"audio files are missing: {missing[0]}")

    try:
        import numpy as np
        import torch
        from datasets import Audio, Dataset
        from transformers import (
            AutoModelForCTC,
            AutoProcessor,
            Seq2SeqTrainer,
            Seq2SeqTrainingArguments,
            WhisperForConditionalGeneration,
            WhisperProcessor,
        )
    except ImportError as exc:
        raise RuntimeError(
            "Kaggle training dependencies are required; install requirements-kaggle.txt"
        ) from exc

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)

    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    dataset = Dataset.from_list(
        [{"audio": row["audio_path"], "sentence": row["text"]} for row in train_rows]
    ).cast_column("audio", Audio(sampling_rate=16000))
    is_whisper = args.candidate_id == "whisper-large-v3-turbo-peft"
    if is_whisper:
        processor = WhisperProcessor.from_pretrained(args.model_revision)
        model = WhisperForConditionalGeneration.from_pretrained(args.model_revision)
        model.config.forced_decoder_ids = None
        model.config.suppress_tokens = []
    else:
        processor = AutoProcessor.from_pretrained(args.model_revision)
        model = AutoModelForCTC.from_pretrained(args.model_revision)

    def prepare(batch):
        audio = batch["audio"]
        if is_whisper:
            batch["model_inputs"] = processor.feature_extractor(
                audio["array"], sampling_rate=audio["sampling_rate"]
            ).input_features[0]
            batch["labels"] = processor.tokenizer(batch["sentence"]).input_ids
        else:
            batch["model_inputs"] = processor(
                audio["array"], sampling_rate=audio["sampling_rate"]
            ).input_values[0]
            batch["labels"] = processor.tokenizer(batch["sentence"]).input_ids
        return batch

    dataset = dataset.map(prepare, remove_columns=dataset.column_names)

    class Collator:
        def __call__(self, features):
            inputs = torch.tensor([item["model_inputs"] for item in features], dtype=torch.float32)
            labels = processor.tokenizer.pad(
                [{"input_ids": item["labels"]} for item in features], return_tensors="pt"
            ).input_ids
            labels = labels.masked_fill(labels == processor.tokenizer.pad_token_id, -100)
            return {"input_features" if is_whisper else "input_values": inputs, "labels": labels}

    training = Seq2SeqTrainingArguments(
        output_dir=str(output / "checkpoint"),
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        num_train_epochs=args.epochs,
        max_steps=args.max_steps,
        fp16=torch.cuda.is_available(),
        logging_steps=10,
        save_strategy="steps",
        save_steps=250,
        save_total_limit=2,
        report_to=[],
        seed=args.seed,
        remove_unused_columns=False,
    )
    trainer = Seq2SeqTrainer(
        model=model,
        args=training,
        train_dataset=dataset,
        data_collator=Collator(),
        tokenizer=processor.feature_extractor if is_whisper else processor.tokenizer,
    )
    trainer.train(resume_from_checkpoint=args.resume_from_checkpoint)
    trainer.save_model(str(output / "checkpoint"))
    processor.save_pretrained(str(output / "checkpoint"))
    (output / "run.json").write_text(
        json.dumps(
            {
                "run_id": args.run_id,
                "candidate_id": args.candidate_id,
                "model_revision": args.model_revision,
                "manifest_sha256": args.manifest_sha256,
                "reservation": args.reservation,
                "seed": args.seed,
                "train_records": len(train_rows),
                "status": "TRAINED",
            },
            sort_keys=True,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return output / "checkpoint"


def main(argv=None) -> int:
    args = parse_train_args(argv)
    run_training(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
