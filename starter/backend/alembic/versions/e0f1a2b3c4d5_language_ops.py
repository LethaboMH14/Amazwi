"""Language Ops: mission proposals and human-only MTN authorisation.

`alembic heads` was run before authoring this file and printed exactly
`d9e0f1a2b3c4 (head)`, so this revision extends the single Stage 6 head
rather than creating a second one.

CROSS-LANE, PENDING SBU'S REVIEW -- schema and money territory.

The `protect_mission_authorisation` trigger makes an authorisation record
append-only at the database level: once written, its operator, key,
confirmation text and timestamp cannot be edited or deleted. An
authorisation is evidence of a human act, so it must not be rewritable.

Revision ID: e0f1a2b3c4d5
Revises: d9e0f1a2b3c4
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "e0f1a2b3c4d5"
down_revision = "d9e0f1a2b3c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on = None

_PROVINCES = "'EC','FS','GP','KZN','LP','MP','NC','NW','WC'"
_DOMAINS = "'support','health','banking','transport','retail','education'"


def upgrade() -> None:
    bind = op.get_bind()

    # Persisted principal facts. Defaults are deliberate: existing rows are
    # real people who hold no operator role, so nothing is silently granted
    # authorisation power by this migration.
    op.add_column(
        "users",
        sa.Column(
            "principal_kind", sa.String(16), nullable=False, server_default="HUMAN"
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "roles",
            postgresql.ARRAY(sa.String()),
            nullable=False,
            server_default="{}",
        ),
    )
    op.add_column("users", sa.Column("display_name", sa.String(120), nullable=True))
    op.create_check_constraint(
        "ck_user_principal_kind", "users", "principal_kind IN ('HUMAN','AUTOMATED')"
    )

    state_enum = postgresql.ENUM(
        "PROPOSED", "AUTHORISED", "REJECTED", name="missionproposalstate"
    )
    state_enum.create(bind, checkfirst=True)

    op.create_table(
        "mission_proposals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "advisory_output_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("council_outputs.id"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "campaign_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("campaigns.id"),
            nullable=True,
        ),
        sa.Column("language", sa.String(2), nullable=False),
        sa.Column("province_code", sa.String(3), nullable=False),
        sa.Column("domain", sa.String(32), nullable=False),
        sa.Column("rationale", sa.String(1000), nullable=False),
        sa.Column("target_verified_clips", sa.Integer(), nullable=False),
        sa.Column("fixed_reward_cents", sa.Integer(), nullable=False),
        sa.Column("budget_cents", sa.Integer(), nullable=False),
        sa.Column(
            "state",
            postgresql.ENUM(
                "PROPOSED",
                "AUTHORISED",
                "REJECTED",
                name="missionproposalstate",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("target_verified_clips > 0", name="ck_mission_target_positive"),
        sa.CheckConstraint("fixed_reward_cents > 0", name="ck_mission_reward_positive"),
        sa.CheckConstraint(
            "budget_cents >= target_verified_clips * fixed_reward_cents",
            name="ck_mission_budget_covers_target",
        ),
        sa.CheckConstraint("language IN ('zu','tn')", name="ck_mission_language_vocab"),
        sa.CheckConstraint(
            f"province_code IN ({_PROVINCES})", name="ck_mission_province_vocab"
        ),
        sa.CheckConstraint(f"domain IN ({_DOMAINS})", name="ck_mission_domain_vocab"),
    )

    op.create_table(
        "mission_authorisations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "proposal_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("mission_proposals.id"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "operator_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("idempotency_key", sa.String(128), nullable=False, unique=True),
        sa.Column("confirmation_text", sa.String(500), nullable=False),
        sa.Column("authorised_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.execute(
        sa.text(
            """
            CREATE FUNCTION protect_mission_authorisation() RETURNS trigger
            LANGUAGE plpgsql AS $$
            BEGIN
              IF TG_OP = 'DELETE' THEN
                RAISE EXCEPTION 'mission authorisations cannot be deleted';
              END IF;
              RAISE EXCEPTION 'mission authorisations are immutable';
            END;
            $$;
            CREATE TRIGGER protect_mission_authorisation_trigger
            BEFORE UPDATE OR DELETE ON mission_authorisations
            FOR EACH ROW EXECUTE FUNCTION protect_mission_authorisation();
            """
        )
    )


def downgrade() -> None:
    bind = op.get_bind()
    op.execute(
        sa.text(
            "DROP TRIGGER IF EXISTS protect_mission_authorisation_trigger "
            "ON mission_authorisations"
        )
    )
    op.execute(sa.text("DROP FUNCTION IF EXISTS protect_mission_authorisation()"))
    op.drop_table("mission_authorisations")
    op.drop_table("mission_proposals")
    postgresql.ENUM(name="missionproposalstate").drop(bind, checkfirst=True)
    op.drop_constraint("ck_user_principal_kind", "users", type_="check")
    op.drop_column("users", "display_name")
    op.drop_column("users", "roles")
    op.drop_column("users", "principal_kind")
