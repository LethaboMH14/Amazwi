"""transactional Council outbox and advisory outputs"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "c8d9e0f1a2b3"
down_revision: Union[str, None] = "b7c8d9e0f1a2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    bind = op.get_bind()
    council_state = postgresql.ENUM("RUNNING", "SUCCEEDED", "FAILED", name="council_output_state")
    council_state.create(bind, checkfirst=True)
    op.create_table("outbox_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("event_type", sa.String(), nullable=False), sa.Column("aggregate_type", sa.String(), nullable=False),
        sa.Column("aggregate_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("dedupe_key", sa.String(), nullable=False),
        sa.Column("payload_json", postgresql.JSONB(), nullable=False), sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("available_at", sa.DateTime(timezone=True), nullable=False), sa.Column("claimed_at", sa.DateTime(timezone=True)),
        sa.Column("claimed_by", sa.String()), sa.Column("completed_at", sa.DateTime(timezone=True)), sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"), sa.Column("last_error", sa.Text()),
        sa.UniqueConstraint("dedupe_key", name="uq_outbox_dedupe_key"),
    )
    op.create_index("ix_outbox_events_event_type", "outbox_events", ["event_type"])
    op.create_index("ix_outbox_events_aggregate_id", "outbox_events", ["aggregate_id"])
    op.create_index("ix_outbox_events_available_at", "outbox_events", ["available_at"])
    op.execute(sa.text("CREATE INDEX ix_outbox_available_uncompleted ON outbox_events (available_at, occurred_at) WHERE completed_at IS NULL"))
    op.create_table("council_outputs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True), sa.Column("event_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("outbox_events.id"), nullable=False),
        sa.Column("specialist", sa.String(), nullable=False), sa.Column("model_version", sa.String(), nullable=False), sa.Column("state", council_state, nullable=False),
        sa.Column("input_sha256", sa.String(64), nullable=False), sa.Column("output_json", postgresql.JSONB()), sa.Column("confidence", sa.Float()), sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"), sa.Column("failure_reason", sa.Text()), sa.Column("started_at", sa.DateTime(timezone=True), nullable=False), sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("event_id", "specialist", "model_version", name="uq_council_event_specialist_version"),
    )

def downgrade() -> None:
    bind = op.get_bind(); op.drop_table("council_outputs"); op.drop_index("ix_outbox_available_uncompleted", table_name="outbox_events"); op.drop_index("ix_outbox_events_available_at", table_name="outbox_events"); op.drop_index("ix_outbox_events_aggregate_id", table_name="outbox_events"); op.drop_index("ix_outbox_events_event_type", table_name="outbox_events"); op.drop_table("outbox_events"); postgresql.ENUM(name="council_output_state").drop(bind, checkfirst=True)
