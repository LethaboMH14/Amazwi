"""Clear the verifier queue so a demo starts from a clean slate.

Why this exists
---------------
The verifier queue is served OLDEST FIRST, which is correct -- the
speaker who has waited longest should be heard first, not buried under
newer clips. But it means anything stale at the head of the queue blocks
everything behind it: a laptop only ever takes item #1.

During development that bit hard. Scripted test clips created through
the API sat at the head of the queue, and three genuine phone recordings
made minutes later sat behind them, invisible. The symptom was "the live
recordings are not landing on the laptops" when in fact they had landed
and were queued behind a synthetic one.

Two modes:

    --synthetic-only   remove only scripted test clips (audio/wav + pcm),
                       leaving every real phone recording untouched.
                       This is the safe default.

    --all-pending      remove every unresolved contribution, real or not,
                       for a completely clean demo take. Resolved
                       contributions are NEVER touched, so the leaderboard,
                       the ledger and the impact figures survive.

Real recordings are identified by their container: a browser MediaRecorder
take is audio/webm (or ogg) with an irregular duration, while scripted
clips in this repo are pcm WAV at a round number of milliseconds. That is
a heuristic, so --all-pending exists for when you want certainty rather
than cleverness.

Demo-only. Guarded by AMAZWI_ALLOW_DEMO_RESET, matching seed_demo.py.
"""
from __future__ import annotations

import argparse
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

RESET_GUARD_ENV = "AMAZWI_ALLOW_DEMO_RESET"

# A scripted clip in this repo is always written as pcm WAV. A real
# MediaRecorder take from a browser is webm or ogg.
SYNTHETIC_PREDICATE = "a.mime_type = 'audio/wav' AND a.codec = 'pcm'"

# Never delete a contribution that has already been resolved: the reward
# ledger, the leaderboard and the impact aggregates all read from it, and
# removing one would silently rewrite the demo's own history.
UNRESOLVED_PREDICATE = """
    c.id NOT IN (SELECT contribution_id FROM eligibility_decisions)
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--synthetic-only", action="store_true", default=True)
    mode.add_argument("--all-pending", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.dry_run and os.environ.get(RESET_GUARD_ENV, "").lower() != "true":
        print(f"refusing: set {RESET_GUARD_ENV}=true to confirm, or use --dry-run")
        return 2

    url = os.environ.get("AMAZWI_DATABASE_URL")
    if not url:
        print("AMAZWI_DATABASE_URL is required")
        return 2

    where = UNRESOLVED_PREDICATE
    if not args.all_pending:
        where += f" AND {SYNTHETIC_PREDICATE}"

    engine = create_engine(url)
    with Session(engine) as session:
        rows = session.execute(
            text(
                f"""
                SELECT c.id, c.declared_language, c.duration_ms, a.mime_type, a.codec
                FROM contributions c
                JOIN audio_objects a ON a.contribution_id = c.id
                WHERE {where}
                ORDER BY c.created_at
                """
            )
        ).fetchall()

        if not rows:
            print("nothing to clear -- the queue holds no matching contributions")
            return 0

        label = "ALL pending" if args.all_pending else "scripted (pcm WAV)"
        print(f"{label} contributions to remove: {len(rows)}")
        for row in rows:
            print(f"  {str(row[0])[:8]}  {row[1]}  {row[2]}ms  {row[3]}/{row[4]}")

        if args.dry_run:
            print("\ndry run -- nothing was deleted")
            return 0

        ids = [row[0] for row in rows]
        # Order matters: children before parents, or the FKs refuse.
        for table in (
            "assignments",
            "audio_objects",
            "reward_events",
            "eligibility_decisions",
        ):
            session.execute(
                text(f"DELETE FROM {table} WHERE contribution_id = ANY(:ids)"),
                {"ids": ids},
            )
        session.execute(
            text("DELETE FROM contributions WHERE id = ANY(:ids)"), {"ids": ids}
        )
        session.commit()

    print(f"\ncleared {len(rows)} contribution(s). Resolved history untouched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
