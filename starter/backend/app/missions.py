"""Mission proposals and human-only MTN authorisation (Plan 03, Task 9).

CROSS-LANE, PENDING SBU'S REVIEW. `05_BUILD.md` §2 gives Sbu final say on
money. This module is written to spec and tested, but no authorisation it
records should be treated as production-authorised MTN spend until Sbu has
reviewed it.

The one rule this module exists to enforce
------------------------------------------
An advisory/automated actor may PROPOSE a mission. Only a real, named human
holding the `MTN_LANGUAGE_OPS` role may AUTHORISE one, and only by echoing
the exact confirmation sentence back. Three independent layers make an
automatic authorisation structurally impossible rather than merely
discouraged:

1. **Persisted principal kind.** `users.principal_kind` is a database
   column. A worker/service account is stored as `AUTOMATED` and can never
   satisfy the gate, no matter which roles it holds or which headers it
   sends. There is no request field that sets this.
2. **Explicit confirmation echo.** `authorise_mission` refuses unless the
   caller passes `confirmation_text` byte-equal to `CONFIRMATION_TEXT`, and
   persists what was confirmed. A scheduled job cannot "accidentally" agree
   to a sentence it must reproduce.
3. **No automated caller exists.** `authorise_mission` is imported by
   exactly one module, the HTTP route. `tests/test_missions.py` asserts
   this by scanning the source tree, so a future outbox worker or scheduler
   cannot quietly acquire an authorisation path without the test failing.

Where the plan's wording was ambiguous about where the human gate sits, the
more conservative reading was built: the gate is on the *authorisation*
call itself, in the service layer, not only in the UI. A UI-only gate would
leave the API auto-approvable.

Authorisation records human intent. It does NOT move money: no campaign
`funded_cents`/`committed_cents` is touched here, and no payment adapter is
called. Disbursement remains a separate, Sbu-owned decision.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import (
    AuditEvent,
    Campaign,
    CouncilOutput,
    MISSION_DOMAINS,
    MISSION_LANGUAGES,
    MISSION_PROVINCES,
    MTN_LANGUAGE_OPS_ROLE,
    MissionAuthorisation,
    MissionProposal,
    MissionProposalState,
    PrincipalKind,
    User,
)

#: The exact sentence a human operator must confirm. Shown verbatim in the
#: UI dialog and stored verbatim on the authorisation record.
CONFIRMATION_TEXT = (
    "You are authorising the persisted mission terms. "
    "AMAZWI will not change the fixed reward or budget from this screen."
)


class MissionRejected(ValueError):
    """Base class for every refusal in this module."""

    code = "MISSION_REJECTED"


class OperatorAuthorisationRequired(MissionRejected):
    """The actor is not a human MTN Language Ops operator, or did not
    confirm. This is the human gate refusing."""

    code = "OPERATOR_ROLE_REQUIRED"


class MissionAlreadyDecided(MissionRejected):
    code = "MISSION_ALREADY_DECIDED"


class IdempotencyConflict(MissionRejected):
    code = "IDEMPOTENCY_CONFLICT"


@dataclass(frozen=True)
class OperatorPrincipal:
    """A principal derived *only* from a persisted `users` row.

    Built exclusively by `principal_for_user`. There is deliberately no
    constructor path that reads `kind` or `roles` from a request.
    """

    user_id: UUID
    kind: str
    roles: tuple[str, ...]
    display_name: str

    @property
    def is_human_mtn_operator(self) -> bool:
        return (
            self.kind == PrincipalKind.HUMAN.value
            and MTN_LANGUAGE_OPS_ROLE in self.roles
        )


def principal_for_user(user: User) -> OperatorPrincipal:
    return OperatorPrincipal(
        user_id=user.id,
        kind=user.principal_kind,
        roles=tuple(user.roles or ()),
        display_name=user.display_name or user.provider_subject,
    )


def _now() -> datetime:
    return datetime.now(timezone.utc)


def propose_mission(
    session: Session,
    *,
    advisory_output_id: UUID,
    language: str,
    province_code: str,
    domain: str,
    rationale: str,
    target_verified_clips: int,
    fixed_reward_cents: int,
    budget_cents: int,
    campaign_id: UUID | None = None,
) -> MissionProposal:
    """Record an advisory proposal. Commits nothing and pays nothing."""
    if session.get(CouncilOutput, advisory_output_id) is None:
        raise MissionRejected("advisory output does not exist")
    if language not in MISSION_LANGUAGES:
        raise MissionRejected(f"language must be one of {MISSION_LANGUAGES}")
    if province_code not in MISSION_PROVINCES:
        raise MissionRejected(f"province must be one of {MISSION_PROVINCES}")
    if domain not in MISSION_DOMAINS:
        raise MissionRejected(f"domain must be one of {MISSION_DOMAINS}")
    if not rationale or len(rationale) > 1000:
        raise MissionRejected("rationale is required and must be <= 1000 chars")
    if target_verified_clips <= 0:
        raise MissionRejected("target_verified_clips must be positive")
    if fixed_reward_cents <= 0:
        raise MissionRejected("fixed_reward_cents must be positive")
    if budget_cents < target_verified_clips * fixed_reward_cents:
        raise MissionRejected("budget_cents must cover target x fixed reward")
    if campaign_id is not None and session.get(Campaign, campaign_id) is None:
        raise MissionRejected("campaign does not exist")
    if session.scalar(
        select(MissionProposal).where(
            MissionProposal.advisory_output_id == advisory_output_id
        )
    ):
        raise MissionRejected("advisory output already has a proposal")

    proposal = MissionProposal(
        advisory_output_id=advisory_output_id,
        campaign_id=campaign_id,
        language=language,
        province_code=province_code,
        domain=domain,
        rationale=rationale,
        target_verified_clips=target_verified_clips,
        fixed_reward_cents=fixed_reward_cents,
        budget_cents=budget_cents,
        state=MissionProposalState.PROPOSED,
    )
    session.add(proposal)
    session.flush()
    return proposal


def authorise_mission(
    session: Session,
    proposal_id: UUID,
    operator: OperatorPrincipal,
    idempotency_key: str,
    now: datetime | None = None,
    *,
    confirmation_text: str,
) -> MissionProposal:
    """THE HUMAN GATE. Refuses anything that is not a confirmed human act.

    `confirmation_text` is keyword-only and has no default precisely so no
    caller can authorise a mission without naming it.
    """
    # --- Gate layer 1+2: persisted human principal, with role, who echoed
    # the confirmation sentence. Checked before anything is read or written.
    if not operator.is_human_mtn_operator:
        raise OperatorAuthorisationRequired(
            "mission authorisation requires a human MTN_LANGUAGE_OPS operator"
        )
    if confirmation_text != CONFIRMATION_TEXT:
        raise OperatorAuthorisationRequired(
            "mission authorisation requires the operator's explicit confirmation"
        )
    if not idempotency_key:
        raise MissionRejected("idempotency key is required")

    proposal = session.get(MissionProposal, proposal_id)
    if proposal is None:
        raise MissionRejected("mission proposal does not exist")

    existing_for_key = session.scalar(
        select(MissionAuthorisation).where(
            MissionAuthorisation.idempotency_key == idempotency_key
        )
    )
    if existing_for_key is not None:
        if existing_for_key.proposal_id != proposal.id:
            raise IdempotencyConflict("idempotency key belongs to another mission")
        # Same key, same mission: a replay. Terms are returned unchanged.
        return proposal

    if proposal.state is not MissionProposalState.PROPOSED:
        raise MissionAlreadyDecided(
            f"mission is already {proposal.state.value}"
        )

    now = now or _now()
    session.add(
        MissionAuthorisation(
            proposal_id=proposal.id,
            operator_id=operator.user_id,
            idempotency_key=idempotency_key,
            confirmation_text=confirmation_text,
            authorised_at=now,
        )
    )
    proposal.state = MissionProposalState.AUTHORISED
    session.add(
        AuditEvent(
            actor_id=operator.user_id,
            action="MISSION_AUTHORISED",
            entity_type="mission_proposal",
            entity_id=str(proposal.id),
            event_metadata=json.dumps(
                {
                    "language": proposal.language,
                    "province_code": proposal.province_code,
                    "domain": proposal.domain,
                    "target_verified_clips": proposal.target_verified_clips,
                    "fixed_reward_cents": proposal.fixed_reward_cents,
                    "budget_cents": proposal.budget_cents,
                    "confirmation_text": confirmation_text,
                    "funds_moved": False,
                },
                sort_keys=True,
            ),
        )
    )
    session.flush()
    return proposal
