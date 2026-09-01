from __future__ import annotations
import argparse

def main(argv=None):
    parser = argparse.ArgumentParser(description="Package hashes for a governed campaign run")
    parser.add_argument("--config"); parser.add_argument("--checkpoint"); parser.add_argument("--predictions"); parser.add_argument("--metrics"); parser.add_argument("--logs"); parser.add_argument("--environment-lock"); parser.add_argument("--output-dir"); parser.add_argument("--run-id")
    parser.parse_args(argv)
    parser.parse_args(argv)
    return 0
if __name__ == "__main__": raise SystemExit(main())
