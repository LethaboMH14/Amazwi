"""Audited administrative release of one stuck Council outbox event."""
import argparse, os, uuid
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.outbox import release_event_for_admin_retry

def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--event-id",required=True); parser.add_argument("--reason",required=True); args=parser.parse_args()
    url=os.environ.get("AMAZWI_DATABASE_URL"); actor=os.environ.get("AMAZWI_ADMIN_ACTOR_ID")
    if not url or not actor: parser.error("AMAZWI_DATABASE_URL and AMAZWI_ADMIN_ACTOR_ID are required")
    engine=create_engine(url)
    with Session(engine) as session: release_event_for_admin_retry(session,uuid.UUID(args.event_id),uuid.UUID(actor),args.reason,datetime.now(timezone.utc))
    return 0
if __name__ == "__main__": raise SystemExit(main())
