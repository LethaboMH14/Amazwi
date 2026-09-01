"""Package a governed Kaggle run without embedding credentials."""
from __future__ import annotations

import argparse
from pathlib import Path


def package_run(paths: list[Path], output: Path) -> str:
    from amazwi_ml.evidence import write_evidence_index

    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise ValueError(f"artefact is missing: {missing[0]}")
    return write_evidence_index(paths, output)


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package hashes for a governed campaign run")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--metrics", type=Path, required=True)
    parser.add_argument("--logs", type=Path, required=True)
    parser.add_argument("--environment-lock", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    output = args.output_dir / f"{args.run_id}-evidence-index.json"
    package_run(
        [args.config, args.checkpoint, args.predictions, args.metrics, args.logs, args.environment_lock],
        output,
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
