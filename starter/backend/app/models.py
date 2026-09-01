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
    Float,
    ForeignKey,
    Integer,
    Index,
    String,
    Text,
    UniqueConstraint,
    Boolean,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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


class CouncilOutputState(str, enum.Enum):
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class OutboxEvent(Base):
    __tablename__ = "outbox_events"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    event_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    aggregate_type: Mapped[str] = mapped_column(String, nullable=False)
    aggregate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    dedupe_key: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    payload_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
    available_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False, index=True)
    claimed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    claimed_by: Mapped[str | None] = mapped_column(String, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    attempt_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    __table_args__ = (Index("ix_outbox_available_uncompleted", "available_at", "occurred_at", postgresql_where=completed_at.is_(None)),)


class CouncilOutput(Base):
    __tablename__ = "council_outputs"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("outbox_events.id"), nullable=False)
    specialist: Mapped[str] = mapped_column(String, nullable=False)
    model_version: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[CouncilOutputState] = mapped_column(SAEnum(CouncilOutputState, name="council_output_state"), nullable=False)
    input_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    output_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    __table_args__ = (UniqueConstraint("event_id", "specialist", "model_version", name="uq_council_event_specialist_version"),)

class DatasetSourceClass(str, enum.Enum):
    EXTERNAL_LICENSED = "EXTERNAL_LICENSED"
    AMAZWI_OPTED_IN = "AMAZWI_OPTED_IN"
    EVALUATION_ONLY = "EVALUATION_ONLY"
    SYNTHETIC_FIXTURE = "SYNTHETIC_FIXTURE"
class DatasetSourceState(str, enum.Enum):
    REGISTERED = "REGISTERED"
    PREFLIGHT_PASSED = "PREFLIGHT_PASSED"
    BLOCKED = "BLOCKED"
    REVOKED = "REVOKED"
class DatasetExportState(str, enum.Enum):
    DRAFT = "DRAFT"
    APPROVED = "APPROVED"
    REVOKED = "REVOKED"

class DatasetSource(Base):
    __tablename__ = "dataset_sources"
    source_id: Mapped[str] = mapped_column(String, primary_key=True)
    version: Mapped[str] = mapped_column(String, nullable=False)
    repository_url: Mapped[str] = mapped_column(String, nullable=False)
    exact_revision: Mapped[str] = mapped_column(String, nullable=False)
    license_spdx: Mapped[str] = mapped_column(String, nullable=False)
    restrictions_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    allowed_tasks: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    languages: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    state: Mapped[DatasetSourceState] = mapped_column(SAEnum(DatasetSourceState, name="dataset_source_state"), nullable=False)
    registry_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    reviewed_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

class DatasetExport(Base):
    __tablename__ = "dataset_exports"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    state: Mapped[DatasetExportState] = mapped_column(SAEnum(DatasetExportState, name="dataset_export_state"), nullable=False)
    purpose: Mapped[str] = mapped_column(String, nullable=False)
    requested_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    approved_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    manifest_id: Mapped[str | None] = mapped_column(String, nullable=True)
    manifest_sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)

class DatasetExportRow(Base):
    __tablename__ = "dataset_export_rows"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    export_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dataset_exports.id"), nullable=False)
    source_class: Mapped[DatasetSourceClass] = mapped_column(SAEnum(DatasetSourceClass, name="dataset_source_class"), nullable=False)
    source_record_id: Mapped[str] = mapped_column(String, nullable=False)
    contribution_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("contributions.id"), nullable=True)
    object_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    consent_version: Mapped[str | None] = mapped_column(String, nullable=True)
    included: Mapped[bool] = mapped_column(Boolean, nullable=False)
    exclusion_reason: Mapped[str | None] = mapped_column(String, nullable=True)
    __table_args__ = (CheckConstraint("(source_class = 'AMAZWI_OPTED_IN' AND contribution_id IS NOT NULL) OR (source_class <> 'AMAZWI_OPTED_IN' AND contribution_id IS NULL)", name="ck_dataset_row_source_link"), UniqueConstraint("export_id", "source_class", "source_record_id", name="uq_dataset_export_source_record"))
