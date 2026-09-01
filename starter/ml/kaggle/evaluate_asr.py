import argparse
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument("--manifest",required=True);p.add_argument("--predictions",required=True);p.add_argument("--output",required=True);p.parse_args(argv);print("EVALUATION_ONLY: no network access");return 0
if __name__=="__main__":raise SystemExit(main())
