import argparse,json
from pathlib import Path
from amazwi_ml.budget import reserve_gpu_run
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument("--ledger",required=True);p.add_argument("--show",action="store_true");p.add_argument("--run-id");p.add_argument("--account");p.add_argument("--phase");p.add_argument("--hours",type=float);p.add_argument("--manifest");p.add_argument("--config");a=p.parse_args(argv)
 if a.show:print(Path(a.ledger).read_text());return 0
 print(json.dumps(reserve_gpu_run(Path(a.ledger),run_id=a.run_id,account_alias=a.account,phase=a.phase,requested_hours=a.hours,manifest_sha256=a.manifest,config_sha256=a.config)));return 0
if __name__=="__main__":raise SystemExit(main())
