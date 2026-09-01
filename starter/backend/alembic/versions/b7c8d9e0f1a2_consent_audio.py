"""governance consent and private audio records

Revision ID: b7c8d9e0f1a2
Revises: a3ea8e6c052e
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "b7c8d9e0f1a2"
down_revision: Union[str, None] = "a3ea8e6c052e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


CONSENT_SCOPES = (
    "RECORD_PROCESS_ROUND",
    "ASSIGNED_VERIFIER_PLAYBACK",
    "RETAIN_MODEL_DEVELOPMENT",
    "PUBLIC_AUDIO_ATTRIBUTION",
)


def upgrade() -> None:
    bind = op.get_bind()
    invalid = bind.execute(
        sa.text(
            "SELECT DISTINCT scope FROM consent_grants "
            "WHERE scope NOT IN (:record, :playback, :retain, :public)"
        ),
        {
            "record": CONSENT_SCOPES[0],
            "playback": CONSENT_SCOPES[1],
            "retain": CONSENT_SCOPES[2],
            "public": CONSENT_SCOPES[3],
        },
    ).scalars().all()
    if invalid:
        raise RuntimeError(
            "cannot migrate consent_grants.scope; invalid scopes: "
            + ", ".join(sorted(invalid))
        )

    consent_scope = postgresql.ENUM(*CONSENT_SCOPES, name="consentscope")
    consent_scope.create(bind, checkfirst=True)
    op.alter_column(
        "consent_grants",
        "scope",
        type_=consent_scope,
        postgresql_using="scope::text::consentscope",
    )
    op.create_index(
        "uq_consent_active_user_scope",
        "consent_grants",
        ["user_id", "scope"],
        unique=True,
        postgresql_where=sa.text("revoked_at IS NULL"),
    )

    audio_state = postgresql.ENUM(
        "PENDING",
        "AVAILABLE",
        "QUARANTINED",
        "DELETED",
        name="audioobjectstate",
        create_type=False,
    )
    audio_state.create(bind, checkfirst=True)
    op.create_table(
        "campaign_reward_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("campaign_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("contribution_reward_cents", sa.Integer(), nullable=False),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("retired_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "contribution_reward_cents > 0", name="ck_campaign_reward_positive"
        ),
        sa.ForeignKeyConstraint(["campaign_id"], ["campaigns.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("campaign_id", "version", name="uq_campaign_reward_rule_version"),
    )
    op.create_index(
        "uq_campaign_active_reward_rule",
        "campaign_reward_rules",
        ["campaign_id"],
        unique=True,
        postgresql_where=sa.text("retired_at IS NULL"),
    )
    op.execute(
        sa.text(
            """
            CREATE FUNCTION protect_campaign_reward_rule() RETURNS trigger
            LANGUAGE plpgsql AS $$
            BEGIN
                IF TG_OP = 'DELETE' THEN
                    RAISE EXCEPTION 'campaign reward rules cannot be deleted';
                END IF;
                IF OLD.campaign_id IS DISTINCT FROM NEW.campaign_id
                   OR OLD.version IS DISTINCT FROM NEW.version
                   OR OLD.contribution_reward_cents IS DISTINCT FROM NEW.contribution_reward_cents
                   OR OLD.effective_from IS DISTINCT FROM NEW.effective_from THEN
                    RAISE EXCEPTION 'campaign reward terms are immutable';
                END IF;
                IF OLD.retired_at IS NOT NULL
                   AND NEW.retired_at IS DISTINCT FROM OLD.retired_at THEN
                    RAISE EXCEPTION 'retired_at transition is immutable';
                END IF;
                RETURN NEW;
            END;
            $$;
            CREATE TRIGGER protect_campaign_reward_rule_trigger
            BEFORE UPDATE OR DELETE ON campaign_reward_rules
            FOR EACH ROW EXECUTE FUNCTION protect_campaign_reward_rule();
            """
        )
    )
    op.create_table(
        "verifier_qualifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("language", sa.String(), nullable=False),
        sa.Column("qualified_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reviewed_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "reviewed_by <> user_id", name="ck_verifier_qualification_independent_reviewer"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["reviewed_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "uq_verifier_active_user_language",
        "verifier_qualifications",
        ["user_id", "language"],
        unique=True,
        postgresql_where=sa.text("revoked_at IS NULL"),
    )
    op.create_table(
        "audio_objects",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("contribution_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("object_key", sa.String(), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=True),
        sa.Column("mime_type", sa.String(), nullable=True),
        sa.Column("codec", sa.String(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("byte_length", sa.Integer(), nullable=True),
        sa.Column("state", audio_state, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finalised_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("quarantined_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["contribution_id"], ["contributions.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("contribution_id"),
        sa.UniqueConstraint("object_key"),
    )
    op.create_index("ix_audio_objects_sha256", "audio_objects", ["sha256"], unique=False)
    op.add_column(
        "contributions",
        sa.Column(
            "reward_rule_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("campaign_reward_rules.id"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    bind = op.get_bind()
    op.drop_column("contributions", "reward_rule_id")
    op.drop_index("ix_audio_objects_sha256", table_name="audio_objects")
    op.drop_table("audio_objects")
    op.drop_index(
        "uq_verifier_active_user_language", table_name="verifier_qualifications"
    )
    op.drop_table("verifier_qualifications")
    op.drop_index("uq_campaign_active_reward_rule", table_name="campaign_reward_rules")
    op.execute(
        sa.text(
            "DROP TRIGGER IF EXISTS protect_campaign_reward_rule_trigger "
            "ON campaign_reward_rules"
        )
    )
    op.execute(sa.text("DROP FUNCTION IF EXISTS protect_campaign_reward_rule()"))
    op.drop_table("campaign_reward_rules")
    op.drop_index("uq_consent_active_user_scope", table_name="consent_grants")
    op.alter_column(
        "consent_grants",
        "scope",
        type_=sa.String(),
        postgresql_using="scope::text",
    )
    postgresql.ENUM(name="audioobjectstate").drop(bind, checkfirst=True)
    postgresql.ENUM(name="consentscope").drop(bind, checkfirst=True)
