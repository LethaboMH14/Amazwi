from __future__ import annotations
import argparse
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Reserve campaign GPU hours without starting a workload")
    parser.add_argument("--ledger", default="kaggle/budget.json")
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args(argv)
    if args.show:
        print(Path(args.ledger).read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
