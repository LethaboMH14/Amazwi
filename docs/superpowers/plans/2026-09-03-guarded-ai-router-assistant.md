# Guarded AI Router and Assistant Implementation Plan

> **For agentic workers:** Implement task-by-task with TDD. Preserve the existing peer-verification, consent, ledger, payment, and private-audio authority boundaries.

**Goal:** Add Groq, Featherless, and optional AIML routing for advisory assistant work, plus a typed assistant intent endpoint that can explain or navigate the existing app without arbitrary actions.

**Architecture:** Keep deterministic application authority unchanged. A provider router selects a configured OpenAI-compatible text provider by task and fallback order. A guarded assistant class turns natural-language text into a small allowlisted intent set, while the API validates identity and returns navigation or explanation metadata. No model receives raw audio, private identifiers, or payment authority.

**Tech Stack:** Python 3.12, FastAPI, Pydantic, urllib, existing SQLAlchemy identity dependency, pytest.

## Global Constraints

- `AI_COUNCIL_ENABLED` remains the hard off-switch for outbound model calls.
- Groq, Featherless, and AIML are text providers only in this slice.
- Provider failures must degrade to a deterministic response, never fail the core user flow.
- Models cannot mutate consent, contribution state, peer decisions, rewards, payment state, or database rows.
- Only allowlisted navigation intents may be returned: `/`, `/consent`, `/record`, `/verify`, `/impact`, `/ops`, `/dashboard`, `/rewards`.
- Do not log API keys, raw audio, or provider request bodies.

### Task 1: Provider routing

**Files:**
- Modify: `starter/backend/app/llm.py`
- Create: `starter/backend/tests/test_llm.py`
- Modify: `starter/backend/.env.example`

**Interfaces:**
- `resolve_provider(task: str = "general") -> ProviderConfig | None`
- `ProviderConfig` gains a provider role/task selection without breaking existing callers.
- Provider order is task-specific: `fast` tries Groq, Featherless, AIML; `reasoning` tries Featherless, AIML, Groq; `general` follows configured `AMAZWI_AI_PROVIDER_ORDER` or the default `groq,featherless,aiml`.

Test first for configured-provider selection, fallback on missing keys, unknown provider names ignored, disabled mode returning `None`, and no secret leakage in errors. Then implement the smallest router and env documentation.

### Task 2: Guarded assistant contract

**Files:**
- Create: `starter/backend/app/assistant.py`
- Create: `starter/backend/tests/test_assistant.py`
- Modify: `starter/backend/app/api_types.py`

**Interfaces:**
- `AssistantRequest(message: str, language: str = "en")`
- `AssistantResponse(reply: str, intent: str, route: str | None, provider: str, advisory: bool)`
- `handle_assistant_message(message: str, language: str, *, model_text: Callable | None = None) -> AssistantResponse`

The deterministic layer recognizes route aliases and safe receipt/reward explanations. Unknown or sensitive requests return a bounded explanation and no route. A model-produced result, if added later, must be parsed into the same allowlisted contract.

### Task 3: Public assistant endpoint

**Files:**
- Create: `starter/backend/app/routes/assistant.py`
- Modify: `starter/backend/app/routes/__init__.py`
- Modify: `starter/backend/app/main.py`
- Create: `starter/backend/tests/test_assistant_api.py`

**Interfaces:**
- `POST /assistant` and `/api/assistant`
- Requires the existing persisted identity headers.
- Returns the typed assistant response and never accepts tool names, URLs, SQL, provider selection, or payment instructions from the caller.

Test authenticated success, identity mismatch, safe navigation, sensitive-action refusal, and provider-disabled fallback through FastAPI's real route contract.

### Verification

Run targeted tests first, then the backend suite, frontend suite/build, content validators, and a live isolated FastAPI smoke test with provider calls disabled. Confirm existing routes remain unchanged.
