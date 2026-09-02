"""Engagement-layer read API.

Authenticated on purpose. Unlike `/impact`, which publishes suppressed
aggregates, this endpoint returns display names and per-person counts, so
it requires the same identity check every other user resource uses.

CROSS-LANE, PENDING SBU'S REVIEW. Publishing contributor names on a
leaderboard -- even to signed-in peers -- is a privacy posture decision,
not a mechanical one. It is scoped as narrowly as the feature allows
(caller's own language cohort, display names only, never a provider
subject), and the ranking is derived from `contributions`, never from any
payment or ledger detail. Sbu has final say per 05_BUILD.md section 2.
"""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from app.api_types import (
    ArcadeDashboardResponse,
    CatalogueRowResponse,
    RedemptionResponse,
    RewardsResponse,
    DeckSummaryResponse,
    InvitationRowResponse,
    LeaderboardRowResponse,
    PeerRowResponse,
    ProgressionResponse,
    QuestRowResponse,
    SpeakerOutcomesResponse,
)
from app.arcade import (
    build_decks,
    build_invitations,
    build_leaderboard,
    build_peer_list,
    build_quests,
    earned_cents,
    progression_for_user,
    speaker_outcomes,
)
from app.rewards import RedemptionRefused, build_catalogue, is_live_provider, redeem
from app.db import get_session
from app.identity import AuthenticatedIdentity, get_current_identity, require_identity_user

router = APIRouter(tags=["arcade"])


def _dashboard(
    session: Session,
    identity: AuthenticatedIdentity,
    language: str | None,
    now: datetime,
) -> ArcadeDashboardResponse:
    user = require_identity_user(session, identity)

    progression = progression_for_user(session, user.id)
    outcomes = speaker_outcomes(session, user.id)
    decks = build_decks(session)
    quests = build_quests(session, current_user_id=user.id, now=now)
    invitations = build_invitations(session, current_user_id=user.id)
    peers = build_peer_list(session, current_user_id=user.id)

    # Rank within a language the caller actually participates in. Falling
    # back to the first available deck keeps the panel populated for a
    # brand-new user without inventing a cohort they are not in.
    board_language = language
    if board_language is None:
        if user.declared_languages:
            board_language = sorted(user.declared_languages)[0]
        elif decks:
            board_language = decks[0].language
    leaderboard = (
        build_leaderboard(
            session, language=board_language, current_user_id=user.id
        )
        if board_language
        else []
    )

    return ArcadeDashboardResponse(
        display_name=user.display_name or "Anonymous contributor",
        earned_cents=earned_cents(session, user.id),
        progression=ProgressionResponse(
            xp=progression.xp,
            level=progression.level,
            tier=progression.tier,
            xp_into_level=progression.xp_into_level,
            xp_for_next_level=progression.xp_for_next_level,
            percent_into_level=progression.percent_into_level,
            verified_contributions=progression.verified_contributions,
            completed_verifications=progression.completed_verifications,
        ),
        outcomes=SpeakerOutcomesResponse(
            understood=outcomes.understood,
            not_understood=outcomes.not_understood,
            awaiting_peers=outcomes.awaiting_peers,
            closed=outcomes.closed,
            total=outcomes.total,
        ),
        decks=[
            DeckSummaryResponse(
                language=deck.language,
                card_count=deck.card_count,
                contributors=deck.contributors,
                verified_contributions=deck.verified_contributions,
            )
            for deck in decks
        ],
        quests=[
            QuestRowResponse(
                key=quest.key,
                label=quest.label,
                detail=quest.detail,
                progress=quest.progress,
                target=quest.target,
                reward_xp=quest.reward_xp,
                complete=quest.complete,
            )
            for quest in quests
        ],
        invitations=[
            InvitationRowResponse(
                assignment_id=str(row.assignment_id),
                contribution_id=str(row.contribution_id),
                language=row.language,
                speaker_name=row.speaker_name,
                created_at=row.created_at,
            )
            for row in invitations
        ],
        peers=[
            PeerRowResponse(
                user_id=str(row.user_id),
                display_name=row.display_name,
                language=row.language,
                tier=row.tier,
                verified_contributions=row.verified_contributions,
            )
            for row in peers
        ],
        leaderboard=[
            LeaderboardRowResponse(
                rank=row.rank,
                user_id=str(row.user_id),
                display_name=row.display_name,
                verified_contributions=row.verified_contributions,
                xp=row.xp,
                tier=row.tier,
                is_current_user=row.is_current_user,
            )
            for row in leaderboard
        ],
        leaderboard_language=board_language,
        generated_at=now,
    )


@router.get("/arcade", response_model=ArcadeDashboardResponse)
@router.get("/api/arcade", response_model=ArcadeDashboardResponse, include_in_schema=False)
def arcade_dashboard(
    language: str | None = Query(default=None, max_length=8),
    session: Session = Depends(get_session),
    identity: AuthenticatedIdentity = Depends(get_current_identity),
) -> ArcadeDashboardResponse:
    return _dashboard(session, identity, language, datetime.now(timezone.utc))


@router.get("/rewards", response_model=RewardsResponse)
@router.get("/api/rewards", response_model=RewardsResponse, include_in_schema=False)
def rewards(
    session: Session = Depends(get_session),
    identity: AuthenticatedIdentity = Depends(get_current_identity),
) -> RewardsResponse:
    """What this contributor's ledger credit can become.

    The provider mode is read from the running app's provider adapter,
    not from a request field, so a client cannot ask to be told it is
    live. With the DemoProvider every row comes back
    PROVIDER_NOT_CONNECTED and the UI renders no redeem action.
    """
    from app.main import provider  # local import: avoids a circular import

    user = require_identity_user(session, identity)
    view = build_catalogue(session, user_id=user.id, provider_mode=provider.mode)
    return RewardsResponse(
        balance_cents=view.balance_cents,
        provider_mode=view.provider_mode,
        provider_connected=view.provider_connected,
        items=[
            CatalogueRowResponse(
                key=row.item.key,
                title=row.item.title,
                description=row.item.description,
                threshold_cents=row.item.threshold_cents,
                momo_product=row.item.momo_product,
                availability=row.availability.value,
                shortfall_cents=row.shortfall_cents,
            )
            for row in view.rows
        ],
        generated_at=datetime.now(timezone.utc),
    )


@router.post("/rewards/{key}/redeem", response_model=RedemptionResponse)
@router.post(
    "/api/rewards/{key}/redeem",
    response_model=RedemptionResponse,
    include_in_schema=False,
)
def redeem_reward(
    key: str,
    idempotency_key: str = Header(alias="Idempotency-Key"),
    session: Session = Depends(get_session),
    identity: AuthenticatedIdentity = Depends(get_current_identity),
) -> RedemptionResponse:
    """Spend ledger credit through the payment provider.

    This is the leg the golden path was missing: peers agree -> resolver
    credits `reward_events` -> (previously nothing) -> now a real
    `PaymentAttempt` and a real provider adapter call.

    `Idempotency-Key` is required, not optional: a double-tapped Redeem
    must reserve once, and the ledger enforces that on the key.
    """
    from app.main import provider

    user = require_identity_user(session, identity)
    try:
        attempt = redeem(
            session,
            user_id=user.id,
            key=key,
            provider_mode=provider.mode,
            provider=provider,
            idempotency_key=idempotency_key,
        )
    except RedemptionRefused as exc:
        # 409, not 400: the request is well-formed, the state refuses it.
        raise HTTPException(status_code=409, detail={"code": exc.code, "detail": str(exc)})

    return RedemptionResponse(
        attempt_id=str(attempt.id),
        reward_key=key,
        amount_cents=attempt.amount_cents,
        provider_mode=attempt.provider_mode,
        provider_reference=attempt.provider_reference,
        state=attempt.state.value if hasattr(attempt.state, "value") else str(attempt.state),
        is_real_settlement=is_live_provider(attempt.provider_mode),
    )
