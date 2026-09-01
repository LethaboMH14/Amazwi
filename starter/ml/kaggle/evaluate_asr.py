from __future__ import annotations
import argparse

def main(argv=None):
    parser = argparse.ArgumentParser(description="CPU-safe ASR evaluation entry point")
    parser.add_argument("--seed", type=int, default=20260901); parser.add_argument("--manifest"); parser.add_argument("--manifest-sha256"); parser.add_argument("--config"); parser.add_argument("--output-dir"); parser.add_argument("--run-id"); parser.add_argument("--budget-reservation")
    parser.parse_args(argv)
    parser.parse_args(argv)
    return 0
if __name__ == "__main__": raise SystemExit(main())
