"""Create reviewed external-source evidence without downloading bytes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from amazwi_ml.external import approve_preflight, load_registry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--dataset", dest="dataset_id", required=True)
    parser.add_argument("--revision", dest="exact_revision", required=True)
    parser.add_argument("--task", dest="intended_task", required=True)
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--reviewed-at", required=True)
    parser.add_argument("--terms-accepted", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        evidence = approve_preflight(load_registry(args.registry), dataset_id=args.dataset_id,
            exact_revision=args.exact_revision, intended_task=args.intended_task,
            reviewer=args.reviewer, reviewed_at=args.reviewed_at,
            terms_accepted=args.terms_accepted)
    except PermissionError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence.model_dump(), sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
