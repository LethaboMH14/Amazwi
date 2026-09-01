"""Reserve and complete Kaggle GPU hours through the governed ledger."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage governed campaign GPU-hour reservations")
    parser.add_argument("--ledger", type=Path, default=Path("kaggle/budget.json"))
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--reserve", action="store_true")
    parser.add_argument("--complete", action="store_true")
    parser.add_argument("--run-id")
    parser.add_argument("--account-alias", choices=["team-sonar-a", "team-sonar-b"])
    parser.add_argument("--phase", choices=["PREFLIGHT_SPLITS", "FIXED_TOURNAMENT", "ISIZULU_ADAPTATION", "SETSWANA_ADAPTATION", "TABULAR_CHALLENGERS", "REPRODUCIBILITY"])
    parser.add_argument("--requested-hours", type=float)
    parser.add_argument("--actual-hours", type=float)
    parser.add_argument("--manifest-sha256")
    parser.add_argument("--config-sha256")
    parser.add_argument("--artefact-sha256")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    if args.show:
        print(args.ledger.read_text(encoding="utf-8"))
        return 0
    from amazwi_ml.budget import complete_gpu_run, reserve_gpu_run

    if args.reserve:
        required = (args.run_id, args.account_alias, args.phase, args.requested_hours, args.manifest_sha256, args.config_sha256)
        if any(value is None for value in required):
            raise SystemExit("--reserve requires run, account, phase, requested-hours, manifest-sha256, and config-sha256")
        result = reserve_gpu_run(args.ledger, run_id=args.run_id, account_alias=args.account_alias, phase=args.phase, requested_hours=args.requested_hours, manifest_sha256=args.manifest_sha256, config_sha256=args.config_sha256)
        print(json.dumps(result.__dict__, sort_keys=True))
        return 0
    if args.complete:
        required = (args.run_id, args.actual_hours, args.artefact_sha256)
        if any(value is None for value in required):
            raise SystemExit("--complete requires run-id, actual-hours, and artefact-sha256")
        result = complete_gpu_run(args.ledger, run_id=args.run_id, actual_gpu_hours=args.actual_hours, artefact_sha256=args.artefact_sha256)
        print(json.dumps(result.__dict__, sort_keys=True))
        return 0
    raise SystemExit("choose --show, --reserve, or --complete")


if __name__ == "__main__":
    raise SystemExit(main())
