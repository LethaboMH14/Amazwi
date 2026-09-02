"""Aggregate, privacy-thresholded coverage for the Impact Map.

HONEST DATA LIMITATION -- read before extending this module.

Plan 03 Task 7 specifies coverage cells keyed by (language, province,
domain). The real schema in `app/models.py` has **no geographic column
anywhere** -- not on `users`, not on `contributions`, not on `campaigns`
-- and no `domain` vocabulary either. Rather than fabricate a location
field, this module aggregates over what the database actually holds:

    declared language  x  funding campaign

`province_code` is therefore `None` on every node this code can produce
today, and `ImpactResponse.geography_available` is `False`. The response
schema keeps the province slot so that a future migration adding a real,
consented, coarse province field needs no contract change -- and so the
UI can render the flat South Africa outline with an explicit "national
totals only" state instead of pretending to place pins.

`model_gap_percent` is likewise always `None`: there is no signed,
active model-evaluation record in this database (model metrics live in
`starter/ml`, unlinked). The UI shows "Model evidence unavailable"
rather than inferring readiness.

Privacy rules enforced here, not in the UI:
- A cell is published only when it has >= MIN_CELL_SIZE (5) committed,
  peer-verified, corpus-eligible contributions.
- Published counts are bands, never exact counts.
- No user id, contribution id, coordinate, audio key, or transcript ever
  leaves this module.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api_types import CoverageNodeResponse, ImpactResponse
from app.models import (
    Campaign,
    Card,
    Contribution,
    ContributionState,
    EligibilityDecision,
)

MIN_CELL_SIZE = 5

# Province-level aggregation is unavailable until a consented, coarse
# province field exists. Flipping this to True requires a real column.
GEOGRAPHY_AVAILABLE = False


def count_band(count: int) -> str:
    """Exact bands from the plan. Anything below MIN_CELL_SIZE is never
    banded -- it is suppressed before reaching here."""
    if count >= 100:
        return "100+"
    if count >= 50:
        return "50-99"
    if count >= 20:
        return "20-49"
    return "5-19"


def _slug(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.strip().lower()).strip("_") or "unnamed"


def build_coverage(session: Session, now: datetime) -> ImpactResponse:
    """Deterministic aggregate over committed peer decisions.

    A contribution counts when its own peer-decision row says
    `corpus_eligible` **and** the contribution reached the terminal
    `CORPUS_ELIGIBLE` state -- i.e. the peer round actually committed,
    not merely a decision row written mid-flight.
    """
    rows = session.execute(
        select(
            Contribution.declared_language.label("language"),
            Campaign.name.label("campaign"),
            func.count(Contribution.id).label("verified_count"),
            func.max(EligibilityDecision.decided_at).label("updated_at"),
        )
        .join(EligibilityDecision, EligibilityDecision.contribution_id == Contribution.id)
        .join(Card, Card.id == Contribution.card_id)
        .join(Campaign, Campaign.id == Card.campaign_id)
        .where(
            EligibilityDecision.corpus_eligible.is_(True),
            Contribution.state == ContributionState.CORPUS_ELIGIBLE,
        )
        .group_by(Contribution.declared_language, Campaign.name)
        # Deterministic ordering at the database, not just in Python.
        .order_by(Contribution.declared_language.asc(), Campaign.name.asc())
    ).all()

    verified_total = sum(row.verified_count for row in rows)
    languages_active = len({row.language for row in rows})

    published = [row for row in rows if row.verified_count >= MIN_CELL_SIZE]
    suppressed_cell_count = len(rows) - len(published)

    nodes = [
        CoverageNodeResponse(
            # `NATIONAL` is the honest placeholder for the province slot
            # while no geographic column exists; a real province code
            # takes its place unchanged once one does.
            id=f"{row.language}:NATIONAL:{_slug(row.campaign)}",
            language=row.language,
            province_code=None,
            campaign=row.campaign,
            verified_count_band=count_band(row.verified_count),
            coverage_percent=(
                round(100 * row.verified_count / verified_total) if verified_total else 0
            ),
            # No signed, active model-evaluation record exists in this
            # database. Never inferred from contribution volume.
            model_gap_percent=None,
            updated_at=row.updated_at or now,
        )
        for row in published
    ]
    nodes.sort(key=lambda node: node.id)

    return ImpactResponse(
        verified_total=verified_total,
        languages_active=languages_active,
        # No `mission_proposals` table exists yet (Plan 03 Task 9 is not
        # built). Reported as 0 rather than approximated from anything else.
        missions_completed=0,
        geography_available=GEOGRAPHY_AVAILABLE,
        suppressed_cell_count=suppressed_cell_count,
        generated_at=now,
        nodes=nodes,
    )
