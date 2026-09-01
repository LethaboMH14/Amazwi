"""Governed dataset-export service.

Export rows are a separate data plane. This service never changes peer decisions,
rewards, wallets, or contribution authority state.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import (
    AudioObject, AudioObjectState, ConsentGrant, ConsentScope, Contribution,
    ContributionState, DatasetExport, DatasetExportRow, DatasetExportState,
    DatasetSourceClass,
)

class ExportRejected(ValueError):
    pass


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _active_consent(session: Session, user_id: UUID) -> ConsentGrant | None:
    return session.scalar(select(ConsentGrant).where(
        ConsentGrant.user_id == user_id,
        ConsentGrant.scope == ConsentScope.RETAIN_MODEL_DEVELOPMENT,
        ConsentGrant.revoked_at.is_(None),
    ))


def create_export(session: Session, *, purpose: str, requested_by: UUID, rows: Iterable[dict]) -> DatasetExport:
    if not purpose:
        raise ExportRejected("purpose is required")
    export = DatasetExport(state=DatasetExportState.DRAFT, purpose=purpose, requested_by=requested_by)
    session.add(export)
    session.flush()
    for item in rows:
        source_class = DatasetSourceClass(item["source_class"])
        contribution_id = item.get("contribution_id")
        consent_version = item.get("consent_version")
        if source_class == DatasetSourceClass.AMAZWI_OPTED_IN:
            if not contribution_id:
                raise ExportRejected("opted-in rows require a contribution")
            contribution = session.get(Contribution, contribution_id)
            audio = session.scalar(select(AudioObject).where(AudioObject.contribution_id == contribution_id))
            consent = _active_consent(session, contribution.speaker_id) if contribution else None
            if not contribution or contribution.state != ContributionState.CORPUS_ELIGIBLE:
                raise ExportRejected("only corpus-eligible contributions may be exported")
            if not audio or audio.state != AudioObjectState.AVAILABLE:
                raise ExportRejected("audio must be available")
            if not consent:
                raise ExportRejected("active model-development consent is required")
            consent_version = consent.version
        session.add(DatasetExportRow(export_id=export.id, source_class=source_class,
            source_record_id=str(item["source_record_id"]), contribution_id=contribution_id,
            object_sha256=item["object_sha256"], consent_version=consent_version,
            included=bool(item.get("included", True)), exclusion_reason=item.get("exclusion_reason")))
    return export


def approve_export(session: Session, *, export_id: UUID, actor_id: UUID, manifest_id: str, manifest_sha256: str) -> DatasetExport:
    export = session.get(DatasetExport, export_id)
    if not export or export.state != DatasetExportState.DRAFT:
        raise ExportRejected("export is not a draft")
    if len(manifest_sha256) != 64:
        raise ExportRejected("manifest sha256 is required")
    rows = list(session.scalars(select(DatasetExportRow).where(DatasetExportRow.export_id == export_id)))
    if not rows or not all(row.included for row in rows):
        raise ExportRejected("approved exports require included rows")
    export.state = DatasetExportState.APPROVED
    export.approved_by = actor_id
    export.approved_at = _now()
    export.manifest_id = manifest_id
    export.manifest_sha256 = manifest_sha256
    return export


def revoke_export(session: Session, *, export_id: UUID, actor_id: UUID) -> DatasetExport:
    export = session.get(DatasetExport, export_id)
    if not export or export.state != DatasetExportState.APPROVED:
        raise ExportRejected("only approved exports may be revoked")
    export.state = DatasetExportState.REVOKED
    export.revoked_by = actor_id
    export.revoked_at = _now()
    return export
