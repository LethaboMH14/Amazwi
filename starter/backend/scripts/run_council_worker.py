"""One-shot recoverable Council worker; disabled mode is a no-op."""
import argparse, os
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.config import AI_COUNCIL_ENABLED
from app.outbox import claim_events, complete_event, retry_event
from app.council import DataStewardRulesV1, SoundSentinelRulesV1, LanguageScoutRulesV1, ExplainerRulesV1, run_council_event

def main():
    p=argparse.ArgumentParser(); p.add_argument("--once",action="store_true"); p.add_argument("--worker-id",default="council-worker"); p.add_argument("--batch-size",type=int,default=10); p.add_argument("--poll-seconds",type=int,default=5); a=p.parse_args()
    if not AI_COUNCIL_ENABLED: return 0
    url=os.environ.get("AMAZWI_DATABASE_URL");
    if not url: p.error("AMAZWI_DATABASE_URL is required")
    engine=create_engine(url); now=datetime.now(timezone.utc)
    with Session(engine) as s:
        events=claim_events(s,worker_id=a.worker_id,now=now,limit=a.batch_size)
        specialists=[DataStewardRulesV1(),SoundSentinelRulesV1(),LanguageScoutRulesV1(),ExplainerRulesV1()]
        for event in events:
            try: run_council_event(s,event,specialists,now); complete_event(s,event.id,a.worker_id,now)
            except Exception as exc: retry_event(s,event.id,a.worker_id,now,str(exc))
    return 0
if __name__=="__main__": raise SystemExit(main())
