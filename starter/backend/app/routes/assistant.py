from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.assistant import handle_assistant_message
from app.api_types import AssistantRequest, AssistantResponse
from app.db import get_session
from app.identity import AuthenticatedIdentity, get_current_identity, require_identity_user

router = APIRouter(tags=["assistant"])


@router.post("/assistant", response_model=AssistantResponse)
@router.post("/api/assistant", response_model=AssistantResponse, include_in_schema=False)
def assistant_message(
    request: AssistantRequest,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
    session: Session = Depends(get_session),
) -> AssistantResponse:
    require_identity_user(session, identity)
    result = handle_assistant_message(request.message, request.language)
    return AssistantResponse(
        reply=result.reply,
        intent=result.intent,
        route=result.route,
        provider=result.provider,
        advisory=result.advisory,
    )
