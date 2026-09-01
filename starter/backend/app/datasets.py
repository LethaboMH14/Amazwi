"""Human-approved provenance firewall for training exports."""
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import (AuditEvent, AudioObject, AudioObjectState, ConsentGrant, ConsentScope, Contribution, ContributionState, DatasetExport, DatasetExportRow, DatasetExportState, DatasetSource, DatasetSourceClass, DatasetSourceState, EligibilityDecision)

class ExportApprovalError(Exception): pass
def _now(): return datetime.now(timezone.utc)
def draft_export(session:Session, *, purpose:str, source_ids:list[str], contribution_ids:list[UUID], actor_id:UUID, now:datetime|None=None)->DatasetExport:
 now=now or _now(); export=DatasetExport(state=DatasetExportState.DRAFT,purpose=purpose,requested_by=actor_id);session.add(export);session.flush()
 for source_id in source_ids:
  source=session.get(DatasetSource,source_id)
  if source is None: raise ExportApprovalError("SOURCE_NOT_FOUND")
  included=source.state==DatasetSourceState.PREFLIGHT_PASSED and purpose in (source.allowed_tasks or [])
  session.add(DatasetExportRow(export_id=export.id,source_class=DatasetSourceClass.EXTERNAL_LICENSED,source_record_id=source.source_id,object_sha256=source.registry_sha256,included=included,exclusion_reason=None if included else "BLOCKED_LICENCE"))
 for cid in contribution_ids:
  c=session.get(Contribution,cid); audio=session.scalar(select(AudioObject).where(AudioObject.contribution_id==cid)); decision=session.get(EligibilityDecision,cid); consent=session.scalar(select(ConsentGrant).where(ConsentGrant.user_id==c.speaker_id if c else False,ConsentGrant.scope==ConsentScope.RETAIN_MODEL_DEVELOPMENT,ConsentGrant.revoked_at.is_(None))) if c else None
  included=bool(c and audio and audio.state==AudioObjectState.AVAILABLE and decision and decision.corpus_eligible and consent)
  reason=None if included else ("BLOCKED_REVOKED" if c and not consent else "REVIEW_REQUIRED")
  session.add(DatasetExportRow(export_id=export.id,source_class=DatasetSourceClass.AMAZWI_OPTED_IN,source_record_id=str(cid),contribution_id=cid,object_sha256=audio.sha256 if audio and audio.sha256 else "0"*64,consent_version=consent.version if consent else None,included=included,exclusion_reason=reason))
 session.add(AuditEvent(actor_id=actor_id,action="DATASET_EXPORT_REQUESTED",entity_type="DatasetExport",entity_id=str(export.id),event_metadata=purpose,created_at=now));session.commit();return export
def approve_export(session:Session, *, export_id:UUID, manifest_id:str, manifest_sha256:str, actor_id:UUID, now:datetime|None=None)->DatasetExport:
 now=now or _now(); export=session.scalar(select(DatasetExport).where(DatasetExport.id==export_id).with_for_update())
 if export is None: raise ExportApprovalError("EXPORT_NOT_FOUND")
 if export.state!=DatasetExportState.DRAFT: raise ExportApprovalError("EXPORT_ALREADY_FINALISED")
 if len(manifest_sha256)!=64: raise ExportApprovalError("MANIFEST_HASH_INVALID")
 rows=session.scalars(select(DatasetExportRow).where(DatasetExportRow.export_id==export_id,DatasetExportRow.included.is_(True))).all()
 if not rows: raise ExportApprovalError("EXPORT_EMPTY")
 for row in rows:
  if row.source_class==DatasetSourceClass.EXTERNAL_LICENSED:
   source=session.get(DatasetSource,row.source_record_id)
   if not source or source.state!=DatasetSourceState.PREFLIGHT_PASSED or export.purpose not in (source.allowed_tasks or []): raise ExportApprovalError("BLOCKED_LICENCE")
  else:
   c=session.get(Contribution,row.contribution_id); consent=session.scalar(select(ConsentGrant).where(ConsentGrant.user_id==c.speaker_id,ConsentGrant.scope==ConsentScope.RETAIN_MODEL_DEVELOPMENT,ConsentGrant.revoked_at.is_(None))) if c else None
   if not c or not consent: row.included=False;row.exclusion_reason="BLOCKED_REVOKED"
 if not any(r.included for r in rows): raise ExportApprovalError("BLOCKED_CONSENT")
 export.state=DatasetExportState.APPROVED;export.manifest_id=manifest_id;export.manifest_sha256=manifest_sha256;export.approved_by=actor_id;export.approved_at=now;session.add(AuditEvent(actor_id=actor_id,action="DATASET_EXPORT_APPROVED",entity_type="DatasetExport",entity_id=str(export.id),event_metadata=manifest_id,created_at=now));session.commit();return export
def revoke_export(session:Session, *, export_id:UUID, actor_id:UUID, reason:str, now:datetime|None=None)->DatasetExport:
 export=session.scalar(select(DatasetExport).where(DatasetExport.id==export_id).with_for_update());
 if export is None: raise ExportApprovalError("EXPORT_NOT_FOUND")
 export.state=DatasetExportState.REVOKED;export.revoked_at=now or _now();export.revoked_by=actor_id;session.add(AuditEvent(actor_id=actor_id,action="DATASET_EXPORT_REVOKED",entity_type="DatasetExport",entity_id=str(export.id),event_metadata=reason[:2000],created_at=export.revoked_at));session.commit();return export
