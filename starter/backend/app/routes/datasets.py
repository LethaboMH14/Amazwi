from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.datasets import ExportRejected, approve_export, create_export, revoke_export
from app.db import get_session
from app.identity import AuthenticatedIdentity, get_current_identity, require_identity_user

router = APIRouter(prefix="/dataset-exports", tags=["dataset-exports"])

class ExportRowDTO(BaseModel):
    source_class: str
    source_record_id: str
    object_sha256: str
    contribution_id: UUID | None = None
    included: bool = True
    exclusion_reason: str | None = None

class ExportDraftDTO(BaseModel):
    purpose: str
    rows: list[ExportRowDTO]

class ExportApprovalDTO(BaseModel):
    manifest_id: str
    manifest_sha256: str

@router.post("", status_code=201)
def draft_export(body: ExportDraftDTO, identity: AuthenticatedIdentity = Depends(get_current_identity), session: Session = Depends(get_session)):
    require_identity_user(session, identity)
    try:
        export = create_export(session, purpose=body.purpose, requested_by=identity.user_id, rows=[row.model_dump() for row in body.rows])
        session.commit()
        return {"id": str(export.id), "state": export.state.value}
    except ExportRejected as exc:
        session.rollback()
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@router.post("/{export_id}/approve")
def approve(export_id: UUID, body: ExportApprovalDTO, identity: AuthenticatedIdentity = Depends(get_current_identity), session: Session = Depends(get_session)):
    require_identity_user(session, identity)
    try:
        export = approve_export(session, export_id=export_id, actor_id=identity.user_id, manifest_id=body.manifest_id, manifest_sha256=body.manifest_sha256)
        session.commit()
        return {"id": str(export.id), "state": export.state.value, "manifest_sha256": export.manifest_sha256}
    except ExportRejected as exc:
        session.rollback()
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@router.post("/{export_id}/revoke")
def revoke(export_id: UUID, identity: AuthenticatedIdentity = Depends(get_current_identity), session: Session = Depends(get_session)):
    require_identity_user(session, identity)
    try:
        export = revoke_export(session, export_id=export_id, actor_id=identity.user_id)
        session.commit()
        return {"id": str(export.id), "state": export.state.value}
    except ExportRejected as exc:
        session.rollback()
        raise HTTPException(status_code=422, detail=str(exc)) from exc
