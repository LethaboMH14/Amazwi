from __future__ import annotations

import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models import CouncilOutput, CouncilOutputState, OutboxEvent


def test_outbox_dedupe_key_is_unique(db_session):
    aggregate_id = uuid.uuid4()
    for _ in range(2):
        db_session.add(
            OutboxEvent(
                event_type="ContributionResolved",
                aggregate_type="Contribution",
                aggregate_id=aggregate_id,
                dedupe_key=f"contribution-resolved:{aggregate_id}",
                payload_json={"contribution_id": str(aggregate_id)},
            )
        )
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_council_output_is_unique_per_event_specialist_version(db_session):
    event = OutboxEvent(
        event_type="ContributionResolved",
        aggregate_type="Contribution",
        aggregate_id=uuid.uuid4(),
        dedupe_key="schema-test-event",
        payload_json={},
    )
    db_session.add(event)
    db_session.flush()
    for _ in range(2):
        db_session.add(
            CouncilOutput(
                event_id=event.id,
                specialist="DATA_STEWARD",
                model_version="rules-1",
                state=CouncilOutputState.SUCCEEDED,
                input_sha256="a" * 64,
                output_json={},
            )
        )
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_council_output_state_values_are_persisted(db_session):
    event = OutboxEvent(
        event_type="ContributionResolved",
        aggregate_type="Contribution",
        aggregate_id=uuid.uuid4(),
        dedupe_key="schema-state-event",
        payload_json={},
    )
    db_session.add(event)
    db_session.flush()
    output = CouncilOutput(
        event_id=event.id,
        specialist="DATA_STEWARD",
        model_version="rules-1",
        state=CouncilOutputState.RUNNING,
        input_sha256="b" * 64,
        output_json={},
    )
    db_session.add(output)
    db_session.commit()
    assert db_session.scalar(select(CouncilOutput.state).where(CouncilOutput.id == output.id)) == CouncilOutputState.RUNNING


def test_council_output_confidence_is_nullable_float(db_session):
    event = OutboxEvent(
        event_type="ContributionResolved",
        aggregate_type="Contribution",
        aggregate_id=uuid.uuid4(),
        dedupe_key="schema-confidence-event",
        payload_json={},
    )
    db_session.add(event)
    db_session.flush()
    output = CouncilOutput(
        event_id=event.id,
        specialist="DATA_STEWARD",
        model_version="rules-1",
        state=CouncilOutputState.SUCCEEDED,
        input_sha256="c" * 64,
        output_json={},
        confidence=0.75,
    )
    db_session.add(output)
    db_session.commit()
    assert db_session.get(CouncilOutput, output.id).confidence == 0.75
