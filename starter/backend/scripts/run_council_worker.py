"""One-shot recoverable Council worker; disabled mode is a no-op.

`process_once` is separated from `main` so the leasing/retry/exhaustion
behaviour can be driven directly by tests against a real session, instead
of only through a process entrypoint that needs env vars and an engine.
"""
import argparse, os
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.config import AI_COUNCIL_ENABLED, AI_COUNCIL_MAX_ATTEMPTS
from app.outbox import claim_events, complete_event, exhaust_event, retry_event
from app.council import DataStewardRulesV1, SoundSentinelRulesV1, LanguageScoutRulesV1, ExplainerRulesV1, run_council_event

SPECIALISTS = (DataStewardRulesV1, SoundSentinelRulesV1, LanguageScoutRulesV1, ExplainerRulesV1)


def process_once(session: Session, *, worker_id: str, batch_size: int, now: datetime,
                 max_attempts: int = AI_COUNCIL_MAX_ATTEMPTS, runner=run_council_event) -> int:
    """Claim up to batch_size events and run the Council over each.

    Returns the number of events claimed. A failing event is retried with a
    deterministic backoff until its attempt_count reaches max_attempts, at
    which point it is terminally exhausted rather than retried forever --
    which is what the previous version did, leaving AI_COUNCIL_MAX_ATTEMPTS
    as dead config and the API's FAILED state unreachable.
    """
    events = claim_events(session, worker_id=worker_id, now=now, limit=batch_size)
    specialists = [cls() for cls in SPECIALISTS]
    for event in events:
        try:
            runner(session, event, specialists, now)
            complete_event(session, event.id, worker_id, now)
        except Exception as exc:
            if event.attempt_count >= max_attempts:
                exhaust_event(session, event.id, worker_id, now)
            else:
                retry_event(session, event.id, worker_id, now, str(exc))
    return len(events)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--once", action="store_true")
    p.add_argument("--worker-id", default="council-worker")
    p.add_argument("--batch-size", type=int, default=10)
    p.add_argument("--poll-seconds", type=int, default=5)
    a = p.parse_args()
    if not AI_COUNCIL_ENABLED:
        return 0
    url = os.environ.get("AMAZWI_DATABASE_URL")
    if not url:
        p.error("AMAZWI_DATABASE_URL is required")
    engine = create_engine(url)
    with Session(engine) as s:
        process_once(s, worker_id=a.worker_id, batch_size=a.batch_size, now=datetime.now(timezone.utc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
