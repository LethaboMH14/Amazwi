"""CPU-safe placeholder: validates campaign inputs without downloading models."""
import argparse
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument("--candidate",choices=["whisper-large-v3-turbo-peft","w2v-bert-2-african","xls-r-mms-comparator"],required=True);p.add_argument("--manifest",required=True);p.add_argument("--output",required=True);p.add_argument("--seed",type=int,required=True);p.parse_args(argv);print("PREFLIGHT_ONLY: no model or dataset download performed");return 0
if __name__=="__main__":raise SystemExit(main())
