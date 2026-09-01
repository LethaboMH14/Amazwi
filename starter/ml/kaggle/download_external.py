"""Validate external preflight before any network client can be imported."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from amazwi_ml.external import PreflightRequired, TaskProhibited, PreflightEvidence, load_registry, require_download_preflight


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path(__file__).parents[1] / "registry" / "external_datasets.yaml")
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--dataset", dest="dataset_id", required=True)
    parser.add_argument("--task", dest="intended_task", required=True)
    parser.add_argument("--destination", type=Path, default=Path("external-data"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    registry = load_registry(args.registry)
    evidence = None
    if args.evidence:
        try:
            evidence = PreflightEvidence(**json.loads(args.evidence.read_text(encoding="utf-8")))
        except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
            print(f"PREFLIGHT_REQUIRED: invalid evidence ({exc})", file=sys.stderr)
            return 2
    try:
        spec = require_download_preflight(registry, evidence, dataset_id=args.dataset_id, intended_task=args.intended_task)
    except (PreflightRequired, TaskProhibited) as exc:
        print(f"PREFLIGHT_REQUIRED: {exc}", file=sys.stderr)
        return 2
    if args.dry_run:
        revision = evidence.exact_revision if evidence else ""
        print(f"dataset={spec.dataset_id} revision={revision} task={args.intended_task} destination={args.destination} registry_sha256={registry.registry_sha256}")
        return 0
    print("Network download is intentionally not implemented in the CPU-safe scaffold.", file=sys.stderr)
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
