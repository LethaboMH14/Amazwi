import argparse,json
from amazwi_ml.tabular import train_quality_challengers,train_mission_challengers
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument("--task",choices=["QUALITY_RISK","MISSION_RANKING"],required=True);p.add_argument("--seed",type=int,required=True);p.add_argument("--output",required=True);a=p.parse_args(argv);rows=[];runs=train_quality_challengers(rows,rows,seed=a.seed) if a.task=="QUALITY_RISK" else train_mission_challengers(rows,rows,seed=a.seed);open(a.output,"w",encoding="utf-8").write(json.dumps([r.__dict__ for r in runs],default=str,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
