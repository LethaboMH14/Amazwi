"""Dataset provenance persistence and the export firewall.

Closes Final Acceptance Checklist items 5, 6 and 7 of
docs/superpowers/plans/2026-09-01-amazwi-02-council-data-models.md:

  5. provenance fields are persisted,
  6. only peer-decided, quality-acceptable, separately opted-in, unrevoked
     AMAZWI rows can enter an approved export,
  7. external licensed / opted-in / evaluation-only / synthetic fixture rows
     stay explicitly distinguished.

test_council_data_e2e.py covered the happy path and one missing-consent
case. The refusals that make the firewall a firewall -- non-final
contributions, unavailable or quarantined audio, consent revoked after
drafting, excluded rows in an approved export, an approved manifest being
re-approved -- had no test.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.datasets import ExportRejected, approve_export, create_export, revoke_export
from app.models import (
    AudioObject,
    AudioObjectState,
    Campaign,
    Card,
    ConsentGrant,
    ConsentScope,
    Contribution,
    ContributionState,
    DatasetExport,
    DatasetExportRow,
    DatasetExportState,
    DatasetSource,
    DatasetSourceClass,
    DatasetSourceState,
    User,
)

NOW = datetime(2026, 9, 2, 12, 0, 0, tzinfo=timezone.utc)


def _user(db_session, subject: str) -> User:
    user = User(id=uuid.uuid4(), provider_subject=subject, declared_languages=["tn"],
                age_confirmed_at=NOW, created_at=NOW)
    db_session.add(user)
    db_session.flush()
    return user


def _eligible_contribution(db_session, speaker, *, state=ContributionState.CORPUS_ELIGIBLE,
                           audio_state=AudioObjectState.AVAILABLE, model_consent=True,
                           suffix="") -> Contribution:
    campaign = Campaign(id=uuid.uuid4(), name=f"DS{suffix}", language="tn", budget_cents=1000,
                        funded_cents=1000, committed_cents=0, provider_mode="DEMO_PROVIDER")
    db_session.add(campaign)
    db_session.flush()
    card = Card(id=uuid.uuid4(), language="tn", target="kgomo", blocked_words=["a", "b", "c", "d"],
                accepted_answers=["kgomo", "kgomo"], distractors=["x", "y", "z"],
                campaign_id=campaign.id, active=True)
    db_session.add(card)
    db_session.flush()
    contribution = Contribution(id=uuid.uuid4(), speaker_id=speaker.id, card_id=card.id,
                                declared_language="tn", state=state)
    db_session.add(contribution)
    db_session.flush()
    db_session.add(AudioObject(id=uuid.uuid4(), contribution_id=contribution.id,
                               object_key=f"ds/{contribution.id}", sha256="a" * 64,
                               state=audio_state, byte_length=4, duration_ms=1000))
    if model_consent:
        db_session.add(ConsentGrant(user_id=speaker.id, version="model-v3",
                                    scope=ConsentScope.RETAIN_MODEL_DEVELOPMENT, granted_at=NOW))
    db_session.commit()
    return contribution


def _row(contribution=None, *, source_class="AMAZWI_OPTED_IN", record="rec-1", **extra):
    row = {"source_class": source_class, "source_record_id": record, "object_sha256": "a" * 64}
    if contribution is not None:
        row["contribution_id"] = contribution.id
    row.update(extra)
    return row


# --- Item 5: provenance is persisted ----------------------------------------


def test_dataset_source_persists_licence_restrictions_and_allowed_tasks(db_session):
    reviewer = _user(db_session, "ds-reviewer")
    db_session.commit()
    source = DatasetSource(
        source_id="swivuriso", version="1.0",
        repository_url="https://example.invalid/swivuriso",
        exact_revision="deadbeef" * 5,
        license_spdx="CC-BY-4.0",
        restrictions_json={"synthesis": "prohibited", "redistribution": "prohibited"},
        allowed_tasks=["ASR_TRAINING"], languages=["ts"],
        state=DatasetSourceState.REGISTERED, registry_sha256="c" * 64,
        reviewed_by=reviewer.id, reviewed_at=NOW,
    )
    db_session.add(source)
    db_session.commit()

    stored = db_session.get(DatasetSource, "swivuriso")
    assert stored.license_spdx == "CC-BY-4.0"
    assert stored.restrictions_json["synthesis"] == "prohibited"
    assert stored.allowed_tasks == ["ASR_TRAINING"]
    assert stored.exact_revision == "deadbeef" * 5
    assert stored.registry_sha256 == "c" * 64
    assert stored.reviewed_by == reviewer.id and stored.reviewed_at is not None
    assert stored.state is DatasetSourceState.REGISTERED


def test_export_row_persists_consent_version_hash_and_exclusion_evidence(db_session):
    speaker = _user(db_session, "ds-provenance")
    contribution = _eligible_contribution(db_session, speaker)

    export = create_export(db_session, purpose="ASR training", requested_by=speaker.id, rows=[
        _row(contribution, record="rec-included"),
        _row(source_class="SYNTHETIC_FIXTURE", record="rec-excluded",
             included=False, exclusion_reason="fixture only"),
    ])
    db_session.commit()

    rows = {r.source_record_id: r for r in
            db_session.query(DatasetExportRow).filter_by(export_id=export.id)}
    included = rows["rec-included"]
    assert included.consent_version == "model-v3", "the consent version in force is snapshotted, not recomputed later"
    assert included.object_sha256 == "a" * 64
    assert included.contribution_id == contribution.id
    assert included.included is True and included.exclusion_reason is None

    excluded = rows["rec-excluded"]
    assert excluded.included is False
    assert excluded.exclusion_reason == "fixture only"
    assert excluded.contribution_id is None


def test_approval_and_revocation_evidence_records_actor_and_time(db_session):
    speaker = _user(db_session, "ds-evidence")
    approver = _user(db_session, "ds-approver")
    db_session.commit()
    contribution = _eligible_contribution(db_session, speaker)

    export = create_export(db_session, purpose="ASR training", requested_by=speaker.id,
                           rows=[_row(contribution)])
    db_session.commit()
    approve_export(db_session, export_id=export.id, actor_id=approver.id,
                   manifest_id="m-1", manifest_sha256="b" * 64)
    db_session.commit()

    stored = db_session.get(DatasetExport, export.id)
    assert stored.approved_by == approver.id and stored.approved_at is not None
    assert stored.manifest_id == "m-1" and stored.manifest_sha256 == "b" * 64

    revoke_export(db_session, export_id=export.id, actor_id=approver.id)
    db_session.commit()
    db_session.refresh(stored)
    assert stored.state is DatasetExportState.REVOKED
    assert stored.revoked_by == approver.id and stored.revoked_at is not None
    assert stored.manifest_sha256 == "b" * 64, "revocation keeps the evidence of what was approved"


# --- Item 6: only eligible rows may enter an approved export -----------------


@pytest.mark.parametrize("state", [
    ContributionState.OPEN,
    ContributionState.UNVALIDATED,
    ContributionState.VOIDED,
    ContributionState.REVIEW_REQUIRED,
    ContributionState.EXPIRED,
    ContributionState.DRAFT,
])
def test_non_final_contributions_cannot_be_exported(db_session, state):
    speaker = _user(db_session, f"ds-state-{state.value}")
    contribution = _eligible_contribution(db_session, speaker, state=state, suffix=state.value)

    with pytest.raises(ExportRejected, match="corpus-eligible"):
        create_export(db_session, purpose="ASR training", requested_by=speaker.id,
                      rows=[_row(contribution)])


@pytest.mark.parametrize("audio_state", [
    AudioObjectState.PENDING,
    AudioObjectState.QUARANTINED,
    AudioObjectState.DELETED,
])
def test_unavailable_or_quarantined_audio_cannot_be_exported(db_session, audio_state):
    speaker = _user(db_session, f"ds-audio-{audio_state.value}")
    contribution = _eligible_contribution(db_session, speaker, audio_state=audio_state,
                                          suffix=audio_state.value)

    with pytest.raises(ExportRejected, match="audio must be available"):
        create_export(db_session, purpose="ASR training", requested_by=speaker.id,
                      rows=[_row(contribution)])


def test_consent_revoked_before_drafting_blocks_the_row(db_session):
    speaker = _user(db_session, "ds-revoked")
    contribution = _eligible_contribution(db_session, speaker)
    grant = db_session.query(ConsentGrant).filter_by(
        user_id=speaker.id, scope=ConsentScope.RETAIN_MODEL_DEVELOPMENT).one()
    grant.revoked_at = NOW + timedelta(days=1)
    db_session.commit()

    with pytest.raises(ExportRejected, match="consent"):
        create_export(db_session, purpose="ASR training", requested_by=speaker.id,
                      rows=[_row(contribution)])


def test_round_consent_alone_is_not_model_development_consent(db_session):
    """Recording for a round is a separate decision from training on it."""
    speaker = _user(db_session, "ds-round-only")
    contribution = _eligible_contribution(db_session, speaker, model_consent=False)
    db_session.add(ConsentGrant(user_id=speaker.id, version="round-v1",
                                scope=ConsentScope.RECORD_PROCESS_ROUND, granted_at=NOW))
    db_session.commit()

    with pytest.raises(ExportRejected, match="consent"):
        create_export(db_session, purpose="ASR training", requested_by=speaker.id,
                      rows=[_row(contribution)])


def test_an_export_with_any_excluded_row_cannot_be_approved(db_session):
    speaker = _user(db_session, "ds-excluded")
    contribution = _eligible_contribution(db_session, speaker)
    export = create_export(db_session, purpose="ASR training", requested_by=speaker.id, rows=[
        _row(contribution, record="keep"),
        _row(source_class="SYNTHETIC_FIXTURE", record="drop", included=False,
             exclusion_reason="not licensed for training"),
    ])
    db_session.commit()

    with pytest.raises(ExportRejected, match="included rows"):
        approve_export(db_session, export_id=export.id, actor_id=speaker.id,
                       manifest_id="m-2", manifest_sha256="b" * 64)


def test_an_empty_export_cannot_be_approved(db_session):
    speaker = _user(db_session, "ds-empty")
    db_session.commit()
    export = create_export(db_session, purpose="ASR training", requested_by=speaker.id, rows=[])
    db_session.commit()

    with pytest.raises(ExportRejected, match="included rows"):
        approve_export(db_session, export_id=export.id, actor_id=speaker.id,
                       manifest_id="m-3", manifest_sha256="b" * 64)


def test_a_purpose_is_required(db_session):
    speaker = _user(db_session, "ds-purpose")
    db_session.commit()
    with pytest.raises(ExportRejected, match="purpose"):
        create_export(db_session, purpose="", requested_by=speaker.id, rows=[])


def test_an_approved_manifest_hash_is_immutable(db_session):
    """Re-approving is the only way to change manifest_sha256 through this
    service, and it is refused -- an approved manifest is a fixed claim."""
    speaker = _user(db_session, "ds-immutable")
    contribution = _eligible_contribution(db_session, speaker)
    export = create_export(db_session, purpose="ASR training", requested_by=speaker.id,
                           rows=[_row(contribution)])
    db_session.commit()
    approve_export(db_session, export_id=export.id, actor_id=speaker.id,
                   manifest_id="m-4", manifest_sha256="b" * 64)
    db_session.commit()

    with pytest.raises(ExportRejected, match="not a draft"):
        approve_export(db_session, export_id=export.id, actor_id=speaker.id,
                       manifest_id="m-4-tampered", manifest_sha256="d" * 64)

    db_session.rollback()
    assert db_session.get(DatasetExport, export.id).manifest_sha256 == "b" * 64


def test_a_malformed_manifest_hash_is_refused(db_session):
    speaker = _user(db_session, "ds-badhash")
    contribution = _eligible_contribution(db_session, speaker)
    export = create_export(db_session, purpose="ASR training", requested_by=speaker.id,
                           rows=[_row(contribution)])
    db_session.commit()

    with pytest.raises(ExportRejected, match="manifest sha256"):
        approve_export(db_session, export_id=export.id, actor_id=speaker.id,
                       manifest_id="m-5", manifest_sha256="tooshort")


def test_only_an_approved_export_can_be_revoked(db_session):
    speaker = _user(db_session, "ds-revoke-draft")
    contribution = _eligible_contribution(db_session, speaker)
    export = create_export(db_session, purpose="ASR training", requested_by=speaker.id,
                           rows=[_row(contribution)])
    db_session.commit()

    with pytest.raises(ExportRejected, match="only approved exports"):
        revoke_export(db_session, export_id=export.id, actor_id=speaker.id)


def test_a_revoked_export_cannot_be_revoked_or_approved_again(db_session):
    speaker = _user(db_session, "ds-revoke-twice")
    contribution = _eligible_contribution(db_session, speaker)
    export = create_export(db_session, purpose="ASR training", requested_by=speaker.id,
                           rows=[_row(contribution)])
    db_session.commit()
    approve_export(db_session, export_id=export.id, actor_id=speaker.id,
                   manifest_id="m-6", manifest_sha256="b" * 64)
    revoke_export(db_session, export_id=export.id, actor_id=speaker.id)
    db_session.commit()

    with pytest.raises(ExportRejected):
        revoke_export(db_session, export_id=export.id, actor_id=speaker.id)
    db_session.rollback()
    with pytest.raises(ExportRejected, match="not a draft"):
        approve_export(db_session, export_id=export.id, actor_id=speaker.id,
                       manifest_id="m-7", manifest_sha256="e" * 64)


# --- Item 7: source classes stay distinguished ------------------------------


def test_each_source_class_is_stored_distinctly_and_not_merged(db_session):
    speaker = _user(db_session, "ds-classes")
    contribution = _eligible_contribution(db_session, speaker)
    export = create_export(db_session, purpose="mixed corpus", requested_by=speaker.id, rows=[
        _row(contribution, record="amazwi-1"),
        _row(source_class="EXTERNAL_LICENSED", record="ext-1"),
        _row(source_class="EVALUATION_ONLY", record="eval-1"),
        _row(source_class="SYNTHETIC_FIXTURE", record="fix-1"),
    ])
    db_session.commit()

    rows = db_session.query(DatasetExportRow).filter_by(export_id=export.id).all()
    assert {r.source_class for r in rows} == set(DatasetSourceClass)
    assert len(rows) == 4, "four classes must remain four rows, never collapsed"
    by_class = {r.source_class: r for r in rows}
    assert by_class[DatasetSourceClass.AMAZWI_OPTED_IN].consent_version == "model-v3"
    for other in (DatasetSourceClass.EXTERNAL_LICENSED, DatasetSourceClass.EVALUATION_ONLY,
                  DatasetSourceClass.SYNTHETIC_FIXTURE):
        assert by_class[other].contribution_id is None, "non-AMAZWI rows carry no speaker link"
        assert by_class[other].consent_version is None


def test_non_amazwi_rows_do_not_require_amazwi_consent(db_session):
    """Externally licensed data is governed by its licence, not by a
    speaker consent grant that does not exist for it."""
    requester = _user(db_session, "ds-external")
    db_session.commit()

    export = create_export(db_session, purpose="external eval", requested_by=requester.id, rows=[
        _row(source_class="EXTERNAL_LICENSED", record="ext-only"),
    ])
    db_session.commit()
    assert db_session.query(DatasetExportRow).filter_by(export_id=export.id).count() == 1


def test_an_opted_in_row_without_a_contribution_is_refused(db_session):
    requester = _user(db_session, "ds-orphan")
    db_session.commit()
    with pytest.raises(ExportRejected, match="require a contribution"):
        create_export(db_session, purpose="ASR training", requested_by=requester.id, rows=[
            _row(source_class="AMAZWI_OPTED_IN", record="orphan"),
        ])


def test_a_non_amazwi_row_may_not_smuggle_in_a_contribution_link(db_session):
    """The DB CHECK is the backstop for the class/link pairing."""
    speaker = _user(db_session, "ds-smuggle")
    contribution = _eligible_contribution(db_session, speaker)
    export = create_export(db_session, purpose="ASR training", requested_by=speaker.id,
                           rows=[_row(contribution)])
    db_session.commit()

    db_session.add(DatasetExportRow(
        export_id=export.id, source_class=DatasetSourceClass.EXTERNAL_LICENSED,
        source_record_id="smuggled", contribution_id=contribution.id,
        object_sha256="a" * 64, included=True,
    ))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_the_same_source_record_cannot_appear_twice_in_one_export(db_session):
    speaker = _user(db_session, "ds-dupe")
    db_session.commit()
    with pytest.raises(IntegrityError):
        create_export(db_session, purpose="ASR training", requested_by=speaker.id, rows=[
            _row(source_class="EXTERNAL_LICENSED", record="same"),
            _row(source_class="EXTERNAL_LICENSED", record="same"),
        ])
        db_session.commit()
    db_session.rollback()
