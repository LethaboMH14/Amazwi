from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Iterator
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api_types import AudioFinaliseRequest, AudioUploadResponse, ContributionCreateRequest, PlaybackResponse
from app.audio import get_audio_store
from app.contributions import (
    AudioNotAuthorised,
    begin_audio_upload,
    create_contribution,
    finalise_audio,
    issue_contributor_playback_token,
)
from app.consent import ConsentRequiredError
from app.consent import require_active_scope
from app.db import get_session
from app.identity import AuthenticatedIdentity, get_current_identity, require_identity_user
from app.models import Assignment, AudioObject, ConsentScope, Contribution
from app.storage import AudioUnavailable, InvalidAudioToken, LocalAudioObjectStore


router = APIRouter(tags=["contributions", "audio"])


@contextmanager
def _transaction(session: Session) -> Iterator[None]:
    transaction = session.begin_nested() if session.in_transaction() else session.begin()
    with transaction:
        yield


def _error(exc: Exception) -> HTTPException:
    code = str(exc)
    if isinstance(exc, ConsentRequiredError):
        code = "CONSENT_REQUIRED"
    mapping = {
        "CONSENT_REQUIRED": 403,
        "CAMPAIGN_REWARD_NOT_CONFIGURED": 409,
        "AUDIO_FORMAT_UNSUPPORTED": 415,
        "AUDIO_DURATION_INVALID": 422,
        "AUDIO_NOT_AUTHORISED": 403,
        "AUDIO_UNAVAILABLE": 404,
        "AUDIO_HASH_MISMATCH": 422,
    }
    return HTTPException(status_code=mapping.get(code, 400), detail={"code": code})


@router.post("/contributions", status_code=status.HTTP_201_CREATED)
def create_contribution_route(
    request: ContributionCreateRequest,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
):
    try:
        require_identity_user(session, identity)
        with _transaction(session):
            contribution = create_contribution(
                session, principal=identity, card_id=uuid.UUID(request.card_id)
            )
        session.commit()
    except Exception as exc:
        if isinstance(exc, HTTPException):
            raise
        raise _error(exc) from exc
    return {"id": str(contribution.id), "state": contribution.state.value, "reward_rule_id": str(contribution.reward_rule_id)}


@router.post("/contributions/{contribution_id}/audio/uploads", response_model=AudioUploadResponse)
def create_audio_upload(
    contribution_id: uuid.UUID,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
    store: LocalAudioObjectStore = Depends(get_audio_store),
):
    try:
        require_identity_user(session, identity)
        with _transaction(session):
            audio = begin_audio_upload(session, store, contribution_id, identity.user_id)
        session.commit()
    except Exception as exc:
        raise _error(exc) from exc
    return AudioUploadResponse(audio_object_id=str(audio.id), object_key=audio.object_key)


@router.put("/private-audio/uploads/{audio_object_id}")
async def upload_audio(
    audio_object_id: uuid.UUID,
    request: Request,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
    store: LocalAudioObjectStore = Depends(get_audio_store),
):
    audio = session.get(AudioObject, audio_object_id)
    require_identity_user(session, identity)
    if audio is None:
        raise HTTPException(status_code=404, detail={"code": "AUDIO_UNAVAILABLE"})
    contribution = session.get(Contribution, audio.contribution_id)
    if contribution is None or contribution.speaker_id != identity.user_id:
        raise HTTPException(status_code=403, detail={"code": "AUDIO_NOT_AUTHORISED"})
    try:
        require_active_scope(session, identity.user_id, ConsentScope.RECORD_PROCESS_ROUND)
    except ConsentRequiredError as exc:
        raise _error(exc) from exc
    try:
        store.write_upload(audio.object_key, await request.body())
    except Exception as exc:
        raise _error(exc) from exc
    return {"status": "uploaded"}


@router.post("/contributions/{contribution_id}/audio/finalise")
def finalise_audio_route(
    contribution_id: uuid.UUID,
    request: AudioFinaliseRequest,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
    store: LocalAudioObjectStore = Depends(get_audio_store),
):
    try:
        require_identity_user(session, identity)
        with _transaction(session):
            contribution = session.get(Contribution, contribution_id)
            if contribution is None or contribution.speaker_id != identity.user_id:
                raise AudioNotAuthorised("AUDIO_NOT_AUTHORISED")
            audio = finalise_audio(session, store, contribution_id, **request.model_dump())
        session.commit()
    except Exception as exc:
        raise _error(exc) from exc
    return {"audio_object_id": str(audio.id), "state": audio.state.value}


@router.post("/contributions/{contribution_id}/playback", response_model=PlaybackResponse)
def contributor_playback(
    contribution_id: uuid.UUID,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
    store: LocalAudioObjectStore = Depends(get_audio_store),
):
    try:
        require_identity_user(session, identity)
        token = issue_contributor_playback_token(session, store, contribution_id, identity)
    except Exception as exc:
        raise _error(exc) from exc
    return PlaybackResponse(url=f"/private-audio/play/{token}")


@router.get("/private-audio/play/{token}")
def play_audio(
    token: str,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
    store: LocalAudioObjectStore = Depends(get_audio_store),
):
    try:
        require_identity_user(session, identity)
        now = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        payload = store.token_payload(token)
        audio = session.scalar(select(AudioObject).where(AudioObject.object_key == payload.get("key")))
        contribution = session.get(Contribution, audio.contribution_id) if audio else None
        if contribution is None:
            raise InvalidAudioToken("audio token is not authorised for this user")
        if payload.get("purpose") == "REPLAY":
            if contribution.speaker_id != identity.user_id:
                raise InvalidAudioToken("audio token is not authorised for this user")
            require_active_scope(session, identity.user_id, ConsentScope.RECORD_PROCESS_ROUND)
        elif payload.get("purpose") == "VERIFY":
            assignment = session.scalar(select(Assignment).where(
                Assignment.contribution_id == contribution.id,
                Assignment.verifier_id == identity.user_id,
            ))
            if assignment is None:
                raise InvalidAudioToken("audio token is not authorised for this user")
            require_active_scope(session, contribution.speaker_id, ConsentScope.ASSIGNED_VERIFIER_PLAYBACK)
            require_active_scope(session, identity.user_id, ConsentScope.ASSIGNED_VERIFIER_PLAYBACK)
        else:
            raise InvalidAudioToken("audio token has an invalid purpose")
        body = store.open_private(
            token,
            audience=str(identity.user_id),
            now=now,
            purpose=payload.get("purpose"),
        ).read()
    except (InvalidAudioToken, AudioUnavailable, ConsentRequiredError) as exc:
        raise HTTPException(status_code=403, detail={"code": "AUDIO_NOT_AUTHORISED"}) from exc
    return Response(content=body, media_type=audio.mime_type or "application/octet-stream")
