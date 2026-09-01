from __future__ import annotations
import argparse

def main(argv=None):
    parser = argparse.ArgumentParser(description="CPU-safe ASR campaign entry point; model execution is explicit and opt-in")
    parser.add_argument("--candidate-id", choices=["whisper-large-v3-turbo-peft", "w2v-bert-2-african", "xls-r-mms-comparator"])
    parser.add_argument("--seed", type=int, default=20260901); parser.add_argument("--manifest"); parser.add_argument("--config"); parser.add_argument("--output-dir"); parser.add_argument("--run-id"); parser.add_argument("--budget-reservation")
    parser.parse_args(argv)
    parser.parse_args(argv)
    return 0
if __name__ == "__main__": raise SystemExit(main())
