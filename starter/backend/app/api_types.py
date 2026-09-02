from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.models import ConsentScope


class ConsentGrantRequest(BaseModel):
    version: str = Field(min_length=1, max_length=64)
    scopes: list[ConsentScope] = Field(min_length=1)


class ConsentState(BaseModel):
    scope: ConsentScope
    version: str
    granted_at: datetime
    revoked_at: datetime | None


class ContributionCreateRequest(BaseModel):
    card_id: str


class AudioUploadResponse(BaseModel):
    audio_object_id: str
    object_key: str


class AudioFinaliseRequest(BaseModel):
    sha256: str = Field(min_length=64, max_length=64)
    mime_type: str
    codec: str
    duration_ms: int
    byte_length: int


class PlaybackResponse(BaseModel):
    url: str


class AssignmentAnswerRequest(BaseModel):
    answer_text: str = Field(min_length=1, max_length=500)
    violation_vote: bool = False


class AssignmentResponse(BaseModel):
    id: str
    contribution_id: str
    mode: str
    language: str
    prompt_text: str
    audio_playback_url: str | None = None


class MissionProposalDTO(BaseModel):
    """Persisted mission terms. The API never accepts these as input on the
    authorisation call -- they are copied from the stored proposal."""

    id: str
    language: str
    province_code: str
    domain: str
    rationale: str
    target_verified_clips: int
    fixed_reward_cents: int
    budget_cents: int
    state: str
    authorised_by: str | None = None


class OpsReadinessRow(BaseModel):
    label: str
    value: str | None = None
    detail: str
    available: bool


class OpsView(BaseModel):
    principal_kind: str
    roles: list[str]
    display_name: str
    confirmation_text: str
    readiness: list[OpsReadinessRow]
    gaps: list[dict]
    proposals: list[MissionProposalDTO]


class ContributionResult(BaseModel):
    status: str
    outcome: str | None = None
    reward_minor: int = 0
    currency: str = "ZAR"
    # A ledger credit is not proof that a real provider cash-out occurred.
    # Return the campaign's declared mode so the receipt can make that
    # distinction visible instead of presenting an internal credit as settled
    # MoMo money.
    provider_mode: str | None = None
    # These are intentionally separate. A resolver can credit the internal
    # ledger without creating a PaymentAttempt, so `CREDITED` must never be
    # rendered as provider settlement.
    ledger_state: str | None = None
    settlement_state: str | None = None
    currency_disclosure_text: str | None = None
    understood: bool | None = None
    corpus_eligible: bool | None = None
    reason: str | None = None


class CoverageNodeResponse(BaseModel):
    """One published, privacy-thresholded coverage cell.

    `province_code` is `None` until the schema carries a real, consented
    coarse province field -- see app/impact.py's module docstring. No
    personal, per-contribution, or audio field is ever present here.
    """

    id: str
    language: str
    province_code: str | None = None
    campaign: str
    verified_count_band: Literal["5-19", "20-49", "50-99", "100+"]
    coverage_percent: int = Field(ge=0, le=100)
    model_gap_percent: int | None = Field(default=None, ge=0, le=100)
    updated_at: datetime


class ImpactResponse(BaseModel):
    verified_total: int = Field(ge=0)
    languages_active: int = Field(ge=0)
    missions_completed: int = Field(ge=0)
    geography_available: bool = False
    suppressed_cell_count: int = Field(ge=0)
    generated_at: datetime
    nodes: list[CoverageNodeResponse]


# --- engagement layer (arcade) ---------------------------------------
# Every field below is derived from real rows by `app.arcade`. There is
# deliberately no skill-radar payload and no "players online" figure:
# AMAZWI measures neither, so neither is published.


class ProgressionResponse(BaseModel):
    xp: int = Field(ge=0)
    level: int = Field(ge=1)
    tier: str
    xp_into_level: int = Field(ge=0)
    xp_for_next_level: int = Field(ge=0)
    percent_into_level: int = Field(ge=0, le=100)
    verified_contributions: int = Field(ge=0)
    completed_verifications: int = Field(ge=0)


class SpeakerOutcomesResponse(BaseModel):
    understood: int = Field(ge=0)
    not_understood: int = Field(ge=0)
    awaiting_peers: int = Field(ge=0)
    closed: int = Field(ge=0)
    total: int = Field(ge=0)


class LeaderboardRowResponse(BaseModel):
    rank: int = Field(ge=1)
    user_id: str
    display_name: str
    verified_contributions: int = Field(ge=0)
    xp: int = Field(ge=0)
    tier: str
    is_current_user: bool


class PeerRowResponse(BaseModel):
    user_id: str
    display_name: str
    language: str
    tier: str
    verified_contributions: int = Field(ge=0)


class InvitationRowResponse(BaseModel):
    assignment_id: str
    contribution_id: str
    language: str
    speaker_name: str
    created_at: datetime


class DeckSummaryResponse(BaseModel):
    language: str
    card_count: int = Field(ge=0)
    contributors: int = Field(ge=0)
    verified_contributions: int = Field(ge=0)


class QuestRowResponse(BaseModel):
    key: str
    label: str
    detail: str
    progress: int = Field(ge=0)
    target: int = Field(ge=1)
    reward_xp: int = Field(ge=0)
    complete: bool


class ArcadeDashboardResponse(BaseModel):
    display_name: str
    earned_cents: int = Field(ge=0)
    progression: ProgressionResponse
    outcomes: SpeakerOutcomesResponse
    decks: list[DeckSummaryResponse]
    quests: list[QuestRowResponse]
    invitations: list[InvitationRowResponse]
    peers: list[PeerRowResponse]
    leaderboard: list[LeaderboardRowResponse]
    leaderboard_language: str | None
    generated_at: datetime


# --- reward catalogue -------------------------------------------------
# `availability` is computed server-side from the live provider mode, so
# a client cannot render a redeem button the backend would refuse. There
# is deliberately no points balance: the ledger is denominated in rand
# cents and a parallel currency would be a second source of truth.


class CatalogueRowResponse(BaseModel):
    key: str
    title: str
    description: str
    threshold_cents: int = Field(ge=0)
    momo_product: str
    availability: Literal[
        "REDEEMABLE", "INSUFFICIENT_CREDIT", "PROVIDER_NOT_CONNECTED"
    ]
    shortfall_cents: int = Field(ge=0)


class RewardsResponse(BaseModel):
    balance_cents: int = Field(ge=0)
    provider_mode: str
    provider_connected: bool
    thresholds_are_proposed: bool = True
    """Redemption thresholds are placeholders pending Sbu's money review."""
    items: list[CatalogueRowResponse]
    generated_at: datetime
