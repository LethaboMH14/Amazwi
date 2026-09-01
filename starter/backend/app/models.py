"""SQLAlchemy models: the core data model from `plan/02_TECH.md` §3-§4,§8.

Cross-lane note: written in Sbu's backend lane (S5) while both lanes are
fair game this session (BUILD_LOG.md, 31 Aug ~23:40). Flagged pending
Sbu's review -- schema, migrations and reward-ledger invariants are
squarely his territory ("data integrity" is his final call per
`05_BUILD.md` §2). This is an implementation of the already-written spec,
not a new design decision.

The records and constraints needed to enforce §8's ledger invariants, §4's
state machines, and the first governance/audio implementation slice are
modelled here. The MoMo provider adapter (§9), consent service, and storage
service remain deferred to their respective implementation tasks.
"""
from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    Index,
    String,
    Text,
    UniqueConstraint,
    Boolean,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def _uuid() -> uuid.UUID:
    return uuid.uuid4()


def _now() -> datetime:
    return datetime.now(timezone.utc)


# --- §4 state machines -------------------------------------------------


class ContributionState(str, enum.Enum):
    DRAFT = "DRAFT"
    RECORDED = "RECORDED"
    QUALITY_PASSED = "QUALITY_PASSED"
    OPEN = "OPEN"
    UNDERSTOOD = "UNDERSTOOD"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    VOIDED = "VOIDED"
    EXPIRED = "EXPIRED"
    CORPUS_ELIGIBLE = "CORPUS_ELIGIBLE"
    UNVALIDATED = "UNVALIDATED"


class RewardState(str, enum.Enum):
    NONE = "NONE"
    CREDITED = "CREDITED"
    RESERVED_FOR_CASH_OUT = "RESERVED_FOR_CASH_OUT"
    SETTLED = "SETTLED"
    RELEASED = "RELEASED"


class PaymentState(str, enum.Enum):
    CREATED = "CREATED"
    SUBMITTED = "SUBMITTED"
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"


class AssignmentMode(str, enum.Enum):
    LEARNER_MCQ = "LEARNER_MCQ"
    PROFICIENT_VERIFIER = "PROFICIENT_VERIFIER"


class ConsentScope(str, enum.Enum):
    RECORD_PROCESS_ROUND = "RECORD_PROCESS_ROUND"
    ASSIGNED_VERIFIER_PLAYBACK = "ASSIGNED_VERIFIER_PLAYBACK"
    RETAIN_MODEL_DEVELOPMENT = "RETAIN_MODEL_DEVELOPMENT"
    PUBLIC_AUDIO_ATTRIBUTION = "PUBLIC_AUDIO_ATTRIBUTION"


class AudioObjectState(str, enum.Enum):
    PENDING = "PENDING"
    AVAILABLE = "AVAILABLE"
    QUARANTINED = "QUARANTINED"
    DELETED = "DELETED"


# --- §3 core records -----------------------------------------------------


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    provider_subject: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    declared_languages: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)
    age_confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)


class ConsentGrant(Base):
    __tablename__ = "consent_grants"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    version: Mapped[str] = mapped_column(String, nullable=False)
    scope: Mapped[ConsentScope] = mapped_column(
        SAEnum(ConsentScope, name="consentscope"), nullable=False
    )
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index(
            "uq_consent_active_user_scope",
            "user_id",
            "scope",
            unique=True,
            postgresql_where=revoked_at.is_(None),
        ),
    )


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=False)
    budget_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    funded_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    committed_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    provider_reference: Mapped[str | None] = mapped_column(String, nullable=True)
    provider_mode: Mapped[str] = mapped_column(String, nullable=False, default="DEMO_PROVIDER")

    __table_args__ = (
        # §8 invariant 5: campaign commitments never exceed the funded budget.
        CheckConstraint("committed_cents <= funded_cents", name="ck_campaign_committed_le_funded"),
        CheckConstraint("committed_cents >= 0", name="ck_campaign_committed_nonneg"),
        CheckConstraint("funded_cents >= 0", name="ck_campaign_funded_nonneg"),
        CheckConstraint("budget_cents >= 0", name="ck_campaign_budget_nonneg"),
    )


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    language: Mapped[str] = mapped_column(String, nullable=False)
    target: Mapped[str] = mapped_column(String, nullable=False)
    blocked_words: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    accepted_answers: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    distractors: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    campaign_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("campaigns.id"), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __table_args__ = (
        # SCHEMA.md's own build-gate check: bare target alone is not
        # exhaustive -- accepted_answers needs >= 2 entries.
        CheckConstraint("array_length(accepted_answers, 1) >= 2", name="ck_card_accepted_answers_min2"),
        CheckConstraint("array_length(blocked_words, 1) = 4", name="ck_card_blocked_words_exactly4"),
        CheckConstraint("array_length(distractors, 1) = 3", name="ck_card_distractors_exactly3"),
    )


class Contribution(Base):
    __tablename__ = "contributions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    speaker_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    card_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cards.id"), nullable=False)
    declared_language: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[ContributionState] = mapped_column(
        SAEnum(ContributionState, name="contribution_state"),
        nullable=False,
        default=ContributionState.DRAFT,
    )
    audio_key: Mapped[str | None] = mapped_column(String, nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    quality_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reward_rule_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("campaign_reward_rules.id"), nullable=True
    )


class AudioObject(Base):
    __tablename__ = "audio_objects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    contribution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("contributions.id"), unique=True, nullable=False
    )
    object_key: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    sha256: Mapped[str | None] = mapped_column(String(64), index=True)
    mime_type: Mapped[str | None] = mapped_column(String)
    codec: Mapped[str | None] = mapped_column(String)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    byte_length: Mapped[int | None] = mapped_column(Integer)
    state: Mapped[AudioObjectState] = mapped_column(
        SAEnum(AudioObjectState, name="audioobjectstate"),
        nullable=False,
        default=AudioObjectState.PENDING,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
    finalised_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    quarantined_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class VerifierQualification(Base):
    __tablename__ = "verifier_qualifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=False)
    qualified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    reviewed_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint(
            "reviewed_by <> user_id",
            name="ck_verifier_qualification_independent_reviewer",
        ),
        Index(
            "uq_verifier_active_user_language",
            "user_id",
            "language",
            unique=True,
            postgresql_where=revoked_at.is_(None),
        ),
    )


class CampaignRewardRule(Base):
    __tablename__ = "campaign_reward_rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    campaign_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("campaigns.id"), nullable=False)
    version: Mapped[str] = mapped_column(String, nullable=False)
    contribution_reward_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint(
            "contribution_reward_cents > 0",
            name="ck_campaign_reward_positive",
        ),
        UniqueConstraint("campaign_id", "version", name="uq_campaign_reward_rule_version"),
        Index(
            "uq_campaign_active_reward_rule",
            "campaign_id",
            unique=True,
            postgresql_where=retired_at.is_(None),
        ),
    )


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    contribution_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("contributions.id"), nullable=False)
    verifier_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    mode: Mapped[AssignmentMode] = mapped_column(SAEnum(AssignmentMode, name="assignment_mode"), nullable=False)
    answer_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    answer_normalised: Mapped[str | None] = mapped_column(Text, nullable=True)
    matched: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    violation_vote: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    answered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        # §5 invariant: the same verifier cannot receive the same
        # contribution twice.
        UniqueConstraint("contribution_id", "verifier_id", name="uq_assignment_contribution_verifier"),
    )


class EligibilityDecision(Base):
    __tablename__ = "eligibility_decisions"

    # one decision per contribution -- PK is the FK itself, not a separate
    # surrogate id, so the "one decision per contribution" invariant is
    # structural rather than merely conventional.
    contribution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("contributions.id"), primary_key=True
    )
    understood: Mapped[bool] = mapped_column(Boolean, nullable=False)
    corpus_eligible: Mapped[bool] = mapped_column(Boolean, nullable=False)
    reason: Mapped[str] = mapped_column(String, nullable=False)
    consent_version: Mapped[str] = mapped_column(String, nullable=False)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)


class RewardEvent(Base):
    __tablename__ = "reward_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    contribution_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("contributions.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)

    __table_args__ = (
        # §8 invariant 1: unique reward on (contribution_id, user_id, type)
        # -- resolving the same contribution repeatedly creates one reward.
        UniqueConstraint("contribution_id", "user_id", "type", name="uq_reward_contribution_user_type"),
        UniqueConstraint("idempotency_key", name="uq_reward_idempotency_key"),
        CheckConstraint("amount_cents > 0", name="ck_reward_amount_positive"),
    )


class PaymentAttempt(Base):
    __tablename__ = "payment_attempts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    provider_mode: Mapped[str] = mapped_column(String, nullable=False)
    provider_reference: Mapped[str | None] = mapped_column(String, nullable=True)
    state: Mapped[PaymentState] = mapped_column(
        SAEnum(PaymentState, name="payment_state"), nullable=False, default=PaymentState.CREATED
    )
    idempotency_key: Mapped[str] = mapped_column(String, nullable=False)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        # §8 invariant 2: unique provider request reference / submitting the
        # same cash-out repeatedly creates one reservation.
        UniqueConstraint("idempotency_key", name="uq_payment_idempotency_key"),
        CheckConstraint("amount_cents > 0", name="ck_payment_amount_positive"),
    )


class Receipt(Base):
    __tablename__ = "receipts"

    contribution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("contributions.id"), primary_key=True
    )
    semantic_label: Mapped[str] = mapped_column(String, nullable=False)
    decision_evidence_json: Mapped[str] = mapped_column(Text, nullable=False)
    reward_rule_version: Mapped[str] = mapped_column(String, nullable=False)
    consent_version: Mapped[str] = mapped_column(String, nullable=False)
    payment_state: Mapped[str] = mapped_column(String, nullable=False)
    settlement_currency: Mapped[str] = mapped_column(String, nullable=False)
    currency_disclosure_text: Mapped[str] = mapped_column(String, nullable=False)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    actor_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String, nullable=False)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[str] = mapped_column(String, nullable=False)
    event_metadata: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
