import argparse,hashlib,json
from pathlib import Path
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument("--output",required=True);p.add_argument("paths",nargs="*");a=p.parse_args(argv);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);items={str(Path(x)):hashlib.sha256(Path(x).read_bytes()).hexdigest() for x in sorted(a.paths)};out.write_text(json.dumps({"artefacts":items},sort_keys=True,separators=(",",":"))+"\n");return 0
if __name__=="__main__":raise SystemExit(main())
