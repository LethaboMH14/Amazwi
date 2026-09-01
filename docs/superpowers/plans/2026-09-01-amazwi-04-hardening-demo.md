# AMAZWI Hardening and Demonstration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete Stage 9 with typed runtime boundaries, local-demo-only security adapters and controls, secret-safe observability, deterministic recovery, full failure drills, two repeatable browser demonstrations, target-device evidence, expanded CI, and honest fallback/documentation artefacts without deploying anything.

**Architecture:** Keep the existing FastAPI, PostgreSQL, private object storage, transactional outbox, Council, provider, model, and Signal Flow boundaries. Add typed configuration and dependency-injected auth, rate-limit, logging, clock, randomness, and failure-control interfaces so test/demo behavior is deterministic while production mode rejects local-only implementations. Drive the complete workflow through Playwright with three browser identities, collect allowlisted evidence, and make every production, target-device, parity, payment, model, and deployment claim evidence-gated.

**Tech Stack:** Python 3.11+, FastAPI, Pydantic 2, pydantic-settings 2.10.1, SQLAlchemy 2, PostgreSQL 16, pytest, React 18, TypeScript 5.5, Vite 5, Vitest 2, Playwright 1.55, axe-core 4.10, Chromium, CSS/WAAPI, GitHub Actions, Android Debug Bridge.

## Global Constraints

- All constraints in `2026-09-01-amazwi-governed-intelligence-program.md` apply.
- Execute this plan only after plans 01–03 provide the integrated local browser, API, private storage, peer, reward, outbox, Council, receipt, impact, and ops workflow.
- The paused Vercel deployment remains paused. Do not create or modify Vercel configuration, run a Vercel command, deploy a preview, deploy production, or resume the project.
- No real payment, provider call, campaign launch, external AI call, external model run, dataset download, Figma mutation, or production data access occurs in this plan.
- Runtime modes are exactly `test`, `demo`, and `production`. Development work uses `test` or `demo`; production mode is exercised only by configuration and startup-rejection tests.
- Demo header authentication, the in-memory rate limiter, deterministic seeds, reset routes, outbox drain routes, failure injection, fake audio, fake providers, and fake Council specialists are prohibited in production.
- The in-memory limiter is per-process, loses state on restart, does not coordinate multiple workers, and is not a DDoS control. Documentation must say this verbatim wherever the limiter is described.
- Production startup must fail closed unless an externally supplied authenticator and distributed rate limiter are injected. This plan does not select or claim a production identity or rate-limit provider.
- Application logs never contain request/response bodies, raw headers, query strings, consent text, transcripts, audio bytes, object keys, signed URLs, tokens, passwords, secrets, email addresses, phone numbers, display names, exact user IDs, or exception messages that may include those values.
- Audit records remain authoritative and separate from operational logs. Log redaction never deletes required database audit evidence.
- Reset is allowed only when the database name ends in `_test` or `_demo`, the private-storage root contains an `.amazwi-demo-root` sentinel, and a configured demo token matches with constant-time comparison.
- Failure drills must cover storage, consent, outbox, AI specialist, payment provider, model evaluation, and reduced motion. Each drill proves the required safe state, not merely that an error appeared.
- Full E2E means browser → API → private storage → peer one → peer two → resolver → reward → outbox → Council → receipt. API-only setup may create the deterministic demo baseline, but recording, playback, both peer answers, and receipt observation must occur through browsers.
- Accessibility acceptance repeats 320, 360, 390, 430, and 480px widths, 200% text sizing, keyboard, accessible names/status, both first-class themes, and reduced motion.
- A physical target-device pass requires one attached Android 12–15 device with 3–6 GiB RAM and current Chrome. Emulation is supporting evidence only and never substitutes for the physical pass.
- Stage 9 exit requires two clean reset-and-demo cycles with identical canonical seed and receipt hashes, one physical target-device pass, all automated gates green, and an honesty review. If any is unavailable, record the exact blocked state and do not declare Stage 9 complete.
- TDD is mandatory. Every task begins with a failing test, reaches green, runs its relevant broader suite, and ends in a focused commit.

---

## Locked File Structure

### Backend

- `starter/backend/app/config.py`: typed settings, secret values, validation, and runtime-mode invariants.
- `starter/backend/app/auth.py`: principal contract, authenticator protocol, demo-header implementation, and fail-closed production factory.
- `starter/backend/app/rate_limit.py`: limiter protocol, policies, per-process sliding-window implementation, and FastAPI dependency.
- `starter/backend/app/safe_logging.py`: allowlisted JSON events, recursive redaction, correlation IDs, and request middleware.
- `starter/backend/app/runtime.py`: injectable clock, random source, and runtime dependencies.
- `starter/backend/app/demo.py`: deterministic reset, seed, state digest, outbox drain, and safe evidence projection.
- `starter/backend/app/failures.py`: failure-point enum, no-op production injector, and scripted test/demo injector.
- `starter/backend/app/routes/demo.py`: demo-only reset, state, drain, and failure-control routes.
- `starter/backend/app/main.py`: app factory and adapter injection only; no local-only route registration in production.
- `starter/backend/tests/test_config.py`, `test_auth.py`, `test_rate_limit.py`, `test_safe_logging.py`, `test_demo_reset.py`, `test_failure_drills.py`: focused hardening tests.

### Frontend and browser evidence

- `starter/frontend/src/config.ts`: typed Vite runtime mode and demo-control boundary.
- `starter/frontend/src/config.test.ts`: production/demo parsing tests.
- `starter/frontend/playwright.config.ts`: local web servers, fake microphone, browser projects, traces, and safe output paths.
- `starter/frontend/e2e/full-governed-demo.spec.ts`: three-context complete workflow.
- `starter/frontend/e2e/failure-drills.spec.ts`: human-visible storage, consent, Council, provider, model, and reduced-motion behavior.
- `starter/frontend/e2e/performance.spec.ts`: Web Vitals, bundle, animation, and reduced-motion budgets.
- `starter/frontend/fixtures/demo-audio.wav`: synthetic spoken-tone fixture with no human voice or personal data.
- `starter/frontend/scripts/measure-bundle.mjs`: deterministic gzip budget check.
- `starter/frontend/scripts/profile-android.mjs`: physical-device class validation and trace capture.
- `starter/frontend/scripts/capture-fallback.mjs`: allowlisted fallback capture.
- `starter/frontend/scripts/verify-fallback.mjs`: hash and forbidden-content verification.

### Cross-project verification and evidence

- `starter/scripts/wait_http.py`: bounded service readiness check.
- `starter/scripts/run_stage9.py`: one non-interactive local verification entry point.
- `starter/scripts/check_evidence_claims.py`: evidence-to-document claim gate.
- `starter/demo/fallback/manifest.json`: hashes and labels for local recorded-demo artefacts.
- `starter/demo/fallback/receipt.json`, `council-disabled.json`, `model-no-improvement.json`: safe synthetic fallback states.
- `starter/demo/fallback/screenshots/*.png`: allowlisted local demo screens without audio or personal data.
- `starter/evidence/stage9/*.json`: generated command, cycle, browser, performance, accessibility, device, and failure evidence.
- `starter/STAGE_9_EVIDENCE.md`: human-readable evidence index generated from JSON records.
- `starter/SECURITY_BOUNDARIES.md`: honest adapter, logging, demo, and production boundary documentation.
- `starter/DEMO_RUNBOOK.md`: live path, failure recovery, fallback path, and stop rules.
- `.github/workflows/ci.yml`: PostgreSQL, backend, frontend, browser, evidence, and artefact gates; no deployment job.

---

### Task 1: Lock typed runtime configuration and demo/production boundaries

**Files:**
- Modify: `starter/backend/requirements.txt`
- Modify: `starter/backend/app/config.py`
- Create: `starter/backend/tests/test_config.py`
- Create: `starter/frontend/src/config.ts`
- Create: `starter/frontend/src/config.test.ts`
- Modify: `starter/frontend/src/app/AppShell.tsx`

**Interfaces:**
- Produces `RuntimeMode = Literal["test", "demo", "production"]` in Python and TypeScript.
- Produces `Settings.load() -> Settings` with `SecretStr` for `audio_signing_key` and `demo_control_token`.
- Produces `parseRuntimeConfig(env: Record<string, string | undefined>) -> RuntimeConfig`.
- Production requires `auth_backend="external"`, `rate_limit_backend="external"`, HTTPS API base URL, and all demo controls off.

- [ ] **Step 1: Add the exact dependency and write failing backend boundary tests**

Add `pydantic-settings==2.10.1` to `starter/backend/requirements.txt`.

```python
import pytest
from pydantic import ValidationError
from app.config import Settings


def test_production_rejects_every_local_only_control():
    with pytest.raises(ValidationError) as error:
        Settings(
            mode="production",
            database_url="postgresql://u:p@db/amazwi",
            private_audio_root="/srv/audio",
            audio_signing_key="secret-value",
            auth_backend="demo_header",
            rate_limit_backend="in_memory",
            demo_controls_enabled=True,
            demo_control_token="reset-secret",
            failure_injection_enabled=True,
        )
    message = str(error.value)
    assert "production requires external authentication" in message
    assert "production requires an external distributed rate limiter" in message
    assert "demo controls are forbidden in production" in message


def test_secret_values_are_absent_from_settings_repr():
    settings = Settings.test_defaults(audio_signing_key="audio-secret", demo_control_token="demo-secret")
    rendered = repr(settings)
    assert "audio-secret" not in rendered
    assert "demo-secret" not in rendered
```

- [ ] **Step 2: Run and confirm failure**

Run: `cd starter/backend && python -m pytest tests/test_config.py -v`
Expected: FAIL because the typed settings and validators do not exist.

- [ ] **Step 3: Implement the minimal typed settings**

```python
class RuntimeMode(str, Enum):
    TEST = "test"
    DEMO = "demo"
    PRODUCTION = "production"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AMAZWI_", extra="forbid")
    mode: RuntimeMode
    database_url: str
    private_audio_root: Path
    audio_signing_key: SecretStr
    auth_backend: Literal["demo_header", "external"]
    rate_limit_backend: Literal["in_memory", "external"]
    demo_controls_enabled: bool = False
    demo_control_token: SecretStr | None = None
    failure_injection_enabled: bool = False

    @model_validator(mode="after")
    def validate_boundaries(self) -> "Settings":
        if self.mode is RuntimeMode.PRODUCTION:
            errors = []
            if self.auth_backend != "external": errors.append("production requires external authentication")
            if self.rate_limit_backend != "external": errors.append("production requires an external distributed rate limiter")
            if self.demo_controls_enabled or self.demo_control_token is not None or self.failure_injection_enabled:
                errors.append("demo controls are forbidden in production")
            if errors: raise ValueError("; ".join(errors))
        return self
```

`Settings.test_defaults()` must return an isolated PostgreSQL test URL, a temporary private root supplied by the caller, `demo_header`, `in_memory`, and demo controls enabled. It must never be called by module import in production.

- [ ] **Step 4: Write and satisfy frontend boundary tests**

```ts
import { expect, it } from "vitest";
import { parseRuntimeConfig } from "./config";

it("rejects demo controls in a production bundle", () => {
  expect(() => parseRuntimeConfig({
    VITE_AMAZWI_MODE: "production",
    VITE_AMAZWI_API_BASE_URL: "https://api.example.invalid",
    VITE_AMAZWI_DEMO_CONTROLS: "true",
  })).toThrow("demo controls are forbidden in production");
});
```

`AppShell` reads the parsed config and renders `Local deterministic demo` only in `demo`; it renders no mode control, reset link, or failure control in `production`.

- [ ] **Step 5: Run focused and broad tests**

Run: `cd starter/backend && python -m pytest tests/test_config.py -v`
Run: `cd starter/frontend && npm test -- src/config.test.ts src/app/AppShell.test.tsx`
Run: `cd starter/frontend && npm run build`
Expected: all pass; a production parse with an HTTP API URL or demo flag fails.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/requirements.txt starter/backend/app/config.py starter/backend/tests/test_config.py starter/frontend/src/config.ts starter/frontend/src/config.test.ts starter/frontend/src/app/AppShell.tsx
git commit -m "Hardening: lock typed runtime boundaries"
```

---

### Task 2: Add injectable authentication with no production impersonation path

**Files:**
- Create: `starter/backend/app/auth.py`
- Create: `starter/backend/tests/test_auth.py`
- Modify: `starter/backend/app/main.py`
- Modify: `starter/backend/app/routes/consents.py`
- Modify: `starter/backend/app/routes/audio.py`
- Modify: `starter/backend/app/routes/assignments.py`
- Modify: `starter/backend/app/routes/ops.py`

**Interfaces:**
- Produces immutable `Principal(user_id: UUID, roles: frozenset[str])`.
- Produces protocol `Authenticator.authenticate(request: Request) -> Awaitable[Principal]`.
- Produces `DemoHeaderAuthenticator`, accepted only in `test` and `demo`.
- Produces `require_principal(request) -> Principal` and `require_role("MTN_LANGUAGE_OPS")`.
- `create_app(settings, authenticator=None, rate_limiter=None, failure_injector=None)` fails startup in production when required external adapters are absent.

- [ ] **Step 1: Write failing impersonation and startup tests**

```python
import pytest
from app.auth import DemoHeaderAuthenticator
from app.main import create_app


def test_demo_headers_are_rejected_by_production_settings(production_settings):
    with pytest.raises(RuntimeError, match="external authenticator must be injected"):
        create_app(production_settings, authenticator=DemoHeaderAuthenticator())


def test_ops_uses_authenticated_principal_not_body_user(client, demo_headers, proposal):
    response = client.post(
        f"/ops/missions/{proposal.id}/authorise",
        headers={**demo_headers(user="ordinary-user", roles=[]), "Idempotency-Key": "auth-test-1"},
        json={"operator_id": "mtn-operator"},
    )
    assert response.status_code == 403
    assert response.json()["code"] == "OPERATOR_ROLE_REQUIRED"
```

- [ ] **Step 2: Run and confirm failure**

Run: `cd starter/backend && python -m pytest tests/test_auth.py -v`
Expected: FAIL because authentication still depends on route-local caller data or no adapter exists.

- [ ] **Step 3: Implement the adapter contract and demo implementation**

```python
@dataclass(frozen=True)
class Principal:
    user_id: UUID
    roles: frozenset[str]

class Authenticator(Protocol):
    async def authenticate(self, request: Request) -> Principal: ...

class DemoHeaderAuthenticator:
    async def authenticate(self, request: Request) -> Principal:
        user = request.headers.get("X-Amazwi-Demo-User")
        if not user: raise AuthenticationRequired()
        roles = frozenset(filter(None, request.headers.get("X-Amazwi-Demo-Roles", "").split(",")))
        return Principal(UUID(user), roles)
```

`DemoHeaderAuthenticator` parses only deterministic seeded UUIDs. It never accepts a user or role from JSON. `create_app` rejects this class when mode is `production`. All protected routes derive actor, contributor, verifier, and operator identity from `Principal`.

- [ ] **Step 4: Run auth, consent, audio, peer, and ops suites**

Run: `cd starter/backend && python -m pytest tests/test_auth.py tests/test_consent_api.py tests/test_audio_api.py tests/test_peer_api.py tests/test_missions_api.py -v`
Expected: all pass; body/query identity cannot override the authenticated principal.

- [ ] **Step 5: Commit**

```bash
git add starter/backend/app/auth.py starter/backend/app/main.py starter/backend/app/routes/consents.py starter/backend/app/routes/audio.py starter/backend/app/routes/assignments.py starter/backend/app/routes/ops.py starter/backend/tests/test_auth.py
git commit -m "Hardening: isolate demo authentication behind an adapter"
```

---

### Task 3: Add rate-limit adapters and document the in-memory limit honestly

**Files:**
- Create: `starter/backend/app/rate_limit.py`
- Create: `starter/backend/tests/test_rate_limit.py`
- Modify: `starter/backend/app/main.py`
- Modify: `starter/backend/app/routes/consents.py`
- Modify: `starter/backend/app/routes/audio.py`
- Modify: `starter/backend/app/routes/assignments.py`
- Modify: `starter/backend/app/routes/ops.py`

**Interfaces:**
- Produces `RateLimitPolicy(name: str, limit: int, window_seconds: int)`.
- Produces protocol `RateLimiter.check(key: str, policy: RateLimitPolicy, now: datetime) -> RateLimitDecision`.
- Produces `InMemorySlidingWindowLimiter`, accepted only in `test` and `demo`.
- Exact policies: consent mutations `10/60s`, audio upload/finalise `5/60s`, peer answer/referee `20/60s`, ops authorisation `5/60s`, demo reset/failure control `2/60s`.
- A rejection returns HTTP 429, code `RATE_LIMITED`, and `Retry-After` rounded up to a whole second.

- [ ] **Step 1: Write failing deterministic-window tests**

```python
from datetime import timedelta
from app.rate_limit import InMemorySlidingWindowLimiter, RateLimitPolicy


def test_sixth_audio_mutation_is_limited(fake_clock):
    limiter = InMemorySlidingWindowLimiter()
    policy = RateLimitPolicy("audio_mutation", 5, 60)
    for _ in range(5):
        assert limiter.check("user:u1", policy, fake_clock.now()).allowed
    decision = limiter.check("user:u1", policy, fake_clock.now()).allowed
    assert decision is False


def test_window_expires_without_sleep(fake_clock):
    limiter = InMemorySlidingWindowLimiter()
    policy = RateLimitPolicy("ops_authorise", 1, 60)
    assert limiter.check("user:u1", policy, fake_clock.now()).allowed
    fake_clock.advance(timedelta(seconds=61))
    assert limiter.check("user:u1", policy, fake_clock.now()).allowed
```

- [ ] **Step 2: Run and confirm failure**

Run: `cd starter/backend && python -m pytest tests/test_rate_limit.py -v`
Expected: FAIL because no limiter protocol or deterministic clock integration exists.

- [ ] **Step 3: Implement the minimal sliding window**

```python
@dataclass(frozen=True)
class RateLimitDecision:
    allowed: bool
    remaining: int
    retry_after_seconds: int

class RateLimiter(Protocol):
    def check(self, key: str, policy: RateLimitPolicy, now: datetime) -> RateLimitDecision: ...

class InMemorySlidingWindowLimiter:
    def __init__(self) -> None:
        self._hits: dict[tuple[str, str], deque[datetime]] = {}
```

Prune timestamps at or before `now - window`; never use `sleep` in tests. Key authenticated routes by principal UUID plus policy name. Key unauthenticated demo-control failures by `request.client.host`; do not trust `X-Forwarded-For` in this local adapter.

- [ ] **Step 4: Prove production rejection and route behavior**

Add tests that production rejects `InMemorySlidingWindowLimiter`, successful responses expose `X-RateLimit-Limit` and `X-RateLimit-Remaining`, and 429 responses do not call the underlying mutation service.

- [ ] **Step 5: Run broad backend gates**

Run: `cd starter/backend && python -m pytest tests/test_rate_limit.py tests/test_consent_api.py tests/test_audio_api.py tests/test_peer_api.py tests/test_missions_api.py -v`
Expected: all pass with no reward, consent, assignment, or mission side effect after a limited request.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/rate_limit.py starter/backend/app/main.py starter/backend/app/routes/consents.py starter/backend/app/routes/audio.py starter/backend/app/routes/assignments.py starter/backend/app/routes/ops.py starter/backend/tests/test_rate_limit.py
git commit -m "Hardening: add injectable local rate limits"
```

---

### Task 4: Add PII- and secret-safe structured logging

**Files:**
- Create: `starter/backend/app/safe_logging.py`
- Create: `starter/backend/tests/test_safe_logging.py`
- Modify: `starter/backend/app/main.py`
- Modify: `starter/backend/app/outbox.py`
- Modify: `starter/backend/app/provider.py`
- Modify: `starter/backend/app/council.py`

**Interfaces:**
- Produces `SafeLogEvent(event, level, request_id, route_name, method, status_code, duration_ms, outcome_code, component, attempt)`.
- Produces `emit_safe(logger, event: SafeLogEvent) -> None` as one JSON object per line.
- Produces request middleware that uses a validated UUID request ID or generates one, logs route names rather than raw paths, and returns `X-Request-ID`.
- Unexpected exceptions log exception class only; raw exception text and stack locals are excluded.

- [ ] **Step 1: Write failing leakage tests with canary secrets and PII**

```python
import json

SENSITIVE = [
    "Bearer top-secret", "signed-audio-token", "0712345678", "person@example.com",
    "speaker display name", "private/audio/object-key", "raw transcript words",
]


def test_request_and_failure_logs_exclude_sensitive_values(client, caplog, demo_headers):
    response = client.post(
        "/consents",
        headers={**demo_headers(), "Authorization": SENSITIVE[0], "X-Request-ID": "not-a-uuid"},
        json={"consent_text": SENSITIVE[6], "email": SENSITIVE[3], "phone": SENSITIVE[2]},
    )
    rendered = "\n".join(record.getMessage() for record in caplog.records)
    for value in SENSITIVE:
        assert value not in rendered
    for line in rendered.splitlines():
        json.loads(line)
```

- [ ] **Step 2: Run and confirm failure**

Run: `cd starter/backend && python -m pytest tests/test_safe_logging.py -v`
Expected: FAIL because request/outbox/provider/Council logs are not centrally allowlisted.

- [ ] **Step 3: Implement allowlisted JSON output**

```python
@dataclass(frozen=True)
class SafeLogEvent:
    event: str
    level: Literal["INFO", "WARNING", "ERROR"] = "INFO"
    request_id: str | None = None
    route_name: str | None = None
    method: str | None = None
    status_code: int | None = None
    duration_ms: int | None = None
    outcome_code: str | None = None
    component: str | None = None
    attempt: int | None = None


def emit_safe(logger: logging.Logger, event: SafeLogEvent) -> None:
    payload = {key: value for key, value in asdict(event).items() if value is not None}
    logger.log(getattr(logging, event.level), json.dumps(payload, sort_keys=True, separators=(",", ":")))
```

Do not pass arbitrary dictionaries to `emit_safe`. Replace direct logging in outbox, provider, and Council paths with stable component/outcome codes such as `OUTBOX_RETRY_SCHEDULED`, `PROVIDER_UNAVAILABLE`, and `COUNCIL_SPECIALIST_FAILED`.

- [ ] **Step 4: Add a forbidden-field property test**

Generate nested dictionaries with keys matching `authorization`, `cookie`, `token`, `secret`, `password`, `email`, `phone`, `transcript`, `audio`, `object_key`, and `signed_url`; prove none can enter serialized events because `SafeLogEvent` has no such fields.

- [ ] **Step 5: Run logging and full backend suites**

Run: `cd starter/backend && python -m pytest tests/test_safe_logging.py -v`
Run: `cd starter/backend && python -m pytest -q`
Expected: all pass; captured operational logs parse as JSON and contain none of the canaries.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/safe_logging.py starter/backend/app/main.py starter/backend/app/outbox.py starter/backend/app/provider.py starter/backend/app/council.py starter/backend/tests/test_safe_logging.py
git commit -m "Hardening: emit allowlisted structured logs"
```

---

### Task 5: Add deterministic seed/reset and disable it structurally in production

**Files:**
- Create: `starter/backend/app/runtime.py`
- Create: `starter/backend/app/demo.py`
- Create: `starter/backend/app/routes/demo.py`
- Create: `starter/backend/tests/test_demo_reset.py`
- Modify: `starter/backend/app/main.py`
- Modify: `starter/backend/tests/conftest.py`

**Interfaces:**
- Produces `Clock.now() -> datetime`, `RandomSource.random() -> random.Random`, `SystemClock`, and deterministic test implementations.
- Produces `reset_and_seed(session, store, settings, clock, seed="amazwi-stage9-v1") -> DemoSeedReceipt`.
- Demo API: `POST /__demo/reset`, `GET /__demo/state/{cycle_id}`, `POST /__demo/outbox/drain`.
- `DemoSeedReceipt` contains `seed_version`, `cycle_id`, `state_hash`, seeded speaker/peer/operator UUIDs, campaign UUID, draft contribution UUID, expected reward cents, and no names, tokens, audio paths, or secrets.

- [ ] **Step 1: Write failing reset safety and determinism tests**

```python
import pytest
from app.demo import UnsafeDemoReset, reset_and_seed


def test_reset_refuses_non_demo_database(db_session, store, production_like_settings, fake_clock):
    with pytest.raises(UnsafeDemoReset, match="database name must end in _test or _demo"):
        reset_and_seed(db_session, store, production_like_settings, fake_clock)


def test_two_resets_produce_same_seed_hash_and_clean_counts(demo_runtime):
    first = demo_runtime.reset_and_seed()
    demo_runtime.complete_one_rewarded_flow()
    second = demo_runtime.reset_and_seed()
    assert first.state_hash == second.state_hash
    assert demo_runtime.reward_event_count() == 0
    assert demo_runtime.outbox_count() == 0
    assert demo_runtime.private_object_count() == 0
```

- [ ] **Step 2: Run and confirm failure**

Run: `cd starter/backend && python -m pytest tests/test_demo_reset.py -v`
Expected: FAIL because no guarded deterministic reset exists.

- [ ] **Step 3: Implement destructive guards before reset**

```python
def assert_demo_reset_safe(settings: Settings) -> None:
    database_name = make_url(settings.database_url).database or ""
    if not database_name.endswith(("_test", "_demo")):
        raise UnsafeDemoReset("database name must end in _test or _demo")
    sentinel = settings.private_audio_root / ".amazwi-demo-root"
    if not sentinel.is_file():
        raise UnsafeDemoReset("private audio root sentinel is missing")
    if settings.mode not in {RuntimeMode.TEST, RuntimeMode.DEMO}:
        raise UnsafeDemoReset("reset is unavailable outside test or demo")
```

After all guards pass, truncate application tables in one explicit PostgreSQL transaction, clear only files beneath the resolved sentinel root, seed fixed UUIDv5 identities/campaign/consents/draft contribution, and compute canonical SHA-256 over sorted JSON excluding `cycle_id` and timestamps.

- [ ] **Step 4: Register routes only in test/demo**

`create_app` includes `routes.demo.router` only when `demo_controls_enabled` and mode is `test` or `demo`. Every request requires `X-Amazwi-Demo-Token`, checked with `hmac.compare_digest`, and uses the `2/60s` control policy. Production route-table tests must assert no path beginning `/__demo` exists.

- [ ] **Step 5: Run reset, migration, storage, and resolver suites**

Run: `cd starter/backend && python -m pytest tests/test_demo_reset.py tests/test_migrations.py tests/test_local_storage.py tests/test_resolver.py -v`
Expected: all pass against PostgreSQL 16; two reset hashes match and no prior reward/outbox/blob survives.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/runtime.py starter/backend/app/demo.py starter/backend/app/routes/demo.py starter/backend/app/main.py starter/backend/tests/test_demo_reset.py starter/backend/tests/conftest.py
git commit -m "Hardening: add guarded deterministic demo reset"
```

---

### Task 6: Add deterministic failure injection and backend safety drills

**Files:**
- Create: `starter/backend/app/failures.py`
- Create: `starter/backend/tests/test_failure_drills.py`
- Modify: `starter/backend/app/storage/local.py`
- Modify: `starter/backend/app/consent.py`
- Modify: `starter/backend/app/outbox.py`
- Modify: `starter/backend/app/council.py`
- Modify: `starter/backend/app/provider.py`
- Modify: `starter/backend/app/routes/demo.py`
- Modify: `starter/ml/amazwi_ml/tournament.py`
- Create: `starter/ml/tests/test_model_failure_drill.py`

**Interfaces:**
- Produces `FailurePoint`: `STORAGE_WRITE`, `CONSENT_LOOKUP`, `OUTBOX_DISPATCH`, `AI_SPECIALIST`, `PAYMENT_PROVIDER`, `MODEL_EVALUATION`.
- Produces protocol `FailureInjector.trip(point: FailurePoint) -> None`.
- Produces `NoopFailureInjector` for production and `ScriptedFailureInjector.arm(point, times=1)` for test/demo.
- Demo API: `POST /__demo/failures` accepts one enum value and integer `times` from 1–3; it never accepts arbitrary exception text or code.

- [ ] **Step 1: Write failing safety-matrix tests**

```python
@pytest.mark.parametrize("point", [
    "STORAGE_WRITE", "CONSENT_LOOKUP", "OUTBOX_DISPATCH",
    "AI_SPECIALIST", "PAYMENT_PROVIDER", "MODEL_EVALUATION",
])
def test_failure_point_is_explicit(point):
    assert FailurePoint(point).value == point


def test_storage_failure_creates_no_phantom_contribution(demo_flow):
    demo_flow.arm(FailurePoint.STORAGE_WRITE)
    response = demo_flow.upload_audio()
    assert response.code == "STORAGE_UNAVAILABLE"
    assert demo_flow.contribution_state() == "DRAFT"
    assert demo_flow.private_object_count() == 0


def test_consent_failure_fails_closed(demo_flow):
    demo_flow.arm(FailurePoint.CONSENT_LOOKUP)
    response = demo_flow.request_playback()
    assert response.code == "CONSENT_CHECK_UNAVAILABLE"
    assert demo_flow.playback_token_count() == 0


def test_outbox_failure_retries_without_duplicate_council_output(demo_flow):
    demo_flow.resolve_with_two_peers()
    demo_flow.arm(FailurePoint.OUTBOX_DISPATCH)
    assert demo_flow.drain_outbox().failed == 1
    assert demo_flow.drain_outbox().completed == 1
    assert demo_flow.council_output_count() == 1
```

- [ ] **Step 2: Run and confirm failure**

Run: `cd starter/backend && python -m pytest tests/test_failure_drills.py -v`
Expected: FAIL because deterministic failure points are not injectable.

- [ ] **Step 3: Implement the injector with bounded counters**

```python
class ScriptedFailureInjector:
    def __init__(self) -> None:
        self._remaining = Counter()
    def arm(self, point: FailurePoint, times: int = 1) -> None:
        if times not in range(1, 4): raise ValueError("times must be 1, 2, or 3")
        self._remaining[point] = times
    def trip(self, point: FailurePoint) -> None:
        if self._remaining[point] > 0:
            self._remaining[point] -= 1
            raise InjectedFailure(point)
```

Call `trip` immediately before the external or stateful action. Never call it after marking payment paid, completing an outbox job, moving a model alias, or committing contribution state.

- [ ] **Step 4: Complete all exact safety assertions**

- `AI_SPECIALIST`: peer decision and one reward remain committed; other specialists complete; failed specialist is retryable; receipt Council state is `FAILED` or `PENDING`, never fabricated `READY`.
- `PAYMENT_PROVIDER`: ledger remains credited, provider attempt is idempotent, payment is never `PAID`, and UI contract receives `FAILED` or `SENT_FOR_PAYMENT` according to existing provider semantics.
- `MODEL_EVALUATION`: active baseline alias and prior signed card remain unchanged; no new readiness claim is emitted; result reason is `MODEL_EVALUATION_UNAVAILABLE`.
- Production app construction always installs `NoopFailureInjector` and exposes no arming route.

- [ ] **Step 5: Run backend, ML, resolver, ledger, outbox, and Council suites**

Run: `cd starter/backend && python -m pytest tests/test_failure_drills.py tests/test_resolver.py tests/test_ledger_invariants.py tests/test_outbox.py tests/test_council.py tests/test_provider.py -v`
Run: `cd starter/ml && python -m pytest tests/test_model_failure_drill.py tests -v`
Expected: all pass; failure drills preserve consent authority, one reward, provider honesty, outbox idempotency, and model alias stability.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/failures.py starter/backend/app/storage/local.py starter/backend/app/consent.py starter/backend/app/outbox.py starter/backend/app/council.py starter/backend/app/provider.py starter/backend/app/routes/demo.py starter/backend/tests/test_failure_drills.py starter/ml/amazwi_ml/tournament.py starter/ml/tests/test_model_failure_drill.py
git commit -m "Hardening: add deterministic failure drills"
```

---

### Task 7: Drive the complete governed workflow through Playwright

**Files:**
- Modify: `starter/frontend/package.json`
- Modify: `starter/frontend/package-lock.json`
- Modify: `starter/frontend/playwright.config.ts`
- Create: `starter/frontend/fixtures/demo-audio.wav`
- Create: `starter/frontend/e2e/full-governed-demo.spec.ts`
- Create: `starter/scripts/wait_http.py`

**Interfaces:**
- Produces script `test:e2e:stage9`.
- Uses three isolated browser contexts: seeded speaker, peer one, peer two; each receives only its own demo auth headers.
- Uses Chromium fake microphone with `demo-audio.wav`; the WAV contains generated tones and silence, not a human recording.
- Writes safe JSON evidence to `starter/evidence/stage9/full-demo.json` and Playwright traces to `starter/evidence/stage9/traces/`.

- [ ] **Step 1: Generate the synthetic WAV and write the failing browser test**

Generate a 2-second mono 16kHz WAV from Python `wave` and `math.sin`: 300ms silence, 1.4s alternating 440/660Hz tones, 300ms silence. Commit the binary fixture and its SHA-256 in the test.

```ts
import { expect, test } from "@playwright/test";

const DEMO_AUDIO_SHA256 = "c7c43f7f81c90f8aa86df18c8c2348984deedbaab70cc807f381a83cfcb3a2d1";

test("browser to private storage to two peers to reward to Council receipt", async ({ browser, request }) => {
  const seed = await resetDemo(request);
  const speaker = await contextFor(browser, seed.speakerId);
  const peerOne = await contextFor(browser, seed.peerOneId);
  const peerTwo = await contextFor(browser, seed.peerTwoId);

  const record = await speaker.newPage();
  await record.goto(`/record/${seed.contributionId}`);
  await record.getByRole("button", { name: "Start recording" }).click();
  await record.getByRole("button", { name: "Stop recording" }).click();
  await record.getByRole("button", { name: "Submit privately" }).click();
  await expect(record.getByText("Waiting for 2 proficient peers")).toBeVisible();

  await answerNext(peerOne, "accept");
  await answerNext(peerTwo, "accept");
  await drainOutbox(request);

  await record.goto(`/receipt/${seed.contributionId}`);
  await expect(record.getByText("Confirmed by 2 proficient peers")).toBeVisible();
  await expect(record.getByText("Credited to your AMAZWI balance")).toBeVisible();
  await expect(record.getByLabel("Advisory AI")).toContainText("Model");
});
```

- [ ] **Step 2: Run and confirm failure**

Run: `cd starter/frontend && npm run test:e2e:stage9 -- e2e/full-governed-demo.spec.ts`
Expected: FAIL until local services, fake microphone, auth contexts, demo controls, and complete selectors are wired.

- [ ] **Step 3: Configure bounded local web servers and fake audio**

`playwright.config.ts` starts FastAPI on `127.0.0.1:8000` and Vite on `127.0.0.1:4173`, waits at most 60 seconds for `/health` and `/`, resolves the fixture with `path.resolve("fixtures/demo-audio.wav")`, and passes Chromium `--use-fake-device-for-media-stream` plus ``--use-file-for-fake-audio-capture=${path.resolve("fixtures/demo-audio.wav")}``. Set `reuseExistingServer: false` in CI. Do not bind the backend to a public interface.

- [ ] **Step 4: Assert private-storage and authority boundaries**

The test must additionally prove:

- exactly one `.bin` object exists below the sentinel demo root and its SHA-256 equals the finalised metadata;
- fetching the object key as a public path returns 404;
- peer one cannot use peer two's playback URL or answer peer two's assignment;
- the first peer answer does not resolve or reward;
- the second matching answer produces one decision and one reward event;
- outbox drain produces one Council result; a second drain produces zero new outputs;
- receipt DOM order is peer truth, reward/payment, then advisory Council;
- no route response contains an object key, filesystem path, signing key, demo token, or raw audio bytes.

- [ ] **Step 5: Run the complete local browser gate**

Run: `cd starter/frontend && npm run test:e2e:stage9 -- e2e/full-governed-demo.spec.ts --trace on`
Expected: PASS in Chromium; safe evidence records one private object, two distinct peer IDs as opaque hashes, one decision, one reward, one Council output, and no sensitive values.

- [ ] **Step 6: Commit**

```bash
git add starter/frontend/package.json starter/frontend/package-lock.json starter/frontend/playwright.config.ts starter/frontend/fixtures/demo-audio.wav starter/frontend/e2e/full-governed-demo.spec.ts starter/scripts/wait_http.py
git commit -m "Hardening: verify the full governed browser workflow"
```

---

### Task 8: Add browser-visible failure and reduced-motion drills

**Files:**
- Create: `starter/frontend/e2e/failure-drills.spec.ts`
- Modify: `starter/frontend/src/features/recording/RecordingRoute.tsx`
- Modify: `starter/frontend/src/features/consent/ConsentRoute.tsx`
- Modify: `starter/frontend/src/features/receipt/ReceiptRoute.tsx`
- Modify: `starter/frontend/src/features/ops/OpsRoute.tsx`
- Modify: `starter/frontend/src/styles/motion.css`

**Interfaces:**
- Stable visible recovery copy: `Private upload unavailable. Your contribution was not submitted.`, `Consent check unavailable. Nothing was shared.`, `Insight unavailable. Peer truth and reward are unchanged.`, `Payment provider unavailable. Your credited balance is unchanged.`, and `Model evidence unavailable. No readiness claim is being made.`
- Reduced motion disables waveform morph, peer-connection animation, reward rise, map ripple, and route movement; workflow actions and live status remain available.

- [ ] **Step 1: Write the failing browser matrix**

```ts
for (const drill of [
  ["STORAGE_WRITE", "Private upload unavailable. Your contribution was not submitted."],
  ["CONSENT_LOOKUP", "Consent check unavailable. Nothing was shared."],
  ["AI_SPECIALIST", "Insight unavailable. Peer truth and reward are unchanged."],
  ["PAYMENT_PROVIDER", "Payment provider unavailable. Your credited balance is unchanged."],
  ["MODEL_EVALUATION", "Model evidence unavailable. No readiness claim is being made."],
] as const) {
  test(`${drill[0]} exposes honest recovery`, async ({ page, request }) => {
    await resetAndArm(request, drill[0]);
    await runRelevantBrowserAction(page, drill[0]);
    await expect(page.getByText(drill[1])).toBeVisible();
  });
}
```

Add an outbox drill that resolves peers, arms `OUTBOX_DISPATCH`, observes Council pending without losing truth/reward, drains again, and observes one recovered Council output.

- [ ] **Step 2: Run and confirm failure**

Run: `cd starter/frontend && npm run test:e2e:stage9 -- e2e/failure-drills.spec.ts`
Expected: FAIL until every injected backend state maps to exact honest copy and retry behavior.

- [ ] **Step 3: Add reduced-motion assertions**

```ts
test("reduced motion preserves the whole workflow", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  const durations = await page.evaluate(() =>
    document.getAnimations().map(animation => animation.effect?.getTiming().duration).filter(Number.isFinite),
  );
  expect(durations.every(duration => Number(duration) <= 200)).toBe(true);
  await expect(page.locator("[data-motion='morph'], [data-motion='ripple'], [data-motion='reward-rise']")).toHaveCount(0);
});
```

The recorder's level meter may update at a slower interval while recording, but no decorative animation may run indefinitely.

- [ ] **Step 4: Run browser drills and frontend unit tests**

Run: `cd starter/frontend && npm run test:e2e:stage9 -- e2e/failure-drills.spec.ts`
Run: `cd starter/frontend && npm test`
Expected: all pass; storage and consent fail closed, outbox recovers idempotently, AI/provider/model copy remains honest, and reduced motion changes presentation only.

- [ ] **Step 5: Commit**

```bash
git add starter/frontend/e2e/failure-drills.spec.ts starter/frontend/src/features/recording/RecordingRoute.tsx starter/frontend/src/features/consent/ConsentRoute.tsx starter/frontend/src/features/receipt/ReceiptRoute.tsx starter/frontend/src/features/ops/OpsRoute.tsx starter/frontend/src/styles/motion.css
git commit -m "Hardening: drill visible failures and reduced motion"
```

---

### Task 9: Produce accessibility, performance, and physical target-device evidence

**Files:**
- Create: `starter/frontend/e2e/performance.spec.ts`
- Create: `starter/frontend/scripts/measure-bundle.mjs`
- Create: `starter/frontend/scripts/profile-android.mjs`
- Modify: `starter/frontend/package.json`
- Modify: `starter/frontend/package-lock.json`
- Create: `starter/scripts/record_accessibility_evidence.py`

**Interfaces:**
- Produces scripts `test:performance`, `check:bundle`, and `profile:android`.
- Bundle budget: all production JS plus CSS totals at most 250 KiB gzip.
- Emulated mobile budgets: LCP at most 3000ms, CLS at most 0.10, no long task above 200ms on Home, Record, Verify, Receipt, Impact, and Ops.
- Physical animation budget: p95 frame interval at most 20ms and no frame interval above 50ms during finite transitions.
- Physical target class: Android SDK 31–35, 3–6 GiB RAM, Chrome installed, exactly one authorised ADB device.

- [ ] **Step 1: Write failing bundle and browser performance checks**

```ts
test("receipt stays within mobile performance budgets", async ({ page }) => {
  await page.goto("/receipt/demo-contribution");
  await page.waitForLoadState("networkidle");
  const metrics = await page.evaluate(() => (window as any).__amazwiPerformanceSnapshot());
  expect(metrics.lcpMs).toBeLessThanOrEqual(3000);
  expect(metrics.cls).toBeLessThanOrEqual(0.10);
  expect(metrics.maxLongTaskMs).toBeLessThanOrEqual(200);
});
```

`measure-bundle.mjs` recursively reads `dist/assets`, gzips `.js` and `.css` with Node `zlib.gzipSync`, prints each file and total, and exits 1 above 256000 bytes.

- [ ] **Step 2: Run and confirm failure**

Run: `cd starter/frontend && npm run build && npm run check:bundle`
Run: `cd starter/frontend && npm run test:performance`
Expected: FAIL until scripts, instrumentation, deterministic seeded routes, and budgets exist.

- [ ] **Step 3: Repeat the complete automated accessibility matrix**

Run: `cd starter/frontend && npm run test:a11y`
Run: `cd starter/frontend && npm run test:e2e -- e2e/routes.spec.ts`
Expected: both themes pass at 320, 360, 390, 430, and 480px; 200% text creates no horizontal page scroll; keyboard activation works; every route has zero serious/critical axe violations; reduced motion remains functional.

- [ ] **Step 4: Implement non-interactive physical-device profiling**

`profile-android.mjs` runs `adb devices`, requires exactly one `device` entry, reads `ro.build.version.sdk`, `/proc/meminfo`, `ro.product.manufacturer`, `ro.product.model`, Chrome version, and display size. It refuses devices outside the target class. It opens the local preview through `adb reverse tcp:4173 tcp:4173`, records Home → Record → Receipt → Impact transitions, computes frame intervals from `requestAnimationFrame`, captures screenshots, and writes `starter/evidence/stage9/target-device.json` without serial number, user data, or audio.

Run: `cd starter/frontend && npm run build && npm run preview -- --host 0.0.0.0 --port 4173`
In a second non-interactive process run: `cd starter/frontend && npm run profile:android`
Expected: PASS only with one qualifying physical device. Zero devices, multiple devices, unauthorised ADB, out-of-class memory/SDK, or failed budgets exits 1 and writes `TARGET_DEVICE_NOT_VERIFIED`.

- [ ] **Step 5: Record the manual TalkBack walkthrough**

On the same physical device, enable TalkBack and complete this exact order: skip link, theme control, consent scopes, start/stop recording, private submission status, peer playback label, peer answer, result status, reward status, advisory AI label, impact map equivalent list, ops authorisation confirmation. Every item must announce role, name, state, and changed status without relying on color or motion.

Run after observation: `cd starter && python scripts/record_accessibility_evidence.py --screen-reader TalkBack --steps-passed 12 --steps-total 12 --device-evidence evidence/stage9/target-device.json --output evidence/stage9/talkback.json`
Expected: the script refuses mismatched counts, missing device evidence, or a non-passing target-device record.

- [ ] **Step 6: Run all performance gates and commit**

Run: `cd starter/frontend && npm run build && npm run check:bundle && npm run test:performance && npm run test:a11y`
Run: `cd starter/frontend && npm run profile:android`
Expected: all automated budgets pass and physical plus TalkBack evidence exists. If no qualifying device is available, stop Stage 9 acceptance and record the block; do not substitute emulation.

```bash
git add starter/frontend/e2e/performance.spec.ts starter/frontend/scripts/measure-bundle.mjs starter/frontend/scripts/profile-android.mjs starter/frontend/package.json starter/frontend/package-lock.json starter/scripts/record_accessibility_evidence.py
git commit -m "Hardening: gate accessibility performance and target devices"
```

---

### Task 10: Expand CI without adding any deployment path

**Files:**
- Modify: `.github/workflows/ci.yml`
- Create: `starter/scripts/run_stage9.py`
- Modify: `starter/scripts/wait_http.py`
- Create: `starter/scripts/test_run_stage9.py`

**Interfaces:**
- Produces `python starter/scripts/run_stage9.py --ci` as the ordered non-interactive verifier.
- CI jobs are `backend`, `frontend`, `browser`, and `evidence`; none has deployment permissions or a deployment command.
- Browser job uses PostgreSQL 16, Python 3.12, Node 20, `npm ci`, Playwright Chromium, loopback-only services, and synthetic demo data.
- CI uploads only Playwright reports, traces, screenshots, safe JSON evidence, and sanitized logs; it excludes private-audio roots and environment files.

- [ ] **Step 1: Write failing verifier-order tests**

```python
from starter.scripts.run_stage9 import commands


def test_ci_commands_include_every_gate_and_no_deployment_command():
    joined = "\n".join(" ".join(command) for command in commands(ci=True))
    for required in ["pytest", "npm", "test", "build", "playwright", "check:bundle", "test:performance", "verify-fallback", "check_evidence_claims"]:
        assert required in joined
    assert "vercel" not in joined.lower()
    assert "deploy" not in joined.lower()
    assert "git push" not in joined.lower()
```

- [ ] **Step 2: Run and confirm failure**

Run: `python -m pytest starter/scripts/test_run_stage9.py -v`
Expected: FAIL because the Stage 9 verifier and CI graph do not exist.

- [ ] **Step 3: Implement exact verifier order**

`run_stage9.py --ci` runs and stops on the first non-zero result:

1. `python -m pytest -q` in `starter/backend`.
2. `python -m pytest -q` in `starter/ml`.
3. `npm test` in `starter/frontend`.
4. `npm run build`.
5. `npm run check:bundle`.
6. `npm run test:a11y`.
7. `npm run test:e2e:stage9`.
8. `npm run test:visual`.
9. `npm run test:performance`.
10. `npm run verify-fallback`.
11. `python scripts/check_evidence_claims.py` in `starter`.

It writes command, UTC start/end, exit code, and duration to `starter/evidence/stage9/commands.json`; it never captures environment values.

- [ ] **Step 4: Expand the workflow**

Use `npm ci`, cache npm/pip downloads, keep the existing PostgreSQL 16 service, install Chromium with `npx playwright install --with-deps chromium`, and run browser services on `127.0.0.1`. Add `permissions: contents: read` at workflow level. Do not add `id-token: write`, environment secrets, production URLs, Figma tokens, cloud credentials, or deployment environments.

On failure, upload these exact paths with `actions/upload-artifact@v4`: `starter/frontend/playwright-report`, `starter/frontend/test-results`, `starter/evidence/stage9`, `/tmp/amazwi-backend.log`, `/tmp/amazwi-frontend.log`. Run the log canary test before upload. Never upload the private-audio directory.

- [ ] **Step 5: Validate YAML and run the local orchestrator**

Run: `python -m pytest starter/scripts/test_run_stage9.py -v`
Run: `python starter/scripts/run_stage9.py --ci`
Expected: verifier order test passes; the full command exits 0 only when all available automated gates pass. Physical-device evidence remains a required release/Stage 9 gate but is not fabricated by hosted CI.

- [ ] **Step 6: Commit**

```bash
git add .github/workflows/ci.yml starter/scripts/run_stage9.py starter/scripts/wait_http.py starter/scripts/test_run_stage9.py
git commit -m "Hardening: expand CI verification without deployment"
```

---

### Task 11: Capture fallback artefacts and prove two clean reset cycles

**Files:**
- Create: `starter/frontend/scripts/capture-fallback.mjs`
- Create: `starter/frontend/scripts/verify-fallback.mjs`
- Create: `starter/frontend/scripts/verify-fallback.test.mjs`
- Modify: `starter/frontend/package.json`
- Create: `starter/frontend/e2e/two-reset-cycles.spec.ts`
- Create: `starter/demo/fallback/manifest.json`
- Create: `starter/demo/fallback/receipt.json`
- Create: `starter/demo/fallback/council-disabled.json`
- Create: `starter/demo/fallback/model-no-improvement.json`
- Create: `starter/demo/fallback/screenshots/home.png`
- Create: `starter/demo/fallback/screenshots/receipt.png`
- Create: `starter/demo/fallback/screenshots/impact.png`
- Create: `starter/demo/fallback/screenshots/ops.png`

**Interfaces:**
- Produces scripts `capture:fallback`, `verify:fallback`, and `test:cycles`.
- Fallback manifest schema: `schemaVersion`, `label`, `source`, `generatedAt`, `seedVersion`, `cycleReceiptHash`, `files[{path, sha256, mediaType}]`, `prohibitions[]`.
- Exact label is `Recorded local deterministic demo. Not live, not deployed, no real payment, no production data.`
- Two-cycle evidence contains `cycles[2]`, equal `seedHash`, equal `receiptHash`, reward count `1` per cycle, Council output count `1` per cycle, and zero surviving rows/blobs between resets.

- [ ] **Step 1: Write failing forbidden-content and hash tests**

```js
import assert from "node:assert/strict";
import test from "node:test";
import { verifyFallback } from "./verify-fallback.mjs";

test("fallback rejects audio, secrets, and live claims", async () => {
  const result = await verifyFallback("../demo/fallback");
  assert.equal(result.forbiddenExtensions.includes(".wav"), false);
  assert.equal(result.text.includes("Not live, not deployed"), true);
  assert.equal(result.hashesValid, true);
});
```

The verifier rejects `.wav`, `.webm`, `.ogg`, `.mp3`, `.env`, raw logs, traces containing headers, object keys, signed URLs, tokens, phone/email patterns, exact seeded UUIDs, and the phrases `live production`, `deployed on Vercel`, or `paid by MTN`.

- [ ] **Step 2: Run and confirm failure**

Run: `cd starter/frontend && node --test scripts/verify-fallback.test.mjs`
Expected: FAIL because no capture, manifest, or verifier exists.

- [ ] **Step 3: Prove two reset cycles in one browser test**

```ts
test("two resets produce equivalent complete demonstrations", async ({ browser, request }) => {
  const cycles = [];
  for (let index = 0; index < 2; index += 1) {
    const seed = await resetDemo(request);
    const result = await runFullGovernedBrowserFlow(browser, request, seed);
    cycles.push(result);
  }
  expect(cycles).toHaveLength(2);
  expect(cycles[0].seedHash).toBe(cycles[1].seedHash);
  expect(cycles[0].receiptHash).toBe(cycles[1].receiptHash);
  expect(cycles.map(c => c.rewardCount)).toEqual([1, 1]);
  expect(cycles.map(c => c.councilOutputCount)).toEqual([1, 1]);
});
```

Before cycle two starts, assert cycle one's contribution, reward, outbox rows, Council outputs, and private object are absent after reset. Canonical hashes exclude timestamps, request IDs, cycle IDs, and generated signed URLs.

- [ ] **Step 4: Capture only allowlisted fallback states**

Run: `cd starter/frontend && npm run test:cycles`
Run: `cd starter/frontend && npm run capture:fallback`
Run: `cd starter/frontend && npm run verify:fallback`
Expected: both cycles pass; capture copies four screenshots and three JSON states from cycle two, strips opaque identifiers to stable aliases, writes hashes, and includes no audio, logs, secrets, or production claim.

The three JSON files must show: successful peer/reward/Council receipt; peer/reward receipt with Council disabled; baseline retained with `MODEL_NO_IMPROVEMENT`. They must never say the provider paid money or a model was promoted unless corresponding signed evidence exists.

- [ ] **Step 5: Commit**

```bash
git add starter/frontend/scripts/capture-fallback.mjs starter/frontend/scripts/verify-fallback.mjs starter/frontend/scripts/verify-fallback.test.mjs starter/frontend/package.json starter/frontend/e2e/two-reset-cycles.spec.ts starter/demo/fallback
git commit -m "Hardening: add verified fallback and reset-cycle artefacts"
```

---

### Task 12: Complete the final evidence and honesty review

**Files:**
- Create: `starter/scripts/check_evidence_claims.py`
- Create: `starter/scripts/test_check_evidence_claims.py`
- Create: `starter/STAGE_9_EVIDENCE.md`
- Create: `starter/SECURITY_BOUNDARIES.md`
- Create: `starter/DEMO_RUNBOOK.md`
- Modify: `starter/README.md`
- Modify: `starter/backend/S5_README.md`
- Modify: `starter/frontend/STAGE_7_8_EVIDENCE.md`
- Modify: `05_amazwi/P0.md`
- Modify: `05_amazwi/BUILD_LOG.md`
- Modify: `HANDOVER_SBU.md`
- Modify: `CLAUDE.md`

**Interfaces:**
- `check_evidence_claims.py` reads `starter/evidence/stage9/*.json`, fallback manifest, and the listed Markdown files; exits 1 on an unsupported claim.
- Evidence states are exactly `implemented`, `automated-local-pass`, `physical-device-pass`, `recorded-fallback`, `blocked`, and `not-run`.
- Production auth/rate limiting is described as `adapter boundary implemented; external production adapter not selected or verified`.
- Deployment is described exactly as `Vercel remains paused. No deployment performed.`

- [ ] **Step 1: Write failing honesty-gate tests**

```python
from starter.scripts.check_evidence_claims import validate_claims


def test_rejects_production_and_device_claims_without_evidence(tmp_path):
    doc = tmp_path / "claim.md"
    doc.write_text("Production authentication is complete. Target-device verified.", encoding="utf-8")
    errors = validate_claims([doc], evidence={})
    assert "unsupported production authentication claim" in errors
    assert "unsupported target-device claim" in errors


def test_accepts_exact_paused_deployment_statement(tmp_path):
    doc = tmp_path / "claim.md"
    doc.write_text("Vercel remains paused. No deployment performed.", encoding="utf-8")
    assert validate_claims([doc], evidence={}) == []
```

- [ ] **Step 2: Run and confirm failure**

Run: `python -m pytest starter/scripts/test_check_evidence_claims.py -v`
Expected: FAIL because evidence-backed claim validation does not exist.

- [ ] **Step 3: Implement the claim matrix**

The checker enforces:

- `Stage 9 complete` requires two passing cycles, all automated commands passing, target-device JSON `physical-device-pass`, TalkBack 12/12, and fallback verification.
- `production authentication` or `production rate limiting` is rejected because external adapters are not selected or verified.
- `deployed`, `live production`, `Vercel preview`, or equivalent is rejected unconditionally in this plan.
- `paid` requires a real provider receipt, which this plan intentionally never creates; demo docs use `credited` only.
- `model promoted` requires signed tournament evidence; otherwise docs use `baseline retained` or `model evidence unavailable`.
- `Figma parity` remains governed by plan 03's fresh evidence gate and is rejected when that evidence is absent/stale.
- `target-device verified` requires the physical-device and TalkBack records; browser emulation alone is insufficient.
- fallback screenshots must be labeled recorded local demo, never live.

- [ ] **Step 4: Write the exact operational documentation**

`SECURITY_BOUNDARIES.md` explains runtime modes, startup rejection, demo auth, external-auth gap, per-process limiter limitation, logging allowlist, audit/log separation, reset guards, failure injection, and prohibited production use.

`DEMO_RUNBOOK.md` contains this order: preflight; confirm Vercel paused; verify demo database/sentinel; run automated verifier; run reset cycle one; run reset cycle two; run physical device and TalkBack; present live flow; trigger one safe AI or outbox drill; switch to clearly labeled fallback if live flow fails; stop on any consent, privacy, reward, provider, model, or evidence inconsistency. It includes rollback only by guarded demo reset and never by production data deletion.

`STAGE_9_EVIDENCE.md` lists every command, UTC timestamp, exit code, test count, PostgreSQL version, Python/Node/Chromium versions, two cycle hashes, failure matrix results, viewport/theme matrix, bundle/performance metrics, physical device class, TalkBack result, fallback manifest hash, Figma comparison state from Stage 7–8, and explicit not-run items.

Update project truth files with the same evidence states. Preserve Sbu-review labels for cross-lane work. State that no external identity/rate-limit provider, real payment, real campaign, external AI/model run, Vercel deployment, or production dataset was used.

- [ ] **Step 5: Run the broad final verification**

Run: `cd starter/backend && python -m pytest -q`
Run: `cd starter/ml && python -m pytest -q`
Run: `cd starter/frontend && npm test && npm run build && npm run check:bundle && npm run test:a11y && npm run test:e2e:stage9 && npm run test:visual && npm run test:performance && npm run verify:fallback`
Run: `python -m pytest starter/scripts/test_run_stage9.py starter/scripts/test_check_evidence_claims.py -v`
Run: `cd starter && python scripts/check_evidence_claims.py`
Run: `git diff --check`
Expected: all available automated checks pass, claim checker exits 0, two cycle hashes match, and physical evidence is passing. If physical evidence is blocked, documentation must say `blocked` and Stage 9 remains incomplete.

- [ ] **Step 6: Review repository truth and commit without deploying**

Read the final diff for contradictions, unsupported superlatives, personal data, secrets, production claims, payment claims, model claims, Figma claims, and missing Sbu-review labels. Confirm `git diff --name-only` contains no `.vercel` path, `vercel.json`, environment file, private audio, real recording, credential, or production export.

```bash
git add starter/scripts/check_evidence_claims.py starter/scripts/test_check_evidence_claims.py starter/STAGE_9_EVIDENCE.md starter/SECURITY_BOUNDARIES.md starter/DEMO_RUNBOOK.md starter/README.md starter/backend/S5_README.md starter/frontend/STAGE_7_8_EVIDENCE.md 05_amazwi/P0.md 05_amazwi/BUILD_LOG.md HANDOVER_SBU.md CLAUDE.md
git commit -m "Docs: record Stage 9 evidence and honest boundaries"
```

Do not run `git push`, any Vercel command, any production command, any real provider command, or any campaign launch command.

---

## Stage 9 Stop Rules

Stop immediately and leave the failing evidence intact if any of these occurs:

- production mode registers a demo route, accepts demo headers, accepts the in-memory limiter, or starts without injected external adapters;
- reset can target a database outside `_test`/`_demo` or a storage root without its sentinel;
- a log, trace, screenshot, fallback file, CI artefact, or evidence record contains a secret, personal data, audio, object key, signed URL, or raw identifier;
- storage or consent failure creates a contribution, playback token, assignment, export, or reward that should not exist;
- outbox retry duplicates a Council output; AI failure changes peer truth or reward; provider failure says `PAID`; model failure moves the active alias or creates a readiness claim;
- the complete Playwright path bypasses browser recording, either real peer browser, private storage, resolver, reward, outbox, Council, or receipt;
- reduced motion blocks an action or decorative motion remains unbounded;
- any required viewport, keyboard, axe, bundle, Web Vital, frame, physical-device, or TalkBack gate fails;
- the two reset cycles differ in canonical seed or receipt hash, retain prior rows/blobs, or create anything other than one reward and one Council output per cycle;
- fallback verification fails or fallback artefacts are described as live;
- documentation claims production readiness, deployment, real payment, model promotion, Figma parity, target-device verification, or Stage 9 completion without its exact evidence;
- a Vercel, deployment, real payment/provider, real campaign, external model/AI, production data, Figma mutation, or `git push` command is about to run.

## Final Acceptance Checklist

- [ ] Typed Python and TypeScript configuration rejects every demo-only control in production.
- [ ] Auth and rate limiting are dependency-injected; production fails closed without external adapters.
- [ ] The in-memory limiter limitation is stated exactly and never presented as distributed or production-grade protection.
- [ ] Structured logs are valid allowlisted JSON and pass secret/PII/audio/object-key canary tests.
- [ ] Reset/seed is deterministic, sentinel-guarded, token-protected, rate-limited, and absent from production routes.
- [ ] Storage, consent, outbox, AI, provider, model, and reduced-motion drills prove the specified safe states.
- [ ] Playwright drives browser → API → private storage → two peers → resolver → one reward → outbox → one Council output → receipt.
- [ ] Public object access and cross-peer playback/answer attempts fail.
- [ ] Both first-class themes pass 320–480px, 200% text, keyboard, axe, route, visual, and reduced-motion gates.
- [ ] Bundle, Web Vital, long-task, and animation budgets pass.
- [ ] One qualifying physical Android device and TalkBack 12/12 evidence pass; emulation is not substituted.
- [ ] CI runs backend, ML, frontend, browser, accessibility, visual, performance, fallback, and honesty gates with read-only permissions and no deployment job.
- [ ] Fallback artefacts contain only allowlisted synthetic local-demo states, valid hashes, and the exact recorded-demo label.
- [ ] Two complete guarded reset cycles have equal canonical seed/receipt hashes and exactly one reward and Council output each.
- [ ] `P0.md`, `BUILD_LOG.md`, `HANDOVER_SBU.md`, `CLAUDE.md`, READMEs, runbook, security boundaries, and evidence index distinguish implemented, locally passed, physically passed, fallback, blocked, and not-run states.
- [ ] Vercel remains paused. No deployment, real payment, real campaign, external AI/model run, production data access, or Figma mutation occurred.
