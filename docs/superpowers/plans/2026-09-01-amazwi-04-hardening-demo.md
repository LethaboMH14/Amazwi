# AMAZWI Stage 9 Hardening and Demonstration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harden the integrated AMAZWI workflow and produce repeatable, honest evidence that browser → API → private storage → two peers → resolver → reward → outbox → Council → receipt survives two deterministic reset cycles and every declared failure drill.

**Architecture:** Add fail-closed typed configuration, explicit OIDC-versus-demo authentication boundaries, a process-local rate-limiter adapter that production configuration rejects, recursive secret/PII sanitisation, and demo-only deterministic seed/reset and fault injection. Drive the complete system through Playwright with three independent browser contexts, collect target-device/accessibility/performance evidence from the running app, package truthful offline fallback artefacts, and expand CI without selecting or resuming a deployment target.

**Tech Stack:** Python 3.11+, FastAPI, Pydantic Settings, SQLAlchemy 2, PostgreSQL 16, pytest, structlog, PyJWT, React 18, TypeScript 5.5, Vite 5, Vitest, Testing Library, Playwright, axe-core, Chrome DevTools Protocol, ffmpeg, GitHub Actions.

## Global Constraints

- All constraints in `docs/superpowers/plans/2026-09-01-amazwi-governed-intelligence-program.md` apply.
- Execute this plan only after Stages 1–8 form one integrated local workflow.
- Peer verification remains authoritative. AI is post-resolution and advisory only.
- The rate limiter implemented here is process-local and single-node only. It must never be described as distributed or multi-node production protection.
- `POST /demo/seed`, `POST /demo/reset`, and all failure-injection controls are unavailable in production, even when a caller knows a demo token.
- Production startup fails if demo auth, demo provider, in-memory rate limiting, deterministic reset, fault injection, wildcard CORS, or a default/blank secret is configured.
- Logs, error payloads, receipts, screenshots, traces, videos, and CI artefacts contain no bearer tokens, cookies, signed audio URLs, object keys, raw phone numbers, email addresses, raw free-text answers, or provider request/response bodies.
- Automated tests use `DEMO_PROVIDER`; no test calls a MoMo sandbox or production provider.
- Failure drills cover storage, consent, outbox, AI, payment provider, model, and motion failures without weakening the peer/reward path.
- Two complete reset-and-demo cycles must pass consecutively against PostgreSQL 16 with identical seeded IDs and no duplicated reward, Council output, outbox completion, or receipt.
- Target UI evidence covers 320–480px widths, 200% zoom, keyboard operation, automated accessibility checks, reduced motion, screen-reader semantics, and a low/mid-range Android performance profile.
- Fallback recordings must be captured from the real running golden path. Static mockups may be labelled design references only and cannot be presented as running-product evidence.
- The paused Vercel deployment remains paused. This plan creates no deployment config, performs no deployment command, and does not resume deployment work.
- Backend, auth, money, data, provider, CI, and deployment-safety changes are cross-lane work pending Sbu review. Record that status without claiming Sbu sign-off.
- TDD is mandatory. Each task begins with a failing test, reaches green, runs its broader gate, and ends in a focused commit.

---

## Locked File Structure

### Backend hardening

- `starter/backend/app/config.py`: validated environment, auth, demo, CORS, provider and rate-limit settings.
- `starter/backend/app/auth.py`: authenticated identity, OIDC verification and demo-session verification.
- `starter/backend/app/rate_limit.py`: adapter protocol and process-local sliding-window implementation.
- `starter/backend/app/sanitise.py`: recursive secret and PII redaction for logs and public DTOs.
- `starter/backend/app/logging.py`: structlog setup and request-context logging.
- `starter/backend/app/demo.py`: deterministic seed/reset service and fixed UUID catalogue.
- `starter/backend/app/faults.py`: demo/test-only failure catalogue and dependency wrappers.
- `starter/backend/app/routes/demo.py`: authenticated demo seed/reset/fault routes.
- `starter/backend/app/routes/receipts.py`: sanitised receipt response mapping.
- `starter/backend/scripts/demo_cycle.py`: non-interactive two-cycle API drill.

### Browser and evidence

- `starter/frontend/playwright.config.ts`: local three-context and target-device projects.
- `starter/frontend/e2e/fixtures.ts`: demo identities, reset helper and failure-control helper.
- `starter/frontend/e2e/golden-path.spec.ts`: complete browser-to-receipt proof and two reset cycles.
- `starter/frontend/e2e/failure-drills.spec.ts`: storage, consent, outbox, AI, provider, model and motion drills.
- `starter/frontend/e2e/accessibility-performance.spec.ts`: zoom, keyboard, axe, reduced-motion and performance collection.
- `starter/frontend/scripts/assert-evidence.mjs`: machine-checkable evidence completeness and budget checks.
- `starter/frontend/public/fallback/impact-static.svg`: static Impact fallback used when motion/WebGL is cut.

### Operator evidence and CI

- `starter/evidence/stage-09/README.md`: evidence index, commands, hashes and limitations.
- `starter/evidence/stage-09/manifest.json`: generated artefact hashes and verification outcomes.
- `starter/evidence/stage-09/failure-matrix.json`: generated drill results.
- `starter/evidence/stage-09/accessibility.json`: generated accessibility results.
- `starter/evidence/stage-09/performance.json`: generated target-device measurements.
- `starter/evidence/stage-09/screenshots/`: running-app screenshots only.
- `starter/evidence/stage-09/fallback/amazwi-golden-path.mp4`: real local golden-path capture.
- `starter/evidence/stage-09/fallback/amazwi-golden-path.webm`: browser-safe duplicate of the same capture.
- `starter/evidence/stage-09/fallback/SHA256SUMS.txt`: fallback artefact hashes.
- `starter/evidence/stage-09/fallback/RECOVERY_CARD.md`: exact offline narration and substitution disclosures.
- `starter/scripts/run-stage-09.ps1`: Windows orchestration for backend, frontend, two resets, drills and evidence.
- `.github/workflows/ci.yml`: backend hardening, frontend unit/build, Playwright, evidence validation and secret scan jobs.
- `05_amazwi/plan/15_DEMO_SCRIPT.md`: replace the “fallback not producible” status only after the real capture passes.
- `05_amazwi/BUILD_LOG.md`: append-only Stage 9 evidence and cross-lane review status.
- `HANDOVER_SBU.md`: exact files, commands, evidence, risks and pending-review request.

---

### Task 1: Config validation and fail-closed startup

**Files:**
- Create: `starter/backend/app/config.py`
- Create: `starter/backend/tests/test_config.py`
- Modify: `starter/backend/app/main.py`
- Modify: `starter/backend/requirements.txt`

**Interfaces:**
- Produces: `Environment`, `AuthMode`, `RateLimitBackend`, `Settings`, `get_settings() -> Settings`.
- Produces: `create_app(settings: Settings | None = None) -> FastAPI`.
- Enforces: production rejects demo auth/provider/routes/faults, wildcard CORS, in-memory rate limiting and weak secrets.

- [ ] **Step 1: Write failing configuration tests**

```python
import pytest
from pydantic import ValidationError

from app.config import Settings


def test_production_rejects_every_demo_only_boundary():
    with pytest.raises(ValidationError) as error:
        Settings(
            environment="production",
            database_url="postgresql://amazwi:secret@db/amazwi",
            auth_mode="demo",
            oidc_issuer=None,
            oidc_audience=None,
            oidc_jwks_url=None,
            demo_admin_token="demo-admin-token-32-bytes-long!!",
            demo_routes_enabled=True,
            fault_injection_enabled=True,
            provider_mode="DEMO_PROVIDER",
            rate_limit_backend="memory",
            cors_origins=["*"],
            receipt_hash_key="receipt-hash-key-32-bytes-long",
            log_hash_key="log-hash-key-32-bytes-long!!!",
        )
    message = str(error.value)
    assert "production requires auth_mode=oidc" in message
    assert "production forbids demo routes" in message
    assert "production forbids fault injection" in message
    assert "memory rate limiting is single-node only" in message
    assert "production forbids DEMO_PROVIDER" in message
    assert "production forbids wildcard CORS" in message


def test_demo_configuration_is_explicit_and_valid():
    settings = Settings(
        environment="demo",
        database_url="postgresql://postgres:postgres@localhost:5432/amazwi_demo",
        auth_mode="demo",
        demo_admin_token="demo-admin-token-32-bytes-long!!",
        demo_routes_enabled=True,
        fault_injection_enabled=True,
        provider_mode="DEMO_PROVIDER",
        rate_limit_backend="memory",
        cors_origins=["http://127.0.0.1:4173"],
        receipt_hash_key="receipt-hash-key-32-bytes-long",
        log_hash_key="log-hash-key-32-bytes-long!!!",
    )
    assert settings.is_demo is True
    assert settings.is_production is False
```

- [ ] **Step 2: Run the tests and confirm configuration is absent**

Run: `cd starter/backend && python -m pytest tests/test_config.py -v`

Expected: collection fails because `app.config` does not exist.

- [ ] **Step 3: Implement exact settings and cross-field validation**

```python
from enum import Enum
from functools import lru_cache
from pydantic import AnyHttpUrl, Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TEST = "test"
    DEMO = "demo"
    PRODUCTION = "production"


class AuthMode(str, Enum):
    DEMO = "demo"
    OIDC = "oidc"


class RateLimitBackend(str, Enum):
    MEMORY = "memory"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AMAZWI_", case_sensitive=False)

    environment: Environment = Environment.DEVELOPMENT
    database_url: str
    auth_mode: AuthMode
    oidc_issuer: AnyHttpUrl | None = None
    oidc_audience: str | None = None
    oidc_jwks_url: AnyHttpUrl | None = None
    demo_admin_token: SecretStr | None = None
    demo_routes_enabled: bool = False
    fault_injection_enabled: bool = False
    provider_mode: str
    rate_limit_backend: RateLimitBackend = RateLimitBackend.MEMORY
    cors_origins: list[str] = Field(default_factory=list)
    receipt_hash_key: SecretStr
    log_hash_key: SecretStr

    @property
    def is_demo(self) -> bool:
        return self.environment is Environment.DEMO

    @property
    def is_production(self) -> bool:
        return self.environment is Environment.PRODUCTION

    @model_validator(mode="after")
    def validate_boundaries(self):
        errors: list[str] = []
        for name in ("receipt_hash_key", "log_hash_key"):
            value = getattr(self, name).get_secret_value()
            if len(value) < 32 or value.lower() in {"changeme", "secret", "default"}:
                errors.append(f"{name} must contain at least 32 non-default characters")
        if self.demo_admin_token and len(self.demo_admin_token.get_secret_value()) < 32:
            errors.append("demo_admin_token must contain at least 32 characters")
        if self.is_production:
            if self.auth_mode is not AuthMode.OIDC:
                errors.append("production requires auth_mode=oidc")
            if not all((self.oidc_issuer, self.oidc_audience, self.oidc_jwks_url)):
                errors.append("production requires oidc_issuer, oidc_audience and oidc_jwks_url")
            if self.demo_routes_enabled:
                errors.append("production forbids demo routes")
            if self.fault_injection_enabled:
                errors.append("production forbids fault injection")
            if self.provider_mode == "DEMO_PROVIDER":
                errors.append("production forbids DEMO_PROVIDER")
            if self.rate_limit_backend is RateLimitBackend.MEMORY:
                errors.append("memory rate limiting is single-node only and forbidden in production")
            if "*" in self.cors_origins:
                errors.append("production forbids wildcard CORS")
        if self.demo_routes_enabled and not self.is_demo:
            errors.append("demo routes require environment=demo")
        if self.fault_injection_enabled and not self.is_demo:
            errors.append("fault injection requires environment=demo")
        if self.auth_mode is AuthMode.DEMO and not self.is_demo:
            errors.append("demo auth requires environment=demo")
        if errors:
            raise ValueError("; ".join(errors))
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

Add exact dependencies to `requirements.txt`:

```text
pydantic-settings==2.10.1
structlog==25.4.0
PyJWT[crypto]==2.10.1
```

- [ ] **Step 4: Convert app startup to a settings-driven factory**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or get_settings()
    app = FastAPI(title="AMAZWI")
    app.state.settings = resolved
    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved.cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type", "X-Demo-Admin-Token"],
        allow_credentials=True,
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {
            "status": "ok",
            "environment": resolved.environment.value,
            "provider_mode": resolved.provider_mode,
            "rate_limit_scope": "single-process" if resolved.rate_limit_backend.value == "memory" else "unknown",
        }

    return app


app = create_app()
```

- [ ] **Step 5: Run focused and existing backend tests**

Run: `cd starter/backend && python -m pytest tests/test_config.py tests/test_provider.py tests/test_resolver.py -v`

Expected: all pass; `/health` says `single-process` rather than implying distributed protection.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/config.py starter/backend/app/main.py starter/backend/requirements.txt starter/backend/tests/test_config.py
git commit -m "Security: validate environment boundaries at startup"
```

---

### Task 2: OIDC and demo authentication boundaries

**Files:**
- Create: `starter/backend/app/auth.py`
- Create: `starter/backend/tests/test_auth.py`
- Create: `starter/backend/tests/test_auth_api.py`
- Modify: `starter/backend/app/main.py`
- Modify: `starter/backend/app/routes/consents.py`
- Modify: `starter/backend/app/routes/audio.py`
- Modify: `starter/backend/app/routes/assignments.py`
- Modify: `starter/backend/app/routes/receipts.py`

**Interfaces:**
- Produces: `Role`, `Identity`, `get_identity(request: Request) -> Identity`, `require_role(*roles: Role)`.
- Demo auth consumes: signed `amazwi_demo_session` cookie created only by `POST /sessions/demo` in demo mode.
- OIDC auth consumes: `Authorization: Bearer <JWT>` and validates issuer, audience, signature, expiry and subject.
- Routes derive user identity from the authenticated subject; request bodies cannot choose `user_id`, `speaker_id`, `verifier_id` or `actor_id`.

- [ ] **Step 1: Write failing boundary tests**

```python
def test_demo_cookie_is_rejected_outside_demo(client_factory, production_settings):
    client = client_factory(production_settings)
    response = client.get("/wallet", cookies={"amazwi_demo_session": "signed-demo-cookie"})
    assert response.status_code == 401


def test_body_cannot_impersonate_another_user(demo_client, demo_speaker):
    response = demo_client.post(
        "/consents",
        json={
            "user_id": "00000000-0000-0000-0000-000000000999",
            "version": "2026-09-01",
            "scopes": ["RECORD_PROCESS_ROUND"],
        },
        cookies=demo_speaker.cookies,
    )
    assert response.status_code == 422
    assert "user_id" in response.text


def test_oidc_rejects_wrong_audience(oidc_client, jwt_for):
    token = jwt_for(subject="speaker-1", audience="wrong-audience")
    response = oidc_client.get("/wallet", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json()["detail"] == "invalid authentication token"
```

- [ ] **Step 2: Run the tests and confirm auth is missing**

Run: `cd starter/backend && python -m pytest tests/test_auth.py tests/test_auth_api.py -v`

Expected: tests fail because `Identity` and authentication dependencies do not exist.

- [ ] **Step 3: Implement exact identity and verifier contracts**

```python
from dataclasses import dataclass
from enum import Enum
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, Request
from jwt import PyJWKClient

from app.config import AuthMode, Settings


class Role(str, Enum):
    SPEAKER = "speaker"
    VERIFIER = "verifier"
    OPS = "ops"
    DEMO_ADMIN = "demo_admin"


@dataclass(frozen=True)
class Identity:
    user_id: UUID
    subject: str
    roles: frozenset[Role]


def _unauthorised() -> HTTPException:
    return HTTPException(status_code=401, detail="invalid authentication token")


def verify_oidc(token: str, settings: Settings) -> dict:
    try:
        key = PyJWKClient(str(settings.oidc_jwks_url)).get_signing_key_from_jwt(token).key
        return jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            issuer=str(settings.oidc_issuer),
            audience=settings.oidc_audience,
            options={"require": ["exp", "iat", "sub"]},
        )
    except jwt.PyJWTError as exc:
        raise _unauthorised() from exc


async def get_identity(request: Request) -> Identity:
    settings: Settings = request.app.state.settings
    if settings.auth_mode is AuthMode.DEMO:
        payload = request.app.state.demo_sessions.verify(request.cookies.get("amazwi_demo_session"))
    else:
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            raise _unauthorised()
        payload = verify_oidc(header.removeprefix("Bearer "), settings)
    return Identity(
        user_id=request.app.state.user_subjects.require_user_id(payload["sub"]),
        subject=payload["sub"],
        roles=frozenset(Role(value) for value in payload.get("roles", [])),
    )


def require_role(*allowed: Role):
    async def dependency(identity: Identity = Depends(get_identity)) -> Identity:
        if not identity.roles.intersection(allowed):
            raise HTTPException(status_code=403, detail="role not permitted")
        return identity
    return dependency
```

Demo sessions use an HMAC-SHA256 signed payload containing only `sub`, `roles`, `iat`, and `exp`, expire after 30 minutes, use `HttpOnly`, `SameSite=Strict`, and set `Secure` whenever the request scheme is HTTPS.

- [ ] **Step 4: Remove identity fields from public request contracts**

```python
class ConsentGrantRequest(BaseModel):
    version: Literal["2026-09-01"]
    scopes: list[ConsentScope]


@router.post("/consents")
def grant_consent(
    request: ConsentGrantRequest,
    identity: Identity = Depends(require_role(Role.SPEAKER)),
    session: Session = Depends(get_session),
):
    return grant_scopes(session, identity.user_id, request.version, request.scopes, identity.user_id)
```

Apply the same rule to contribution creation, assignment answers, referee votes, wallet operations, receipts and ops routes. A route may accept an entity ID, but never a caller-selected actor ID.

- [ ] **Step 5: Run auth, consent, audio, assignment and receipt API suites**

Run: `cd starter/backend && python -m pytest tests/test_auth.py tests/test_auth_api.py tests/test_consent_api.py tests/test_audio_api.py tests/test_peer_api.py tests/test_receipt_api.py -v`

Expected: all pass; impersonation requests are rejected before service code runs.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/auth.py starter/backend/app/main.py starter/backend/app/routes/consents.py starter/backend/app/routes/audio.py starter/backend/app/routes/assignments.py starter/backend/app/routes/receipts.py starter/backend/tests/test_auth.py starter/backend/tests/test_auth_api.py
git commit -m "Auth: isolate demo sessions from production identity"
```

---

### Task 3: Honest process-local rate-limiter adapter

**Files:**
- Create: `starter/backend/app/rate_limit.py`
- Create: `starter/backend/tests/test_rate_limit.py`
- Create: `starter/backend/tests/test_rate_limit_api.py`
- Modify: `starter/backend/app/main.py`
- Modify: `starter/backend/app/routes/sessions.py`
- Modify: `starter/backend/app/routes/audio.py`
- Modify: `starter/backend/app/routes/assignments.py`
- Modify: `starter/backend/app/routes/wallet.py`
- Modify: `starter/backend/app/routes/demo.py`

**Interfaces:**
- Produces: `RateLimitDecision`, `RateLimiter`, `InMemorySlidingWindowRateLimiter`, `rate_limit(bucket, limit, window_seconds)`.
- Keys authenticated operations by `(bucket, identity.user_id)` and unauthenticated session creation by `(bucket, client_ip)`.
- Limits: demo session `10/min/IP`; audio upload `6/min/user`; assignment answer/referee `30/min/user`; cash-out `3/10min/user`; demo reset/fault controls `6/min/admin`.
- Explicit limitation: state is per process and resets when the process restarts.

- [ ] **Step 1: Write failing limiter tests with an injected clock**

```python
from app.rate_limit import InMemorySlidingWindowRateLimiter


def test_sliding_window_rejects_only_the_excess_request(fake_clock):
    limiter = InMemorySlidingWindowRateLimiter(clock=fake_clock)
    assert limiter.check("audio:user-1", limit=2, window_seconds=60).allowed
    assert limiter.check("audio:user-1", limit=2, window_seconds=60).allowed
    denied = limiter.check("audio:user-1", limit=2, window_seconds=60)
    assert denied.allowed is False
    assert denied.retry_after_seconds == 60
    fake_clock.advance(61)
    assert limiter.check("audio:user-1", limit=2, window_seconds=60).allowed


def test_keys_do_not_leak_between_users(fake_clock):
    limiter = InMemorySlidingWindowRateLimiter(clock=fake_clock)
    limiter.check("cashout:user-1", limit=1, window_seconds=600)
    assert limiter.check("cashout:user-2", limit=1, window_seconds=600).allowed
```

- [ ] **Step 2: Run tests and confirm the adapter is missing**

Run: `cd starter/backend && python -m pytest tests/test_rate_limit.py -v`

Expected: collection fails because `app.rate_limit` does not exist.

- [ ] **Step 3: Implement the protocol and process-local adapter**

```python
from collections import defaultdict, deque
from dataclasses import dataclass
from threading import Lock
from time import monotonic
from typing import Callable, Protocol


@dataclass(frozen=True)
class RateLimitDecision:
    allowed: bool
    limit: int
    remaining: int
    retry_after_seconds: int


class RateLimiter(Protocol):
    scope: str

    def check(self, key: str, limit: int, window_seconds: int) -> RateLimitDecision:
        raise NotImplementedError


class InMemorySlidingWindowRateLimiter:
    scope = "single-process"

    def __init__(self, clock: Callable[[], float] = monotonic):
        self._clock = clock
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str, limit: int, window_seconds: int) -> RateLimitDecision:
        now = self._clock()
        with self._lock:
            events = self._events[key]
            while events and events[0] <= now - window_seconds:
                events.popleft()
            if len(events) >= limit:
                retry = max(1, int(window_seconds - (now - events[0])))
                return RateLimitDecision(False, limit, 0, retry)
            events.append(now)
            return RateLimitDecision(True, limit, limit - len(events), 0)
```

The dependency returns HTTP `429` with `Retry-After`, `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Scope: single-process`.

- [ ] **Step 4: Apply exact endpoint policies and prove production rejection**

```python
@router.post("/wallet/cash-outs", dependencies=[Depends(rate_limit("cashout", 3, 600))], response_model=CashOutResponse)
def create_cash_out(
    request: CashOutRequest,
    identity: Identity = Depends(require_role(Role.SPEAKER)),
    session: Session = Depends(get_session),
) -> CashOutResponse:
    attempt = request_cash_out(
        session,
        user_id=identity.user_id,
        amount_cents=request.amount_cents,
        idempotency_key=request.idempotency_key,
    )
    return CashOutResponse.model_validate(attempt)
```

Use the same dependency shape on session, audio, assignment and demo-control routes. Extend `test_config.py` to assert production cannot start with `rate_limit_backend="memory"`; do not add a fake Redis implementation.

- [ ] **Step 5: Run focused and API tests**

Run: `cd starter/backend && python -m pytest tests/test_rate_limit.py tests/test_rate_limit_api.py tests/test_config.py -v`

Expected: all pass; the 429 response advertises `single-process` scope.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/rate_limit.py starter/backend/app/main.py starter/backend/app/routes/sessions.py starter/backend/app/routes/audio.py starter/backend/app/routes/assignments.py starter/backend/app/routes/wallet.py starter/backend/app/routes/demo.py starter/backend/tests/test_rate_limit.py starter/backend/tests/test_rate_limit_api.py starter/backend/tests/test_config.py
git commit -m "Security: add explicit single-process rate limits"
```

---

### Task 4: Log, error and receipt secret/PII sanitisation

**Files:**
- Create: `starter/backend/app/sanitise.py`
- Create: `starter/backend/app/logging.py`
- Create: `starter/backend/tests/test_sanitise.py`
- Create: `starter/backend/tests/test_logging.py`
- Modify: `starter/backend/app/main.py`
- Modify: `starter/backend/app/api_types.py`
- Modify: `starter/backend/app/routes/receipts.py`
- Modify: `starter/frontend/src/api/contracts.ts`
- Modify: `starter/frontend/src/features/receipt/ReceiptView.tsx`
- Create: `starter/frontend/src/features/receipt/ReceiptView.test.tsx`

**Interfaces:**
- Produces: `sanitise(value, *, hash_key: bytes) -> object`, `public_receipt(receipt, *, hash_key: bytes) -> ReceiptResponse`.
- Always redacts keys matching `authorization`, `cookie`, `set-cookie`, `token`, `secret`, `password`, `audio_key`, `object_key`, `signed_url`, `provider_request`, `provider_response`.
- Replaces phone/email values with stable keyed hashes such as `phone#7d8f22c2e6e1`; raw answers are logged only as length and keyed hash.
- Receipt exposes contribution ID, semantic label, two peer-result summaries, reward basis/version, consent version/scopes, provider mode, payment state, settlement currency/disclosure, Council status/version and timestamps. It excludes private storage and contact data.

- [ ] **Step 1: Write failing recursive sanitiser tests**

```python
from app.sanitise import sanitise


def test_recursive_sanitiser_removes_secrets_and_pseudonymises_pii():
    value = {
        "authorization": "Bearer abc",
        "nested": {
            "phone": "+27821234567",
            "email": "speaker@example.org",
            "object_key": "audio/private/clip.webm",
            "answer_text": "sefofane",
        },
    }
    clean = sanitise(value, hash_key=b"k" * 32)
    assert clean["authorization"] == "[REDACTED]"
    assert clean["nested"]["object_key"] == "[REDACTED]"
    assert clean["nested"]["phone"].startswith("phone#")
    assert clean["nested"]["email"].startswith("email#")
    assert clean["nested"]["answer_text"] == {"length": 8, "hash": clean["nested"]["answer_text"]["hash"]}
    rendered = repr(clean)
    for forbidden in ("abc", "+27821234567", "speaker@example.org", "clip.webm", "sefofane"):
        assert forbidden not in rendered
```

- [ ] **Step 2: Write a failing public receipt contract test**

```python
def test_receipt_response_contains_evidence_but_no_private_locator(receipt_client, completed_contribution):
    response = receipt_client.get(f"/receipts/{completed_contribution.id}")
    assert response.status_code == 200
    body = response.json()
    assert body["contribution_id"] == str(completed_contribution.id)
    assert body["peer_evidence"]["accepted_count"] == 2
    assert body["provider_mode"] == "DEMO_PROVIDER"
    assert body["payment_state"] in {"CREDITED", "SUBMITTED", "PENDING", "PAID", "FAILED"}
    forbidden = {"audio_key", "object_key", "signed_url", "phone", "email", "answer_text", "provider_response"}
    assert forbidden.isdisjoint(body.keys())
    assert forbidden.isdisjoint(response.text)
```

- [ ] **Step 3: Run tests and observe secret leakage or missing modules**

Run: `cd starter/backend && python -m pytest tests/test_sanitise.py tests/test_logging.py tests/test_receipt_api.py -v`

Expected: failures because sanitisation and the restricted receipt mapper are absent.

- [ ] **Step 4: Implement recursive sanitisation and structlog processors**

```python
import hashlib
import hmac
import re
from collections.abc import Mapping, Sequence

_SECRET_KEYS = re.compile(r"authorization|cookie|set-cookie|token|secret|password|audio_key|object_key|signed_url|provider_request|provider_response", re.I)
_PHONE_KEYS = re.compile(r"phone|msisdn", re.I)
_EMAIL_KEYS = re.compile(r"email", re.I)
_ANSWER_KEYS = re.compile(r"answer_text|raw_answer", re.I)


def _digest(prefix: str, value: str, key: bytes) -> str:
    digest = hmac.new(key, value.encode("utf-8"), hashlib.sha256).hexdigest()[:12]
    return f"{prefix}#{digest}"


def sanitise(value, *, hash_key: bytes):
    if isinstance(value, Mapping):
        result = {}
        for key, item in value.items():
            if _SECRET_KEYS.search(str(key)):
                result[key] = "[REDACTED]"
            elif _PHONE_KEYS.search(str(key)):
                result[key] = _digest("phone", str(item), hash_key)
            elif _EMAIL_KEYS.search(str(key)):
                result[key] = _digest("email", str(item).lower(), hash_key)
            elif _ANSWER_KEYS.search(str(key)):
                text = str(item)
                result[key] = {"length": len(text), "hash": _digest("answer", text, hash_key)}
            else:
                result[key] = sanitise(item, hash_key=hash_key)
        return result
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [sanitise(item, hash_key=hash_key) for item in value]
    return value
```

Configure structlog so `sanitise` runs before JSON rendering. Request logs contain `request_id`, method, route template, status, duration, authenticated user hash and provider mode, but never raw query strings or request/response bodies.

- [ ] **Step 5: Implement identical backend/frontend receipt DTOs**

```python
class ReceiptResponse(BaseModel):
    contribution_id: UUID
    semantic_label: str
    peer_evidence: PeerEvidenceResponse
    reward: RewardReceiptResponse
    consent: ConsentReceiptResponse
    provider_mode: ProviderMode
    payment_state: str
    settlement_currency: str
    currency_disclosure_text: str
    council: CouncilReceiptResponse
    created_at: datetime
```

```ts
export interface ReceiptResponse {
  contribution_id: string;
  semantic_label: string;
  peer_evidence: { accepted_count: 2; violation_count: number; decision: string };
  reward: { amount_cents: number; rule_version: string; state: string };
  consent: { version: string; active_scopes: string[] };
  provider_mode: 'DEMO_PROVIDER' | 'SANDBOX_COLLECTIONS' | 'SANDBOX_DISBURSEMENT' | 'PRODUCTION';
  payment_state: string;
  settlement_currency: string;
  currency_disclosure_text: string;
  council: { state: 'PENDING' | 'COMPLETE' | 'PARTIAL' | 'FAILED' | 'DISABLED'; version: string | null };
  created_at: string;
}
```

- [ ] **Step 6: Run backend and frontend sanitisation gates**

Run: `cd starter/backend && python -m pytest tests/test_sanitise.py tests/test_logging.py tests/test_receipt_api.py -v`

Run: `cd starter/frontend && npm test -- ReceiptView.test.tsx && npm run build`

Expected: all pass; forbidden values are absent from captured logs and rendered receipt DOM.

- [ ] **Step 7: Commit**

```bash
git add starter/backend/app/sanitise.py starter/backend/app/logging.py starter/backend/app/main.py starter/backend/app/api_types.py starter/backend/app/routes/receipts.py starter/backend/tests/test_sanitise.py starter/backend/tests/test_logging.py starter/frontend/src/api/contracts.ts starter/frontend/src/features/receipt/ReceiptView.tsx starter/frontend/src/features/receipt/ReceiptView.test.tsx
git commit -m "Privacy: sanitise logs and receipt payloads"
```

---

### Task 5: Deterministic demo seed and reset with production denial

**Files:**
- Create: `starter/backend/app/demo.py`
- Create: `starter/backend/app/routes/demo.py`
- Create: `starter/backend/tests/test_demo_seed.py`
- Create: `starter/backend/tests/test_demo_reset_api.py`
- Create: `starter/backend/scripts/demo_cycle.py`
- Modify: `starter/backend/app/main.py`
- Modify: `starter/backend/app/models.py`
- Create: `starter/backend/alembic/versions/d4e5f6a7b8c9_demo_run.py`
- Modify: `starter/backend/tests/test_migrations.py`

**Interfaces:**
- Produces: `DemoCatalogue`, `seed_demo(session, run_id) -> DemoSeedResult`, `reset_demo(session, storage, run_id) -> DemoSeedResult`.
- API: `POST /demo/seed`, `POST /demo/reset` protected by demo-admin identity, `X-Demo-Admin-Token`, demo mode and rate limit.
- Fixed namespace UUID: `UUID("75d3db52-7058-4a36-9e26-d7423f1a4d2e")`; IDs derive from `uuid5(namespace, f"{run_id}:{entity}:{name}")`.
- Reset deletes only rows and private objects tagged with the requested `demo_run_id`; it never truncates untagged records.

- [ ] **Step 1: Write failing deterministic and isolation tests**

```python
def test_seed_is_byte_stable_after_reset(db_session, private_storage):
    first = seed_demo(db_session, run_id="judge-golden")
    first_snapshot = first.model_dump(mode="json")
    reset_demo(db_session, private_storage, run_id="judge-golden")
    second = seed_demo(db_session, run_id="judge-golden")
    assert second.model_dump(mode="json") == first_snapshot


def test_reset_preserves_non_demo_records(db_session, private_storage, real_user):
    seed_demo(db_session, run_id="judge-golden")
    reset_demo(db_session, private_storage, run_id="judge-golden")
    assert db_session.get(User, real_user.id) is not None


def test_production_returns_404_for_demo_reset(client_factory, production_settings):
    response = client_factory(production_settings).post(
        "/demo/reset",
        headers={"X-Demo-Admin-Token": "demo-admin-token-32-bytes-long!!"},
    )
    assert response.status_code == 404
```

- [ ] **Step 2: Run tests and confirm seed/reset is missing**

Run: `cd starter/backend && python -m pytest tests/test_demo_seed.py tests/test_demo_reset_api.py -v`

Expected: failures because demo services and routes do not exist.

- [ ] **Step 3: Add a demo-run marker to reset-owned records**

```python
class DemoRun(Base):
    __tablename__ = "demo_runs"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    run_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    generation: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    seeded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)
```

Add nullable `demo_run_id` foreign keys with `ON DELETE CASCADE` to demo-owned mutable roots: users, campaigns, cards, contributions, outbox events and fault state. Child records already cascading from those roots must not gain redundant markers.

- [ ] **Step 4: Implement fixed catalogue and reset transaction**

```python
DEMO_NAMESPACE = UUID("75d3db52-7058-4a36-9e26-d7423f1a4d2e")


def demo_uuid(run_id: str, entity: str, name: str) -> UUID:
    return uuid5(DEMO_NAMESPACE, f"{run_id}:{entity}:{name}")


@dataclass(frozen=True)
class DemoCatalogue:
    speaker_subject: str = "demo-speaker"
    verifier_one_subject: str = "demo-verifier-1"
    verifier_two_subject: str = "demo-verifier-2"
    ops_subject: str = "demo-ops"
    campaign_name: str = "Judge Golden Path"
    reward_amount_cents: int = 200
    settlement_currency: str = "ZAR"


def reset_demo(session: Session, storage: PrivateAudioStorage, run_id: str) -> DemoSeedResult:
    run = session.scalar(select(DemoRun).where(DemoRun.run_id == run_id).with_for_update())
    if run:
        object_keys = list(session.scalars(select(AudioObject.object_key).join(Contribution).where(Contribution.demo_run_id == run.id)))
        for object_key in object_keys:
            storage.delete(object_key)
        session.delete(run)
        session.flush()
    result = seed_demo(session, run_id)
    session.commit()
    return result
```

Seed an open campaign, one isiZulu card and one Setswana card from the reviewed content files, four identities, required consent for the speaker/verifiers, and no pre-resolved contribution. The Playwright flow must create the contribution, assignments, reward, outbox event, Council outputs and receipt itself.

- [ ] **Step 5: Add authenticated demo endpoints and two-cycle CLI**

```python
@router.post("/demo/reset", response_model=DemoSeedResult)
def reset(
    request: Request,
    identity: Identity = Depends(require_role(Role.DEMO_ADMIN)),
    session: Session = Depends(get_session),
):
    settings: Settings = request.app.state.settings
    if not settings.demo_routes_enabled:
        raise HTTPException(status_code=404)
    supplied = request.headers.get("X-Demo-Admin-Token", "")
    expected = settings.demo_admin_token.get_secret_value()
    if not secrets.compare_digest(supplied, expected):
        raise HTTPException(status_code=403, detail="invalid demo admin token")
    return reset_demo(session, request.app.state.storage, "judge-golden")
```

`demo_cycle.py` calls reset, health, seed summary and receipt absence checks twice. It exits non-zero if seeded IDs differ or any previous reward/outbox/Council/receipt row survives.

- [ ] **Step 6: Run migration, reset and production-denial tests**

Run: `cd starter/backend && python -m pytest tests/test_migrations.py tests/test_demo_seed.py tests/test_demo_reset_api.py -v`

Expected: all pass against PostgreSQL 16, including upgrade → downgrade → upgrade.

- [ ] **Step 7: Commit**

```bash
git add starter/backend/app/demo.py starter/backend/app/routes/demo.py starter/backend/app/main.py starter/backend/app/models.py starter/backend/alembic/versions/d4e5f6a7b8c9_demo_run.py starter/backend/tests/test_demo_seed.py starter/backend/tests/test_demo_reset_api.py starter/backend/tests/test_migrations.py starter/backend/scripts/demo_cycle.py
git commit -m "Demo: add isolated deterministic seed and reset"
```

---

### Task 6: Demo-only failure injection and full failure drills

**Files:**
- Create: `starter/backend/app/faults.py`
- Create: `starter/backend/tests/test_faults.py`
- Create: `starter/backend/tests/test_failure_drills.py`
- Modify: `starter/backend/app/routes/demo.py`
- Modify: `starter/backend/app/storage/local.py`
- Modify: `starter/backend/app/consent.py`
- Modify: `starter/backend/app/outbox.py`
- Modify: `starter/backend/app/council.py`
- Modify: `starter/backend/app/provider.py`
- Modify: `starter/backend/app/models_runtime.py`
- Modify: `starter/frontend/src/styles/motion.css`
- Create: `starter/frontend/src/features/errors/FailureState.test.tsx`

**Interfaces:**
- Produces: `FaultName`, `FaultMode`, `FaultRegistry`, `fault_guard(name)`.
- Fault names are exactly `storage_upload`, `storage_playback_expired`, `consent_revoked`, `outbox_crash_after_claim`, `ai_all_unavailable`, `ai_one_specialist_unavailable`, `provider_unavailable`, `model_worse_than_baseline`, `motion_budget_exceeded`.
- API: `PUT /demo/faults/{fault_name}` with `{"mode":"once"|"always"|"off"}`; demo admin only.
- Fault state is scoped to `demo_run_id` and reset clears it.

- [ ] **Step 1: Write a failing registry test**

```python
def test_once_fault_fires_once_and_is_cleared(fault_registry):
    fault_registry.set("judge-golden", FaultName.STORAGE_UPLOAD, FaultMode.ONCE)
    with pytest.raises(InjectedFault):
        fault_registry.guard("judge-golden", FaultName.STORAGE_UPLOAD)
    fault_registry.guard("judge-golden", FaultName.STORAGE_UPLOAD)


def test_fault_routes_are_absent_in_production(client_factory, production_settings):
    response = client_factory(production_settings).put(
        "/demo/faults/ai_all_unavailable",
        json={"mode": "always"},
    )
    assert response.status_code == 404
```

- [ ] **Step 2: Write failing service-level drill assertions**

```python
def test_ai_failure_does_not_change_peer_reward_or_receipt(peer_resolved_case, fault_registry):
    fault_registry.set("judge-golden", FaultName.AI_ALL_UNAVAILABLE, FaultMode.ALWAYS)
    drain_outbox(peer_resolved_case.session)
    receipt = get_receipt(peer_resolved_case.session, peer_resolved_case.contribution_id)
    assert receipt.peer_evidence.accepted_count == 2
    assert receipt.reward.amount_cents == 200
    assert receipt.council.state == "FAILED"


def test_outbox_crash_retries_without_duplicate_council_outputs(peer_resolved_case, fault_registry):
    fault_registry.set("judge-golden", FaultName.OUTBOX_CRASH_AFTER_CLAIM, FaultMode.ONCE)
    with pytest.raises(InjectedFault):
        drain_outbox(peer_resolved_case.session)
    drain_outbox(peer_resolved_case.session)
    assert count_completed_outbox(peer_resolved_case.session) == 1
    assert count_council_outputs(peer_resolved_case.session) == expected_specialist_count()
```

- [ ] **Step 3: Run tests and confirm controlled failures are absent**

Run: `cd starter/backend && python -m pytest tests/test_faults.py tests/test_failure_drills.py -v`

Expected: failures because the fault registry and wrappers do not exist.

- [ ] **Step 4: Implement exact persistent fault state and guard**

```python
class FaultName(str, Enum):
    STORAGE_UPLOAD = "storage_upload"
    STORAGE_PLAYBACK_EXPIRED = "storage_playback_expired"
    CONSENT_REVOKED = "consent_revoked"
    OUTBOX_CRASH_AFTER_CLAIM = "outbox_crash_after_claim"
    AI_ALL_UNAVAILABLE = "ai_all_unavailable"
    AI_ONE_SPECIALIST_UNAVAILABLE = "ai_one_specialist_unavailable"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    MODEL_WORSE_THAN_BASELINE = "model_worse_than_baseline"
    MOTION_BUDGET_EXCEEDED = "motion_budget_exceeded"


class FaultMode(str, Enum):
    OFF = "off"
    ONCE = "once"
    ALWAYS = "always"


class InjectedFault(RuntimeError):
    pass
```

`FaultRegistry.guard` locks the row, turns `ONCE` into `OFF` before raising, commits that transition, and raises `InjectedFault(name.value)`. The registry constructor refuses to initialise unless both `environment=demo` and `fault_injection_enabled=true`.

- [ ] **Step 5: Wire every fault to required honest behaviour**

| Fault | Injection point | Required observable result |
|---|---|---|
| `storage_upload` | before local adapter writes bytes | upload returns retryable 503; no `AVAILABLE` audio and no submitted contribution |
| `storage_playback_expired` | signed playback verification | 410; authorised refresh returns a new short-lived URL |
| `consent_revoked` | immediately before assignment/playback/export check | action returns 403; audit and existing reward remain |
| `outbox_crash_after_claim` | after claim commit, before handler | lease expires/retry succeeds; one completed event and one versioned output per specialist |
| `ai_all_unavailable` | Council orchestrator | peer decision/reward/receipt complete; Council state `FAILED` |
| `ai_one_specialist_unavailable` | one deterministic specialist | other outputs complete; Council state `PARTIAL`; failed specialist retry remains idempotent |
| `provider_unavailable` | before demo-provider submission | payment attempt becomes `FAILED` or stays `PENDING` per current provider contract; never `PAID`; reservation releases where contract requires |
| `model_worse_than_baseline` | model promotion gate | active alias remains baseline; signed no-improvement evidence is displayed |
| `motion_budget_exceeded` | frontend mode endpoint/flag | `data-motion="reduced"`; static Impact SVG renders; workflow and controls remain available |

- [ ] **Step 6: Run backend and frontend failure suites**

Run: `cd starter/backend && python -m pytest tests/test_faults.py tests/test_failure_drills.py tests/test_outbox.py tests/test_council.py tests/test_provider.py -v`

Run: `cd starter/frontend && npm test -- FailureState.test.tsx && npm run build`

Expected: all pass; no drill changes peer truth, money authority, consent authority or production configuration.

- [ ] **Step 7: Commit**

```bash
git add starter/backend/app/faults.py starter/backend/app/routes/demo.py starter/backend/app/storage/local.py starter/backend/app/consent.py starter/backend/app/outbox.py starter/backend/app/council.py starter/backend/app/provider.py starter/backend/app/models_runtime.py starter/backend/tests/test_faults.py starter/backend/tests/test_failure_drills.py starter/frontend/src/styles/motion.css starter/frontend/src/features/errors/FailureState.test.tsx
git commit -m "Reliability: add demo-only failure drills"
```

---

### Task 7: Playwright full workflow and two reset cycles

**Files:**
- Modify: `starter/frontend/package.json`
- Modify: `starter/frontend/package-lock.json`
- Create: `starter/frontend/playwright.config.ts`
- Create: `starter/frontend/e2e/fixtures.ts`
- Create: `starter/frontend/e2e/golden-path.spec.ts`
- Create: `starter/frontend/e2e/failure-drills.spec.ts`
- Create: `starter/frontend/e2e/assets/isiZulu-sefofane.webm`
- Create: `starter/frontend/e2e/assets/isiZulu-sefofane.sha256`

**Interfaces:**
- Consumes: demo reset/session/fault APIs, real browser MediaRecorder upload path, private playback, two verifier accounts, resolver, reward, outbox, Council and receipt APIs.
- Produces: Playwright projects `desktop-judge`, `android-360`, `android-412`, `reduced-motion`.
- Test IDs: `consent-submit`, `record-start`, `record-stop`, `record-submit`, `assignment-answer`, `assignment-referee-no`, `receipt-open`, `receipt-peer-count`, `receipt-reward`, `receipt-council`, `provider-mode`.

- [ ] **Step 1: Add Playwright and accessibility dependencies**

```json
{
  "scripts": {
    "test": "vitest run",
    "test:e2e": "playwright test",
    "test:e2e:golden": "playwright test e2e/golden-path.spec.ts",
    "test:e2e:failures": "playwright test e2e/failure-drills.spec.ts",
    "evidence:assert": "node scripts/assert-evidence.mjs"
  },
  "devDependencies": {
    "@axe-core/playwright": "4.10.2",
    "@playwright/test": "1.55.0"
  }
}
```

Run: `cd starter/frontend && npm install`

Expected: lockfile updates and `npx playwright --version` prints `Version 1.55.0`.

- [ ] **Step 2: Write the failing full-path test with three isolated contexts**

```ts
import { test, expect } from './fixtures';

for (const cycle of [1, 2]) {
  test(`golden path reset cycle ${cycle}`, async ({ resetDemo, newDemoPage, api }) => {
    const seed = await resetDemo();
    const speaker = await newDemoPage('demo-speaker');
    const verifier1 = await newDemoPage('demo-verifier-1');
    const verifier2 = await newDemoPage('demo-verifier-2');

    await speaker.goto('/consent');
    await speaker.getByTestId('consent-record').check();
    await speaker.getByTestId('consent-playback').check();
    await speaker.getByTestId('consent-submit').click();

    await speaker.goto('/record');
    await speaker.getByTestId('record-start').click();
    await speaker.setInputFiles('[data-testid="recording-fixture"]', 'e2e/assets/isiZulu-sefofane.webm');
    await speaker.getByTestId('record-stop').click();
    await speaker.getByTestId('record-submit').click();
    const contributionId = await speaker.getByTestId('contribution-id').textContent();

    for (const verifier of [verifier1, verifier2]) {
      await verifier.goto('/verify');
      await verifier.getByTestId('assignment-answer').fill('sefofane');
      await verifier.getByTestId('assignment-lock').click();
      await verifier.getByTestId('assignment-referee-no').click();
      await verifier.getByTestId('assignment-submit').click();
    }

    await api.post('/internal/demo/drain-outbox');
    await speaker.goto(`/receipt/${contributionId}`);
    await expect(speaker.getByTestId('receipt-peer-count')).toHaveText('Confirmed by 2 verifiers');
    await expect(speaker.getByTestId('receipt-reward')).toHaveText('R2.00 credited');
    await expect(speaker.getByTestId('receipt-council')).toContainText(/Complete|Partial/);
    await expect(speaker.getByTestId('provider-mode')).toHaveText('DEMO_PROVIDER');

    const counts = await api.get(`/internal/demo/counts?run_id=${seed.run_id}`).then(r => r.json());
    expect(counts).toEqual({
      contributions: 1,
      completed_assignments: 2,
      eligibility_decisions: 1,
      rewards: 1,
      completed_outbox_events: 1,
      receipts: 1,
    });
  });
}
```

The `recording-fixture` input is compiled only in demo/test builds and feeds bytes through the same frontend upload client as MediaRecorder. It is absent when `VITE_AMAZWI_ENVIRONMENT=production`.

- [ ] **Step 3: Run and confirm the browser path fails before hardening wiring is complete**

Run: `cd starter/frontend && npx playwright install chromium && npm run test:e2e:golden`

Expected: failure at the first missing demo session, test ID, private upload, assignment or receipt integration; no test is skipped.

- [ ] **Step 4: Implement deterministic fixtures and target projects**

```ts
export default defineConfig({
  testDir: './e2e',
  use: { baseURL: 'http://127.0.0.1:4173', trace: 'retain-on-failure', video: 'retain-on-failure' },
  webServer: [
    { command: 'python -m uvicorn app.main:app --host 127.0.0.1 --port 8000', cwd: '../backend', url: 'http://127.0.0.1:8000/health', reuseExistingServer: false },
    { command: 'npm run dev -- --host 127.0.0.1 --port 4173', cwd: '.', url: 'http://127.0.0.1:4173', reuseExistingServer: false },
  ],
  projects: [
    { name: 'desktop-judge', use: { viewport: { width: 1280, height: 800 } } },
    { name: 'android-360', use: { browserName: 'chromium', userAgent: devices['Galaxy S9+'].userAgent, deviceScaleFactor: 3, isMobile: true, hasTouch: true, viewport: { width: 360, height: 800 } } },
    { name: 'android-412', use: { browserName: 'chromium', userAgent: devices['Pixel 5'].userAgent, deviceScaleFactor: 2.625, isMobile: true, hasTouch: true, viewport: { width: 412, height: 915 } } },
    { name: 'reduced-motion', use: { viewport: { width: 390, height: 844 }, reducedMotion: 'reduce' } },
  ],
});
```

Use separate browser contexts, session cookies and users for speaker and each verifier. Never reuse one authenticated page to impersonate all three roles.

- [ ] **Step 5: Add browser-visible failure drill tests**

```ts
const drills = [
  ['storage_upload', 'Recording was not submitted. Try again.'],
  ['consent_revoked', 'Consent changed. This audio is no longer available.'],
  ['outbox_crash_after_claim', 'Peer decision complete. Advisory insight is pending.'],
  ['ai_all_unavailable', 'Peer decision complete. Advisory insight is unavailable.'],
  ['provider_unavailable', 'Reward credited. Transfer not completed.'],
  ['model_worse_than_baseline', 'Baseline remains active. No improvement claimed.'],
  ['motion_budget_exceeded', 'Reduced visual mode'],
] as const;

for (const [fault, message] of drills) {
  test(`${fault} is honest and recoverable`, async ({ setFault, runToRelevantStep, page }) => {
    await setFault(fault, 'once');
    await runToRelevantStep(fault, page);
    await expect(page.getByText(message)).toBeVisible();
    await expect(page.getByRole('button', { name: /retry|continue|refresh/i })).toBeEnabled();
  });
}
```

- [ ] **Step 6: Run golden path twice and all browser drills**

Run: `cd starter/frontend && npm run test:e2e:golden -- --project=desktop-judge && npm run test:e2e:failures -- --project=android-360`

Expected: both reset cycles and every drill pass; Playwright report has zero skipped tests.

- [ ] **Step 7: Commit**

```bash
git add starter/frontend/package.json starter/frontend/package-lock.json starter/frontend/playwright.config.ts starter/frontend/e2e/fixtures.ts starter/frontend/e2e/golden-path.spec.ts starter/frontend/e2e/failure-drills.spec.ts starter/frontend/e2e/assets/isiZulu-sefofane.webm starter/frontend/e2e/assets/isiZulu-sefofane.sha256
git commit -m "Test: prove the full three-device governed workflow"
```

---

### Task 8: Target-device, accessibility and performance evidence

**Files:**
- Create: `starter/frontend/e2e/accessibility-performance.spec.ts`
- Create: `starter/frontend/scripts/assert-evidence.mjs`
- Create: `starter/frontend/public/fallback/impact-static.svg`
- Modify: `starter/frontend/src/features/impact/CoverageConstellation.tsx`
- Modify: `starter/frontend/src/styles/motion.css`
- Create: `starter/evidence/stage-09/accessibility.json`
- Create: `starter/evidence/stage-09/performance.json`
- Create: `starter/evidence/stage-09/screenshots/.gitkeep`

**Interfaces:**
- Accessibility acceptance: zero axe violations with impact `critical` or `serious`; complete keyboard path; visible focus; 44×44 CSS-pixel minimum primary controls; 200% zoom with no horizontal document overflow at 320, 360, 390, 412 and 480 CSS px; reduced-motion state has no infinite non-essential animation.
- Performance acceptance on `android-360` with Chromium CPU throttling rate 4 and network `Fast 3G`: LCP ≤ 3,500 ms, CLS ≤ 0.10, INP proxy longest interaction task ≤ 200 ms, no animation frame task > 50 ms during the receipt transition, initial JS gzip ≤ 250 KiB, lazy Impact chunk gzip ≤ 60 KiB.
- Evidence JSON records observed values, browser version, commit SHA, viewport, throttling and timestamp. A failed budget remains a failed artefact; do not rewrite it as a pass.

- [ ] **Step 1: Write failing accessibility and evidence assertions**

```ts
test('golden path passes axe, keyboard, zoom and reduced motion', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations.filter(v => ['critical', 'serious'].includes(v.impact ?? ''))).toEqual([]);

  await page.keyboard.press('Tab');
  await expect(page.getByRole('button', { name: /start|continue/i })).toBeFocused();

  await page.evaluate(() => { document.documentElement.style.zoom = '2'; });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1);
});
```

```js
const accessibility = JSON.parse(readFileSync('starter/evidence/stage-09/accessibility.json', 'utf8'));
if (accessibility.serious_or_critical_violations !== 0) process.exit(1);
if (!accessibility.keyboard_complete || !accessibility.zoom_200_percent_pass) process.exit(1);
```

- [ ] **Step 2: Run and capture current failures before optimising**

Run: `cd starter/frontend && npm run test:e2e -- e2e/accessibility-performance.spec.ts --project=android-360`

Expected: the test writes measured failures for any missing focus, small target, overflow, motion or performance budget; it does not suppress them.

- [ ] **Step 3: Add target checks and CDP throttling**

```ts
const session = await page.context().newCDPSession(page);
await session.send('Emulation.setCPUThrottlingRate', { rate: 4 });
await session.send('Network.emulateNetworkConditions', {
  offline: false,
  latency: 150,
  downloadThroughput: 1_600_000 / 8,
  uploadThroughput: 750_000 / 8,
  connectionType: 'cellular3g',
});
```

Measure Web Vitals with `PerformanceObserver`, collect long tasks, inspect every primary button bounding box, run axe on consent, recording, verifier, receipt and Impact routes, and take screenshots at 320, 360, 390, 412 and 480 CSS px in Midnight and Daylight themes.

- [ ] **Step 4: Implement motion fallback and budget enforcement**

```tsx
export function CoverageConstellation({ motionBudgetPassed }: { motionBudgetPassed: boolean }) {
  const reduced = useReducedMotion();
  if (reduced || !motionBudgetPassed) {
    return <img src="/fallback/impact-static.svg" alt="Aggregate language coverage by province" data-testid="impact-static" />;
  }
  return <LazyConstellation data-testid="impact-motion" />;
}
```

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 80ms !important;
  }
}
```

Cut or simplify effects until budgets pass. Do not raise thresholds after observing results.

- [ ] **Step 5: Generate and assert evidence**

Run: `cd starter/frontend && npm run test:e2e -- e2e/accessibility-performance.spec.ts`

Run: `node starter/frontend/scripts/assert-evidence.mjs`

Expected: all accessibility and performance budgets pass on generated evidence; screenshots come from the running app and contain no secrets or PII.

- [ ] **Step 6: Commit**

```bash
git add starter/frontend/e2e/accessibility-performance.spec.ts starter/frontend/scripts/assert-evidence.mjs starter/frontend/public/fallback/impact-static.svg starter/frontend/src/features/impact/CoverageConstellation.tsx starter/frontend/src/styles/motion.css starter/evidence/stage-09/accessibility.json starter/evidence/stage-09/performance.json starter/evidence/stage-09/screenshots/.gitkeep
git commit -m "Evidence: verify mobile accessibility and performance"
```

---

### Task 9: Honest fallback artefacts and recovery card

**Files:**
- Create: `starter/scripts/capture-fallback.ps1`
- Create: `starter/evidence/stage-09/fallback/RECOVERY_CARD.md`
- Create: `starter/evidence/stage-09/fallback/SHA256SUMS.txt`
- Create: `starter/evidence/stage-09/fallback/amazwi-golden-path.mp4`
- Create: `starter/evidence/stage-09/fallback/amazwi-golden-path.webm`
- Modify: `05_amazwi/plan/15_DEMO_SCRIPT.md`

**Interfaces:**
- Consumes: a passing Playwright golden path on the integrated local app.
- Produces: 1080p MP4 and WebM captures of the same real run, each under 90 seconds, with visible `DEMO_PROVIDER` and browser/demo-mode labels.
- Recovery copies are exactly those already approved in `05_amazwi/plan/15_DEMO_SCRIPT.md`; no new payment or deployment claim is introduced.

- [ ] **Step 1: Write the artefact validation before capturing**

```powershell
$ErrorActionPreference = 'Stop'
$files = @(
  'starter/evidence/stage-09/fallback/amazwi-golden-path.mp4',
  'starter/evidence/stage-09/fallback/amazwi-golden-path.webm'
)
foreach ($file in $files) {
  if (-not (Test-Path $file)) { throw "Missing fallback artefact: $file" }
  if ((Get-Item $file).Length -lt 100000) { throw "Fallback artefact is implausibly small: $file" }
}
$duration = [double](& ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 $files[0])
if ($duration -gt 90) { throw "Fallback video exceeds 90 seconds: $duration" }
```

- [ ] **Step 2: Run validation and confirm artefacts do not yet pass**

Run: `powershell -ExecutionPolicy Bypass -File starter/scripts/capture-fallback.ps1 -ValidateOnly`

Expected: fails because the real fallback captures do not exist yet.

- [ ] **Step 3: Implement non-interactive capture from the running golden path**

`capture-fallback.ps1` must:

1. run `starter/scripts/run-stage-09.ps1 -GoldenPathOnly`;
2. select Playwright’s successful golden-path WebM recording;
3. set `$source = Get-ChildItem 'starter/frontend/test-results' -Filter 'video.webm' -Recurse | Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1`, fail if `$source` is null, then run `ffmpeg -y -i "$($source.FullName)" -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -pix_fmt yuv420p -movflags +faststart starter/evidence/stage-09/fallback/amazwi-golden-path.mp4`;
4. copy the source to `amazwi-golden-path.webm`;
5. calculate SHA-256 hashes with `Get-FileHash -Algorithm SHA256`;
6. run the validation block from Step 1.

No screen may show a token, raw phone/email, signed audio URL, object key or terminal containing secrets.

- [ ] **Step 4: Write the exact recovery card**

```markdown
# AMAZWI Offline Recovery Card

1. Say: “We are switching to a recording of the same tested local golden path.”
2. Play `amazwi-golden-path.mp4` from the local device.
3. At the reward state say: “This is our labelled demo provider. The state machine and idempotency are real; the rand amount is not a production transfer.”
4. At the Council state say: “The two peers made the authoritative decision. The Council runs afterward and cannot change eligibility or money.”
5. At the receipt say: “One screen proves what was contributed, why it qualified, what it earned, what the person consented to and where the value is now.”
6. Do not claim a deployment, live MoMo settlement, production storage provider, production authentication provider or promoted model that the evidence does not prove.
```

- [ ] **Step 5: Capture, validate and update the demo script status honestly**

Run: `powershell -ExecutionPolicy Bypass -File starter/scripts/capture-fallback.ps1`

Expected: both videos validate, hashes are written, and `15_DEMO_SCRIPT.md` names the exact artefact paths and capture commit. Replace only the old “not producible yet” status paragraph; retain the historical explanation that static mockups were not acceptable evidence.

- [ ] **Step 6: Commit**

```bash
git add starter/scripts/capture-fallback.ps1 starter/evidence/stage-09/fallback/RECOVERY_CARD.md starter/evidence/stage-09/fallback/SHA256SUMS.txt starter/evidence/stage-09/fallback/amazwi-golden-path.mp4 starter/evidence/stage-09/fallback/amazwi-golden-path.webm 05_amazwi/plan/15_DEMO_SCRIPT.md
git commit -m "Demo: capture the real offline golden-path fallback"
```

---

### Task 10: Stage 9 orchestration and evidence manifest

**Files:**
- Create: `starter/scripts/run-stage-09.ps1`
- Create: `starter/evidence/stage-09/README.md`
- Create: `starter/evidence/stage-09/manifest.json`
- Create: `starter/evidence/stage-09/failure-matrix.json`
- Create: `starter/backend/tests/test_stage09_manifest.py`

**Interfaces:**
- Produces one non-interactive Windows command for local acceptance.
- Manifest schema: `commit_sha`, `generated_at`, `environment`, `provider_mode`, `rate_limit_scope`, `reset_cycles`, `golden_path`, `failure_drills`, `accessibility`, `performance`, `fallback_hashes`, `deployment_resumed`, `pending_sbu_review`.
- Required fixed values: `environment="demo"`, `provider_mode="DEMO_PROVIDER"`, `rate_limit_scope="single-process"`, `reset_cycles=2`, `deployment_resumed=false`, `pending_sbu_review=true`.

- [ ] **Step 1: Write a failing manifest contract test**

```python
import json
from pathlib import Path


def test_stage09_manifest_is_complete_and_honest():
    manifest = json.loads(Path("../evidence/stage-09/manifest.json").read_text())
    assert manifest["environment"] == "demo"
    assert manifest["provider_mode"] == "DEMO_PROVIDER"
    assert manifest["rate_limit_scope"] == "single-process"
    assert manifest["reset_cycles"] == 2
    assert manifest["golden_path"]["passed"] is True
    assert set(manifest["failure_drills"]) == {
        "storage_upload", "storage_playback_expired", "consent_revoked",
        "outbox_crash_after_claim", "ai_all_unavailable",
        "ai_one_specialist_unavailable", "provider_unavailable",
        "model_worse_than_baseline", "motion_budget_exceeded",
    }
    assert manifest["deployment_resumed"] is False
    assert manifest["pending_sbu_review"] is True
```

- [ ] **Step 2: Run and confirm the manifest is absent**

Run: `cd starter/backend && python -m pytest tests/test_stage09_manifest.py -v`

Expected: failure because `manifest.json` does not exist.

- [ ] **Step 3: Implement the exact orchestration sequence**

```powershell
$ErrorActionPreference = 'Stop'
$env:AMAZWI_ENVIRONMENT = 'demo'
$env:AMAZWI_AUTH_MODE = 'demo'
$env:AMAZWI_DEMO_ROUTES_ENABLED = 'true'
$env:AMAZWI_FAULT_INJECTION_ENABLED = 'true'
$env:AMAZWI_PROVIDER_MODE = 'DEMO_PROVIDER'
$env:AMAZWI_RATE_LIMIT_BACKEND = 'memory'
$env:AMAZWI_CORS_ORIGINS = '["http://127.0.0.1:4173"]'

Push-Location starter/backend
python -m pytest -v
python -m app.scripts.demo_cycle --cycles 2
Pop-Location

Push-Location starter/frontend
npm ci
npm test
npm run build
npx playwright install chromium
npm run test:e2e:golden -- --project=desktop-judge
npm run test:e2e:failures -- --project=android-360
npm run test:e2e -- e2e/accessibility-performance.spec.ts
npm run evidence:assert
Pop-Location

python starter/backend/scripts/build_stage09_manifest.py
python -m pytest starter/backend/tests/test_stage09_manifest.py -v
```

The script accepts secrets only through pre-existing environment variables, never echoes them, and refuses to run if `AMAZWI_ENVIRONMENT=production`. It contains no `vercel`, `az`, `aws`, `gcloud`, `docker push`, remote migration or deployment command.

- [ ] **Step 4: Generate drill and manifest JSON from test outputs**

```json
{
  "environment": "demo",
  "provider_mode": "DEMO_PROVIDER",
  "rate_limit_scope": "single-process",
  "reset_cycles": 2,
  "golden_path": { "passed": true, "browser_contexts": 3 },
  "failure_drills": {
    "storage_upload": "passed",
    "storage_playback_expired": "passed",
    "consent_revoked": "passed",
    "outbox_crash_after_claim": "passed",
    "ai_all_unavailable": "passed",
    "ai_one_specialist_unavailable": "passed",
    "provider_unavailable": "passed",
    "model_worse_than_baseline": "passed",
    "motion_budget_exceeded": "passed"
  },
  "deployment_resumed": false,
  "pending_sbu_review": true
}
```

The generator fills commit SHA, timestamps, observed metrics and hashes from actual command outputs. It must never set `passed=true` when an input report is missing.

- [ ] **Step 5: Run the complete local gate twice**

Run: `powershell -ExecutionPolicy Bypass -File starter/scripts/run-stage-09.ps1`

Run again: `powershell -ExecutionPolicy Bypass -File starter/scripts/run-stage-09.ps1`

Expected: both invocations exit `0`; each invocation internally proves two reset cycles; manifest hashes and deterministic seeded IDs match where expected, while timestamps and trace IDs may differ.

- [ ] **Step 6: Commit**

```bash
git add starter/scripts/run-stage-09.ps1 starter/evidence/stage-09/README.md starter/evidence/stage-09/manifest.json starter/evidence/stage-09/failure-matrix.json starter/backend/tests/test_stage09_manifest.py starter/backend/scripts/build_stage09_manifest.py
git commit -m "Demo: automate Stage 9 acceptance evidence"
```

---

### Task 11: Expand CI without deployment

**Files:**
- Modify: `.github/workflows/ci.yml`
- Create: `starter/scripts/scan-secrets.py`
- Create: `starter/backend/tests/test_no_production_demo_routes.py`

**Interfaces:**
- CI jobs: `backend`, `frontend`, `e2e`, `evidence`, `secret-scan`.
- CI uses PostgreSQL 16 and `DEMO_PROVIDER`; it performs no external provider call and no deployment.
- Uploads Playwright reports and Stage 9 JSON only on failure or from sanitised generated artefacts; raw private storage is never uploaded.

- [ ] **Step 1: Write failing route and secret-scan tests**

```python
def test_production_openapi_contains_no_demo_paths(client_factory, production_settings):
    paths = client_factory(production_settings).get("/openapi.json").json()["paths"]
    assert not any(path.startswith("/demo/") or path == "/sessions/demo" for path in paths)
```

```python
FORBIDDEN_PATTERNS = {
    "bearer": re.compile(r"Bearer\s+[A-Za-z0-9._~-]{20,}"),
    "signed_url": re.compile(r"https?://[^\s]+(?:signature|sig|token)=[^\s]+", re.I),
    "sa_phone": re.compile(r"(?:\+27|0)[6-8][0-9]{8}"),
    "private_object": re.compile(r"audio/private/[A-Za-z0-9._/-]+"),
}
```

- [ ] **Step 2: Run the checks and establish the current failure**

Run: `cd starter/backend && python -m pytest tests/test_no_production_demo_routes.py -v`

Run: `python starter/scripts/scan-secrets.py starter/evidence starter/frontend/playwright-report`

Expected: route test fails until demo routers are conditionally registered; scanner exits non-zero for any seeded forbidden fixture intentionally placed in its unit test.

- [ ] **Step 3: Expand CI with exact jobs**

```yaml
  e2e:
    runs-on: ubuntu-latest
    needs: [backend, frontend]
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: amazwi_test
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 5s
          --health-timeout 5s
          --health-retries 10
    env:
      AMAZWI_TEST_DATABASE_URL: postgresql://postgres:postgres@localhost:5432/amazwi_test
      AMAZWI_DATABASE_URL: postgresql://postgres:postgres@localhost:5432/amazwi_test
      AMAZWI_ENVIRONMENT: demo
      AMAZWI_AUTH_MODE: demo
      AMAZWI_DEMO_ROUTES_ENABLED: "true"
      AMAZWI_FAULT_INJECTION_ENABLED: "true"
      AMAZWI_PROVIDER_MODE: DEMO_PROVIDER
      AMAZWI_RATE_LIMIT_BACKEND: memory
      AMAZWI_DEMO_ADMIN_TOKEN: ci-demo-admin-token-32-characters-minimum
      AMAZWI_RECEIPT_HASH_KEY: ci-receipt-hash-key-32-characters-minimum
      AMAZWI_LOG_HASH_KEY: ci-log-hash-key-32-characters-minimum-value
      AMAZWI_CORS_ORIGINS: '["http://127.0.0.1:4173"]'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - uses: actions/setup-node@v4
        with: { node-version: "20", cache: npm, cache-dependency-path: starter/frontend/package-lock.json }
      - run: pip install -r starter/backend/requirements.txt
      - run: npm ci
        working-directory: starter/frontend
      - run: npx playwright install --with-deps chromium
        working-directory: starter/frontend
      - run: npm run test:e2e:golden -- --project=desktop-judge
        working-directory: starter/frontend
      - run: npm run test:e2e:failures -- --project=android-360
        working-directory: starter/frontend
```

Add `evidence` to run accessibility/performance assertions and `secret-scan` to scan generated logs, JSON, screenshots metadata and Playwright report HTML. Do not add any deployment job or environment.

- [ ] **Step 4: Validate workflow syntax and all CI-equivalent commands locally**

Run: `python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml', encoding='utf-8')); print('workflow yaml ok')"`

Run: `powershell -ExecutionPolicy Bypass -File starter/scripts/run-stage-09.ps1`

Run: `python starter/scripts/scan-secrets.py starter/evidence starter/frontend/playwright-report`

Expected: YAML parses, Stage 9 passes, secret scan reports zero findings, and no deployment command appears in the workflow.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/ci.yml starter/scripts/scan-secrets.py starter/backend/tests/test_no_production_demo_routes.py
git commit -m "CI: gate hardening browser evidence and secret safety"
```

---

### Task 12: Documentation, honesty ledger and Sbu review handoff

**Files:**
- Modify: `starter/evidence/stage-09/README.md`
- Modify: `05_amazwi/BUILD_LOG.md`
- Modify: `HANDOVER_SBU.md`
- Modify: `05_amazwi/P0.md`
- Modify: `05_amazwi/plan/07_TRUTH.md`
- Create: `starter/evidence/stage-09/HONESTY_LEDGER.md`

**Interfaces:**
- Produces a claim-to-evidence ledger with statuses `PROVED`, `DEMO_ONLY`, `NOT_PROVED`, `PENDING_SBU_REVIEW`.
- Records no deployment resume and no production-safety claim for the in-memory limiter.
- Requests Sbu review for auth, consent, storage, outbox, provider/money, logs, CI and production guards.

- [ ] **Step 1: Write the exact honesty ledger before changing status documents**

```markdown
# AMAZWI Stage 9 Honesty Ledger

| Claim | Status | Evidence | Exact limitation |
|---|---|---|---|
| Three browser identities complete the governed path | PROVED | `manifest.json`, Playwright report | Local demo environment with deterministic identities |
| Audio is private and assignment-bound | PROVED | private-storage API tests and golden-path trace | Local private adapter, not a selected production object-store provider |
| Two proficient peers are authoritative | PROVED | resolver tests and receipt evidence | Demo cohort and reviewed hero cards |
| Reward is idempotent | PROVED | PostgreSQL tests and two reset cycles | Credited ledger event through `DEMO_PROVIDER`; not production settlement |
| Council is recoverable and advisory | PROVED | outbox/AI drills | Deterministic/local specialists unless a separately evidenced provider is configured |
| Rate limiting protects this demo process | DEMO_ONLY | rate-limit tests and `X-RateLimit-Scope` | In-memory, per-process, not distributed or multi-node safe |
| Production configuration fails closed | PROVED | config/auth/OpenAPI tests | Configuration proof only; no production deployment was attempted |
| Deterministic reset is unavailable in production | PROVED | production OpenAPI and route tests | Demo/test control only |
| Target mobile accessibility and budgets pass | PROVED | `accessibility.json`, `performance.json` | Chromium profiles plus named physical-device evidence; not every handset |
| MoMo money was transferred in production | NOT_PROVED | none | `DEMO_PROVIDER` is visibly labelled; no production transfer claim |
| Vercel or another production deployment is ready | NOT_PROVED | none | Deployment remains paused and was not resumed |
| Platform/money/deployment boundaries have Sbu approval | PENDING_SBU_REVIEW | `HANDOVER_SBU.md` | Implementation evidence is not teammate sign-off |
```

- [ ] **Step 2: Append a full build-log entry without rewriting history**

Use the repository’s DID/HOW/WHY/CHANGED/NEXT/BLOCKED-PING format. Include:

```markdown
**BLOCKED/PING:** Cross-lane Stage 9 platform, auth, privacy, provider, CI and production-boundary work remains pending Sbu review. The in-memory limiter is single-process only. `DEMO_PROVIDER` is not a production transfer. Deterministic reset/fault routes are absent in production configuration. Vercel deployment remains paused and no deployment command was run.
```

List exact commands and observed pass counts from the completed implementation, not planned numbers.

- [ ] **Step 3: Update P0 and the truth register conservatively**

`P0.md` may mark Gate H complete only if the final local gate, both reset cycles, physical-device checks and fallback copies on both laptops and a phone are evidenced. Otherwise record the precise remaining item and leave Gate H open.

Add these prohibited claims to `07_TRUTH.md`:

```markdown
- Do not call the process-local in-memory limiter distributed, multi-node or production-safe.
- Do not call `DEMO_PROVIDER` a live MoMo transfer.
- Do not call local private storage a selected production storage provider.
- Do not call configuration hardening a production deployment.
- Do not call deterministic Council baselines a promoted production model.
- Do not call browser emulation physical-device evidence.
```

- [ ] **Step 4: Write the exact Sbu handoff request**

```markdown
## Stage 9 cross-lane review request

Please review these boundaries before they are treated as final in your lane:
1. production configuration rejects demo auth/provider/reset/faults, wildcard CORS and in-memory rate limiting;
2. route identity is server-derived and body impersonation is rejected;
3. consent/storage/outbox/provider failure drills preserve authority and financial invariants;
4. receipt and logs redact secrets, private object locators and direct PII;
5. deterministic reset deletes only tagged demo data and is absent from production OpenAPI;
6. CI uses PostgreSQL 16 and `DEMO_PROVIDER`, uploads no private audio, and contains no deployment job.

Evidence: `starter/evidence/stage-09/README.md` and `manifest.json`.
Status: tested cross-lane implementation, pending your review, not your recorded sign-off.
Deployment: still paused; this work did not resume it.
```

- [ ] **Step 5: Run documentation and evidence consistency checks**

Run: `python starter/scripts/scan-secrets.py starter/evidence 05_amazwi/BUILD_LOG.md HANDOVER_SBU.md 05_amazwi/P0.md 05_amazwi/plan/07_TRUTH.md`

Run: `python -m pytest starter/backend/tests/test_stage09_manifest.py -v`

Run: `git grep -n -E "distributed rate limit|production-safe rate limit|live MoMo transfer|deployment complete" -- starter/evidence 05_amazwi/BUILD_LOG.md HANDOVER_SBU.md 05_amazwi/P0.md 05_amazwi/plan/07_TRUTH.md`

Expected: secret scan and manifest test pass; grep returns no unsupported claim. Legitimate negated warnings must use the exact wording from the honesty ledger so reviewers can distinguish them from claims.

- [ ] **Step 6: Commit**

```bash
git add starter/evidence/stage-09/README.md starter/evidence/stage-09/HONESTY_LEDGER.md 05_amazwi/BUILD_LOG.md HANDOVER_SBU.md 05_amazwi/P0.md 05_amazwi/plan/07_TRUTH.md
git commit -m "Docs: record Stage 9 evidence and review boundaries"
```

---

## Final Acceptance Gate

- [ ] `cd starter/backend && python -m pytest -v` passes against PostgreSQL 16.
- [ ] `cd starter/frontend && npm test && npm run build` passes.
- [ ] `cd starter/frontend && npm run test:e2e:golden -- --project=desktop-judge` passes both reset cycles with three independent browser contexts.
- [ ] `cd starter/frontend && npm run test:e2e:failures -- --project=android-360` passes storage, consent, outbox, AI, provider, model and motion drills.
- [ ] `cd starter/frontend && npm run test:e2e -- e2e/accessibility-performance.spec.ts` passes all viewport, zoom, keyboard, axe, reduced-motion and declared performance budgets.
- [ ] `powershell -ExecutionPolicy Bypass -File starter/scripts/run-stage-09.ps1` exits `0` twice consecutively.
- [ ] Physical low/mid-range Android evidence records device model, Android version, browser version, viewport, network, screenshots and observed performance. Emulator evidence is labelled separately.
- [ ] `starter/evidence/stage-09/fallback/amazwi-golden-path.mp4` and `.webm` are copied to both laptops and one phone, and hashes match `SHA256SUMS.txt`.
- [ ] `python starter/scripts/scan-secrets.py starter/evidence starter/frontend/playwright-report` reports zero findings.
- [ ] Production OpenAPI exposes no `/demo/*` or `/sessions/demo` paths.
- [ ] The evidence manifest says `rate_limit_scope="single-process"`, `provider_mode="DEMO_PROVIDER"`, `deployment_resumed=false`, and `pending_sbu_review=true`.
- [ ] No Vercel, cloud, remote migration, provider sandbox or production deployment command is run.
- [ ] Sbu’s review remains pending until he records acceptance, rejection or requested changes himself.
