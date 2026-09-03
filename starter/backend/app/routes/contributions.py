from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Iterator
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Header
from sqlalchemy import select, func
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
from app.models import Assignment, AudioObject, Card, ConsentScope, Contribution, User
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


@router.get("/cards/next")
def next_card(
    language: str,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
):
    """A card to record in `language`, chosen at random from active cards.

    Added because the recording screen hardcoded a single isiZulu card id,
    so every contribution in the entire product was the same word and
    Setswana was unreachable from the UI despite having a full reviewed
    deck in the database.

    Random rather than sequential: two speakers in the same room should
    not be handed the same word, and a fixed order makes a demo look
    scripted. Returns exactly the SPEAKER projection -- target and blocked
    words, never accepted_answers or distractors.

    NOTE: this route must be declared BEFORE /cards/{card_id}. FastAPI
    matches in declaration order, so the parameterised route would
    otherwise swallow "next" as a card id and 404 every request.
    """
    require_identity_user(session, identity)
    card = session.scalar(
        select(Card)
        .where(Card.language == language, Card.active.is_(True))
        .order_by(func.random())
        .limit(1)
    )
    if card is None:
        raise HTTPException(status_code=404, detail={"code": "NO_CARD_FOR_LANGUAGE"})
    return {
        "id": str(card.id),
        "language": card.language,
        "target": card.target,
        "blocked_words": list(card.blocked_words),
    }


@router.get("/cards/{card_id}")
def get_card(
    card_id: str,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
):
    """The card a SPEAKER is about to describe: target plus blocked words.

    Both fields are exactly what the speaker is being asked to work with, so
    withholding them is what breaks the game -- the recording screen said
    "Say the card aloud" and showed no card at all until 2 Sep 2026.

    Deliberately NOT a verifier leak: a verifier never learns a card_id until
    routes/assignments.py reveals it, which only happens after their answer is
    locked. Knowing the id is the capability here. Authentication is still
    required so this is not an open corpus dump.
    """
    require_identity_user(session, identity)
    try:
        card = session.get(Card, uuid.UUID(card_id))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail={"code": "CARD_NOT_FOUND"}) from exc
    if card is None:
        raise HTTPException(status_code=404, detail={"code": "CARD_NOT_FOUND"})
    return {
        "id": str(card.id),
        "language": card.language,
        "target": card.target,
        "blocked_words": list(card.blocked_words),
    }


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
    # The speaker must be able to SEE the card they are describing -- the
    # target word and the four words they may not say ARE the game. Without
    # this the recording screen says "Say the card aloud" and shows no card,
    # which is what it did until 2 Sep 2026.
    #
    # Safe to return here specifically because this is the contribution's own
    # speaker, who by definition already knows the target: they are being
    # asked to describe it. This is NOT the verifier path -- assignments.py
    # deliberately withholds the card until a verifier has locked their answer
    # (routes/assignments.py), and that asymmetry is the whole integrity
    # model. Do not reuse this shape on any verifier-facing route.
    card = session.get(Card, contribution.card_id)
    return {
        "id": str(contribution.id),
        "state": contribution.state.value,
        "reward_rule_id": str(contribution.reward_rule_id),
        "card": None
        if card is None
        else {
            "id": str(card.id),
            "language": card.language,
            "target": card.target,
            "blocked_words": list(card.blocked_words),
        },
    }


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
    x_user_id: str | None = Header(default=None),
    session: Session = Depends(get_session),
    store: LocalAudioObjectStore = Depends(get_audio_store),
):
    """Stream a private clip, authorised by the SIGNED TOKEN itself.

    The acting user is taken from the token's `aud` claim rather than
    from an X-User-ID header, and that is a security IMPROVEMENT, not a
    relaxation:

      * the header identity (app/identity.py) carries NO signature -- it
        is an unsigned assertion that anyone who knows a valid pair can
        make;
      * the playback token is HMAC-signed with a server secret, bound to
        one audience, bound to one purpose, and expires in five minutes.

    Every consent and assignment check below is unchanged. They simply
    key on the token's audience instead of on an unsigned header, and
    `store.open_private` still verifies the signature, the expiry, the
    audience and the purpose before a byte is read.

    This also fixes the only real client. An <audio> element CANNOT send
    headers, so requiring one meant playback worked solely because a dev
    proxy injected it -- and broke completely anywhere that proxy is not
    present, which is every deployment target.

    When a header IS supplied it must still agree with the token, so a
    device that sends one gets defence in depth rather than a bypass.
    """
    try:
        now = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        payload = store.token_payload(token)

        raw_audience = payload.get("aud")
        if not isinstance(raw_audience, str):
            raise InvalidAudioToken("audio token has no audience")
        try:
            acting_user_id = uuid.UUID(raw_audience)
        except ValueError as exc:
            raise InvalidAudioToken("audio token audience is not a user id") from exc

        # Defence in depth: a caller that DOES present a header must not be
        # able to present a different one from the token it is redeeming.
        if x_user_id:
            try:
                if uuid.UUID(x_user_id) != acting_user_id:
                    raise InvalidAudioToken("header identity does not match the token")
            except ValueError as exc:
                raise InvalidAudioToken("header identity is not a user id") from exc

        actor = session.get(User, acting_user_id)
        if actor is None:
            raise InvalidAudioToken("audio token audience is not a known user")

        audio = session.scalar(select(AudioObject).where(AudioObject.object_key == payload.get("key")))
        contribution = session.get(Contribution, audio.contribution_id) if audio else None
        if contribution is None:
            raise InvalidAudioToken("audio token is not authorised for this user")
        if payload.get("purpose") == "REPLAY":
            if contribution.speaker_id != acting_user_id:
                raise InvalidAudioToken("audio token is not authorised for this user")
            require_active_scope(session, acting_user_id, ConsentScope.RECORD_PROCESS_ROUND)
        elif payload.get("purpose") == "VERIFY":
            assignment = session.scalar(select(Assignment).where(
                Assignment.contribution_id == contribution.id,
                Assignment.verifier_id == acting_user_id,
            ))
            if assignment is None:
                raise InvalidAudioToken("audio token is not authorised for this user")
            require_active_scope(session, contribution.speaker_id, ConsentScope.ASSIGNED_VERIFIER_PLAYBACK)
            require_active_scope(session, acting_user_id, ConsentScope.ASSIGNED_VERIFIER_PLAYBACK)
        else:
            raise InvalidAudioToken("audio token has an invalid purpose")
        body = store.open_private(
            token,
            audience=str(acting_user_id),
            now=now,
            purpose=payload.get("purpose"),
        ).read()
    except (InvalidAudioToken, AudioUnavailable, ConsentRequiredError) as exc:
        raise HTTPException(status_code=403, detail={"code": "AUDIO_NOT_AUTHORISED"}) from exc
    return Response(content=body, media_type=audio.mime_type or "application/octet-stream")
