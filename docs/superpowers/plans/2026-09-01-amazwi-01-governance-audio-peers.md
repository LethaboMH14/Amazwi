# AMAZWI Governance, Private Audio and Real Peers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Stages 1–3 so server-derived consent controls private audio and two real peers can create one authoritative atomic decision and reward.

**Architecture:** Add append-only scoped consent with auditable revocation, a local private object-store adapter, audio metadata and signed playback, closed-cohort selection, and typed FastAPI routes. Keep the existing resolver and ledger authoritative; replace caller-supplied consent/quality booleans with database-derived service inputs at the API boundary.

**Tech Stack:** FastAPI, Pydantic, SQLAlchemy 2, Alembic, PostgreSQL 16, pytest, React, TypeScript, Vitest, Testing Library, Web Audio/MediaRecorder.

## Global Constraints

- All constraints in `2026-09-01-amazwi-governed-intelligence-program.md` apply.
- Scope names are exactly `RECORD_PROCESS_ROUND`, `ASSIGNED_VERIFIER_PLAYBACK`, `RETAIN_MODEL_DEVELOPMENT`, `PUBLIC_AUDIO_ATTRIBUTION`.
- `PUBLIC_AUDIO_ATTRIBUTION` is off by default and unused in the competition path.
- A training opt-out never changes peer resolution or configured reward eligibility.
- Every API identity is derived from a fail-closed FastAPI dependency. Request bodies, paths and query strings never select the acting user.
- Local playback URLs expire and point back to an authenticated backend streaming route. That route re-checks current assignment ownership and current consent before opening the private file, so revocation invalidates already-issued URLs.
- `RECORD_PROCESS_ROUND` is the only consent scope used by the Stage 1–3 eligibility wrapper. `RETAIN_MODEL_DEVELOPMENT` is checked only by later export/training code and never changes peer truth or reward.
- Consent rows are never deleted or overwritten. Grant fields are immutable after insert; revocation is the single write-once `revoked_at` transition plus an audit event in the same transaction.
- The paused Vercel deployment is a hard prohibition for this plan, not a conditional stop.

---

### Task 1: Governance and audio schema migration

**Files:**
- Modify: `starter/backend/app/models.py`
- Create: `starter/backend/alembic/versions/b7c8d9e0f1a2_consent_audio.py`
- Modify: `starter/backend/tests/test_migrations.py`
- Create: `starter/backend/tests/test_governance_schema.py`

**Interfaces:**
- Produces: `ConsentScope`, `AudioObjectState`, `AudioObject`, `VerifierQualification`, `CampaignRewardRule`, and `Contribution.reward_rule_id`.
- Preserves: existing `ConsentGrant`, `Contribution`, reward and payment records.

- [ ] **Step 1: Write failing schema tests**

```python
from sqlalchemy.exc import DBAPIError, IntegrityError
from app.models import (
    AudioObject, AudioObjectState, CampaignRewardRule, ConsentGrant,
    ConsentScope, VerifierQualification,
)


def test_only_one_active_grant_per_user_scope(db_session, user):
    db_session.add(ConsentGrant(user_id=user.id, version="2026-09-01", scope=ConsentScope.RECORD_PROCESS_ROUND))
    db_session.commit()
    db_session.add(ConsentGrant(user_id=user.id, version="2026-09-01", scope=ConsentScope.RECORD_PROCESS_ROUND))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_only_one_audio_object_exists_per_contribution(db_session, contribution):
    db_session.add(AudioObject(contribution_id=contribution.id, object_key="audio/a", sha256="a" * 64, state=AudioObjectState.AVAILABLE))
    db_session.commit()
    db_session.add(AudioObject(contribution_id=contribution.id, object_key="audio/b", sha256="b" * 64, state=AudioObjectState.AVAILABLE))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_duplicate_hash_is_recorded_not_rejected(db_session, two_contributions):
    for contribution, key in zip(two_contributions, ("audio/a", "audio/b")):
        db_session.add(AudioObject(contribution_id=contribution.id, object_key=key, sha256="a" * 64, state=AudioObjectState.AVAILABLE))
    db_session.commit()


def test_verifier_qualification_is_persisted_per_language(db_session, user, reviewer):
    db_session.add(VerifierQualification(
        user_id=user.id,
        language="tn",
        qualified_at=NOW,
        reviewed_by=reviewer.id,
    ))
    db_session.commit()


def test_reward_rule_is_positive_and_contribution_snapshots_rule(db_session, campaign, contribution_factory):
    rule = CampaignRewardRule(
        campaign_id=campaign.id,
        version="speaker-v1",
        contribution_reward_cents=200,
        effective_from=NOW,
    )
    db_session.add(rule)
    db_session.flush()
    contribution = contribution_factory(reward_rule_id=rule.id)
    db_session.commit()
    assert contribution.reward_rule_id == rule.id


def test_reward_rule_financial_terms_cannot_be_updated_or_deleted(db_session, reward_rule):
    reward_rule.contribution_reward_cents = 999
    with pytest.raises(DBAPIError, match="campaign reward terms are immutable"):
        db_session.commit()
    db_session.rollback()
    with pytest.raises(DBAPIError, match="campaign reward rules cannot be deleted"):
        db_session.delete(reward_rule)
        db_session.commit()
```

Define `user`, `reviewer`, `campaign`, `contribution_factory`, `contribution`, and `two_contributions` as local fixtures/helpers in `test_governance_schema.py`; the current shared `conftest.py` provides only PostgreSQL engine/session fixtures.

- [ ] **Step 2: Run tests and confirm the models are missing**

Run: `cd starter/backend && python -m pytest tests/test_governance_schema.py -v`
Expected: collection failure because `ConsentScope` and `AudioObject` do not exist.

- [ ] **Step 3: Add exact enums and records**

```python
class ConsentScope(str, enum.Enum):
    RECORD_PROCESS_ROUND = "RECORD_PROCESS_ROUND"
    ASSIGNED_VERIFIER_PLAYBACK = "ASSIGNED_VERIFIER_PLAYBACK"
    RETAIN_MODEL_DEVELOPMENT = "RETAIN_MODEL_DEVELOPMENT"
    PUBLIC_AUDIO_ATTRIBUTION = "PUBLIC_AUDIO_ATTRIBUTION"

class AudioObjectState(str, enum.Enum):
    PENDING = "PENDING"
    AVAILABLE = "AVAILABLE"
    QUARANTINED = "QUARANTINED"
    DELETED = "DELETED"

class AudioObject(Base):
    __tablename__ = "audio_objects"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    contribution_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("contributions.id"), unique=True, nullable=False)
    object_key: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    sha256: Mapped[str | None] = mapped_column(String(64), index=True)
    mime_type: Mapped[str | None] = mapped_column(String)
    codec: Mapped[str | None] = mapped_column(String)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    byte_length: Mapped[int | None] = mapped_column(Integer)
    state: Mapped[AudioObjectState] = mapped_column(SAEnum(AudioObjectState, name="audioobjectstate"), default=AudioObjectState.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
    finalised_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    quarantined_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

class VerifierQualification(Base):
    __tablename__ = "verifier_qualifications"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=False)
    qualified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    reviewed_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (
        CheckConstraint("reviewed_by <> user_id", name="ck_verifier_qualification_independent_reviewer"),
    )

class CampaignRewardRule(Base):
    __tablename__ = "campaign_reward_rules"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    campaign_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("campaigns.id"), nullable=False)
    version: Mapped[str] = mapped_column(String, nullable=False)
    contribution_reward_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (
        CheckConstraint("contribution_reward_cents > 0", name="ck_campaign_reward_positive"),
        UniqueConstraint("campaign_id", "version", name="uq_campaign_reward_rule_version"),
    )
```

Add a PostgreSQL partial unique index on active consent:

```python
Index(
    "uq_consent_active_user_scope",
    ConsentGrant.user_id,
    ConsentGrant.scope,
    unique=True,
    postgresql_where=ConsentGrant.revoked_at.is_(None),
)
```

Add the equivalent partial unique index `uq_verifier_active_user_language` on `(VerifierQualification.user_id, VerifierQualification.language)` where `revoked_at IS NULL`, and `uq_campaign_active_reward_rule` on `CampaignRewardRule.campaign_id` where `retired_at IS NULL`. Add nullable `Contribution.reward_rule_id` for legacy rows; every new contribution created by Task 4 must snapshot one active rule. Reward-rule `campaign_id`, `version`, `contribution_reward_cents`, and `effective_from` are immutable; `retired_at` may transition once from null to a timestamp. Cohort selection must use persisted qualification, not `User.declared_languages` alone.

- [ ] **Step 4: Write the manual Alembic migration**

Set `revision = "b7c8d9e0f1a2"` and `down_revision = "a3ea8e6c052e"`. Before altering `consent_grants.scope`, fail with a descriptive error if any existing value is outside the four locked scopes. Create the enum and use explicit PostgreSQL conversions:

```python
op.alter_column(
    "consent_grants", "scope",
    type_=consent_scope,
    postgresql_using="scope::text::consentscope",
)
# downgrade uses postgresql_using="scope::text"
```

Create `audio_objects`, `verifier_qualifications`, `campaign_reward_rules`, add `contributions.reward_rule_id`, create all partial indexes, and reverse every table/index/type operation in downgrade. Install PostgreSQL triggers that reject `UPDATE` of reward-rule campaign/version/amount/effective time, reject a second or reversed `retired_at` transition, and reject `DELETE`; downgrade drops the triggers/functions before the table. Add migration tests that exercise those triggers, seed one valid legacy varchar scope and prove upgrade preserves it, and prove an invalid legacy value fails before destructive DDL. Existing contributions may retain a null snapshot after migration, but resolver code must reject them as `CAMPAIGN_REWARD_NOT_CONFIGURED`; never invent a migration default amount.

- [ ] **Step 5: Extend migration expectations**

Add `audio_objects`, `verifier_qualifications`, and `campaign_reward_rules` to `test_upgrade_creates_all_expected_tables`; assert the contribution foreign key exists and downgrade removes `consentscope` and `audioobjectstate` alongside existing enums.

- [ ] **Step 6: Run schema and migration tests**

Run: `cd starter/backend && python -m pytest tests/test_governance_schema.py tests/test_migrations.py -v`
Expected: all pass against PostgreSQL 16.

- [ ] **Step 7: Commit**

```bash
git add starter/backend/app/models.py starter/backend/alembic/versions/b7c8d9e0f1a2_consent_audio.py starter/backend/tests/test_governance_schema.py starter/backend/tests/test_migrations.py
git commit -m "Consent: add scoped governance and private audio schema"
```

---

### Task 2: Consent service and API

**Files:**
- Create: `starter/backend/app/config.py`
- Create: `starter/backend/app/db.py`
- Create: `starter/backend/app/identity.py`
- Create: `starter/backend/app/api_types.py`
- Create: `starter/backend/app/consent.py`
- Create: `starter/backend/app/routes/__init__.py`
- Create: `starter/backend/app/routes/consents.py`
- Modify: `starter/backend/app/main.py`
- Create: `starter/backend/tests/test_consent.py`
- Create: `starter/backend/tests/test_consent_api.py`

**Interfaces:**
- Produces: `AuthenticatedIdentity`, `get_current_identity()`, and test-overridable fail-closed identity resolution.
- Produces: `grant_scopes(session, user_id, version, scopes, actor_id) -> list[ConsentGrant]` without committing internally.
- Produces: `revoke_scope(session, user_id, scope, actor_id, reason) -> ConsentGrant` without committing internally.
- Produces: `require_active_scope(session, user_id, scope) -> ConsentGrant`.
- API: `POST /consents`, `GET /consents/me`, `POST /consents/{scope}/revoke`; all three derive the subject/actor from `AuthenticatedIdentity`.

- [ ] **Step 1: Write failing consent matrix tests**

```python
def test_training_opt_out_does_not_remove_round_scope(db_session, user):
    grant_scopes(db_session, user.id, "2026-09-01", [ConsentScope.RECORD_PROCESS_ROUND], user.id)
    assert require_active_scope(db_session, user.id, ConsentScope.RECORD_PROCESS_ROUND)
    with pytest.raises(ConsentRequiredError):
        require_active_scope(db_session, user.id, ConsentScope.RETAIN_MODEL_DEVELOPMENT)


def test_revocation_preserves_audit_and_blocks_future_use(db_session, user):
    grant_scopes(db_session, user.id, "2026-09-01", [ConsentScope.ASSIGNED_VERIFIER_PLAYBACK], user.id)
    revoked = revoke_scope(db_session, user.id, ConsentScope.ASSIGNED_VERIFIER_PLAYBACK, user.id, "user request")
    assert revoked.revoked_at is not None
    assert db_session.scalar(select(AuditEvent).where(AuditEvent.action == "CONSENT_REVOKED"))
    with pytest.raises(ConsentRequiredError):
        require_active_scope(db_session, user.id, ConsentScope.ASSIGNED_VERIFIER_PLAYBACK)
```

- [ ] **Step 2: Run and confirm failure**

Run: `cd starter/backend && python -m pytest tests/test_consent.py -v`
Expected: import failure for `app.consent`.

- [ ] **Step 3: Implement consent service with row locking and idempotency**

```python
class ConsentRequiredError(Exception):
    def __init__(self, scope: ConsentScope):
        self.scope = scope
        super().__init__(f"active consent required: {scope.value}")


def require_active_scope(session: Session, user_id: UUID, scope: ConsentScope) -> ConsentGrant:
    grant = session.scalar(select(ConsentGrant).where(
        ConsentGrant.user_id == user_id,
        ConsentGrant.scope == scope,
        ConsentGrant.revoked_at.is_(None),
    ))
    if grant is None:
        raise ConsentRequiredError(scope)
    return grant
```

`grant_scopes` first locks the subject `User` row, then returns an existing active grant instead of duplicating it. `revoke_scope` locks the active row with `with_for_update()`, rejects a second revocation, sets `revoked_at` exactly once, and writes `AuditEvent`. Neither service commits. The route owns one `with session.begin():` boundary so consent and audit state commit or roll back together. Add tests proving rows cannot be deleted through the service and existing grant metadata is never rewritten.

- [ ] **Step 4: Add typed API contracts**

```python
class ConsentGrantRequest(BaseModel):
    version: str = Field(min_length=1, max_length=64)
    scopes: list[ConsentScope] = Field(min_length=1)

class ConsentState(BaseModel):
    scope: ConsentScope
    version: str
    granted_at: datetime
    revoked_at: datetime | None
```

- [ ] **Step 5: Add database dependency and routes**

`db.py` must read `AMAZWI_DATABASE_URL`, create one engine, and yield a session that rolls back on exception and closes always. `identity.py` must expose an injectable dependency that returns 401 when no authenticated identity is available; it must not trust a body/query/path `user_id`. Stage 9 may replace the verifier behind this interface with OIDC, but Stage 1 routes already fail closed. Map `ConsentRequiredError` to HTTP 403 with `{code: "CONSENT_REQUIRED", scope}`.

In `test_consent_api.py`, construct the app with dependency overrides for both `get_session` and `get_current_identity`. Add an impersonation regression test that sends another user's UUID in extra JSON/query fields and proves the authenticated subject remains the only affected user.

- [ ] **Step 6: Test API idempotency and revocation**

Run: `cd starter/backend && python -m pytest tests/test_consent.py tests/test_consent_api.py -v`
Expected: grant repeat returns one active row; revoke repeat returns 409 `CONSENT_ALREADY_REVOKED`; scope state remains auditable.

- [ ] **Step 7: Run backend suite and commit**

Run: `cd starter/backend && python -m pytest -q`

```bash
git add starter/backend/app starter/backend/tests/test_consent.py starter/backend/tests/test_consent_api.py
git commit -m "Consent: enforce scoped grants and revocations server-side"
```

---

### Task 3: Local private audio adapter

**Files:**
- Create: `starter/backend/app/storage/__init__.py`
- Create: `starter/backend/app/storage/base.py`
- Create: `starter/backend/app/storage/local.py`
- Create: `starter/backend/tests/test_local_storage.py`

**Interfaces:**
- Produces: `AudioObjectStore.begin_upload`, `write_upload`, `finalise`, `open_private`, `quarantine`, `delete`.
- Produces: `SignedAudioToken` containing object key, audience user, assignment/contribution identity, purpose and expiry. A valid signature is necessary but never sufficient for playback.

- [ ] **Step 1: Write failing traversal, expiry and quarantine tests**

```python
def test_object_key_cannot_escape_storage_root(store):
    with pytest.raises(InvalidObjectKey):
        store.write_upload("../secret", b"x")


def test_expired_or_wrong_audience_token_cannot_play(store):
    token = store.issue_token("audio/one", audience="user-a", purpose="VERIFY", ttl_seconds=1, now=NOW)
    with pytest.raises(InvalidAudioToken):
        store.open_private(token, audience="user-b", now=NOW)
    with pytest.raises(InvalidAudioToken):
        store.open_private(token, audience="user-a", now=NOW + timedelta(seconds=2))


def test_quarantine_removes_playback(store):
    store.write_upload("audio/one", b"voice")
    store.quarantine("audio/one")
    with pytest.raises(AudioUnavailable):
        store.open_by_key("audio/one")
```

- [ ] **Step 2: Run and confirm failure**

Run: `cd starter/backend && python -m pytest tests/test_local_storage.py -v`
Expected: missing storage package.

- [ ] **Step 3: Define the protocol and typed exceptions**

```python
class AudioObjectStore(Protocol):
    def write_upload(self, object_key: str, body: bytes) -> StoredObject: ...
    def verify(self, object_key: str, sha256: str, byte_length: int) -> StoredObject: ...
    def issue_token(self, object_key: str, audience: str, purpose: str, ttl_seconds: int, now: datetime) -> str: ...
    def open_private(self, token: str, audience: str, now: datetime) -> BinaryIO: ...
    def quarantine(self, object_key: str) -> None: ...
    def delete(self, object_key: str) -> None: ...
```

- [ ] **Step 4: Implement local storage**

Resolve every key under `AMAZWI_PRIVATE_AUDIO_ROOT`, reject absolute paths and `..`, use SHA-256, `hmac.compare_digest`, URL-safe base64 payloads, and atomic `Path.replace()` from `.pending` to `.bin`. Never mount the directory as static files. `open_private()` remains an internal primitive called only after the audio service has re-authorised the current request against PostgreSQL.

- [ ] **Step 5: Run storage tests and commit**

Run: `cd starter/backend && python -m pytest tests/test_local_storage.py -v`

```bash
git add starter/backend/app/storage starter/backend/tests/test_local_storage.py
git commit -m "Audio: add signed local private object storage"
```

---

### Task 4: Audio upload, finalisation, playback and revocation

**Files:**
- Create: `starter/backend/app/contributions.py`
- Create: `starter/backend/app/audio.py`
- Create: `starter/backend/app/routes/contributions.py`
- Create: `starter/backend/app/routes/audio.py`
- Modify: `starter/backend/app/api_types.py`
- Modify: `starter/backend/app/main.py`
- Create: `starter/backend/tests/test_audio_service.py`
- Create: `starter/backend/tests/test_audio_api.py`
- Create: `starter/backend/tests/test_contribution_api.py`

**Interfaces:**
- Produces: `create_contribution(session, *, principal: AuthenticatedIdentity, card_id) -> Contribution` with no commit.
- API: `POST /contributions` accepts only `card_id`; speaker identity is derived from `AuthenticatedIdentity`.
- API: `POST /contributions/{id}/audio/uploads`.
- API: `PUT /private-audio/uploads/{audio_object_id}` with raw body.
- API: `POST /contributions/{id}/audio/finalise`.
- API: `POST /assignments/{id}/playback` returns a short-lived application URL.
- API: `GET /private-audio/play/{token}` authenticates the caller, re-checks current consent and assignment/contributor authority, then streams from private storage.
- Produces: `finalise_audio(session, store, contribution_id, sha256, mime_type, codec, duration_ms, byte_length)`.

- [ ] **Step 1: Write failing contribution-creation, consent and phantom-submission tests**

```python
def test_contribution_creation_requires_round_consent(api_client, card):
    response = api_client.post("/contributions", json={"card_id": str(card.id)})
    assert response.status_code == 403
    assert response.json()["code"] == "CONSENT_REQUIRED"


def test_contribution_snapshots_persisted_reward_rule(api_client, active_round_consent, card, reward_rule):
    response = api_client.post("/contributions", json={"card_id": str(card.id)})
    assert response.status_code == 201
    contribution = load_contribution(response.json()["id"])
    assert contribution.reward_rule_id == reward_rule.id


def test_upload_requires_round_consent(db_session, store, contribution):
    with pytest.raises(ConsentRequiredError):
        begin_audio_upload(db_session, store, contribution.id, contribution.speaker_id)


def test_failed_hash_does_not_mark_contribution_recorded(db_session, store, contribution, active_round_consent):
    audio = begin_audio_upload(db_session, store, contribution.id, contribution.speaker_id)
    store.write_upload(audio.object_key, b"voice")
    with pytest.raises(AudioHashMismatch):
        finalise_audio(db_session, store, contribution.id, "0" * 64, "audio/webm", "opus", 1800, 5)
    db_session.refresh(contribution)
    assert contribution.state == ContributionState.DRAFT
```

`create_contribution` locks the active `Card`, its `Campaign`, and active `CampaignRewardRule`; requires `RECORD_PROCESS_ROUND`; rejects inactive cards, absent reward configuration, or a rule whose `campaign_id` differs from the card campaign; and sets `speaker_id` from the authenticated principal plus `reward_rule_id` from persisted state. It never accepts speaker, campaign, reward amount or reward version from JSON. The route owns the transaction and audit write. Add a regression test proving a rule from another campaign cannot be snapshotted.

- [ ] **Step 2: Implement deterministic physical checks**

Accept only `audio/webm`, `audio/ogg`, and `audio/wav`; duration must be 500–20,000 ms; SHA-256 and byte length must match. Store quality JSON with rule version and physical results. Do not add ML scoring in this task.

- [ ] **Step 3: Enforce playback authorisation**

All upload/finalise/playback routes derive the caller from `AuthenticatedIdentity`. Assigned verifier playback requires an unanswered assignment belonging to that caller plus active `ASSIGNED_VERIFIER_PLAYBACK` consent from the speaker. Contributor replay requires caller equals speaker plus active `RECORD_PROCESS_ROUND`.

The streaming GET route must repeat those checks on every request before opening the file; an issued token is not a bearer capability. Lock the `AudioObject`, contribution and relevant consent row in a short transaction while authorising the open. Add a two-session race test where a token is issued, playback consent is revoked and committed, and the old token then returns 403 without reading bytes.

Scope effects are distinct: revoking `ASSIGNED_VERIFIER_PLAYBACK` blocks verifier assignment/playback; revoking `RETAIN_MODEL_DEVELOPMENT` only blocks later export/training; revoking `RECORD_PROCESS_ROUND` quarantines the object and blocks further processing. None removes an already-earned reward.

- [ ] **Step 4: Add routes with stable error codes**

Use `CONSENT_REQUIRED`, `CAMPAIGN_REWARD_NOT_CONFIGURED`, `AUDIO_HASH_MISMATCH`, `AUDIO_FORMAT_UNSUPPORTED`, `AUDIO_DURATION_INVALID`, `AUDIO_NOT_AUTHORISED`, `AUDIO_UNAVAILABLE`.

- [ ] **Step 5: Run race and API tests**

Run: `cd starter/backend && python -m pytest tests/test_contribution_api.py tests/test_audio_service.py tests/test_audio_api.py tests/test_resolver.py -v`
Expected: no phantom contribution, expired token rejected, an old token fails after revocation, impersonation attempts fail, revocation wins before new playback, existing resolver tests remain green.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/contributions.py starter/backend/app/audio.py starter/backend/app/routes/contributions.py starter/backend/app/routes/audio.py starter/backend/app/api_types.py starter/backend/app/main.py starter/backend/tests/test_contribution_api.py starter/backend/tests/test_audio_service.py starter/backend/tests/test_audio_api.py
git commit -m "Audio: enforce private upload and authorised playback"
```

---

### Task 5: Closed cohort and real peer API

**Files:**
- Create: `starter/backend/app/cohorts.py`
- Create: `starter/backend/app/routes/assignments.py`
- Modify: `starter/backend/app/routes/contributions.py`
- Modify: `starter/backend/app/resolver.py`
- Modify: `starter/backend/app/api_types.py`
- Modify: `starter/backend/app/main.py`
- Create: `starter/backend/tests/test_cohorts.py`
- Create: `starter/backend/tests/test_peer_api.py`

**Interfaces:**
- Produces: `select_next_verifier(session, contribution_id, language, rng) -> User | None`.
- API: `GET /assignments/next`; verifier identity comes only from `AuthenticatedIdentity`.
- API: `POST /assignments/{id}/answer`.
- API: `POST /assignments/{id}/referee`.
- API: `GET /contributions/{id}/result`.

- [ ] **Step 1: Write failing cohort tests**

```python
def test_cohort_excludes_speaker_prior_assignees_and_wrong_language(db_session, contribution, users):
    chosen = select_next_verifier(db_session, contribution.id, "tn", random.Random(7))
    assert chosen.id == users.eligible_tn.id


def test_revoked_playback_consent_yields_no_assignment(db_session, contribution, verifier):
    revoke_scope(db_session, contribution.speaker_id, ConsentScope.ASSIGNED_VERIFIER_PLAYBACK, contribution.speaker_id, "stop")
    assert select_next_verifier(db_session, contribution.id, "tn", random.Random(7)) is None
```

- [ ] **Step 2: Implement deterministic-in-test random selection**

Select users with age confirmation and an active persisted `VerifierQualification` for the contribution language, not the speaker, and not previously assigned. `declared_languages` alone is not proof of proficiency. Lock the contribution and use the supplied `random.Random`; production passes `secrets.SystemRandom()`.

- [ ] **Step 3: Replace resolver consent boolean at the route boundary**

Refactor the existing resolver into a non-committing internal branch function and create `resolve_from_persisted_state(session, contribution_id) -> EligibilityDecision`. The wrapper is called only after exactly two completed proficient answers; if that precondition is not met it raises `ResolutionNotReadyError` rather than returning a second shape. It owns one transaction, locks the `Contribution` row with `FOR UPDATE`, rechecks any existing `EligibilityDecision`, derives physical quality from the available `AudioObject`, checks only active `RECORD_PROCESS_ROUND` consent, loads the snapshotted `CampaignRewardRule` through `Contribution.reward_rule_id`, verifies that its `campaign_id` matches the contribution card's campaign, and derives campaign/amount/version from that immutable row. It raises `CAMPAIGN_REWARD_NOT_CONFIGURED` for a legacy/null/missing/mismatched rule instead of accepting or inventing an amount. It must never check `RETAIN_MODEL_DEVELOPMENT` for peer resolution or reward. The answer route invokes it after the second answer; `GET /contributions/{id}/result` represents an unresolved contribution as a typed `PENDING` DTO without calling the resolver. No route accepts `consent_active`, `audio_quality_passed`, campaign, reward amount/version, reward recipient, speaker identity or verifier identity from JSON.

Add a real PostgreSQL two-session concurrency test that calls resolution concurrently and proves exactly one `EligibilityDecision`, one `RewardEvent`, one campaign commitment and one final contribution state. A rollback in reward credit must also roll back the decision/state.

- [ ] **Step 4: Write answer/referee API tests**

Test two distinct authenticated real users, assignment-owner enforcement, duplicate answer rejection, learner answers excluded, violation-vote branches, reward idempotency, result polling, self-verification rejection and caller-ID injection attempts.

- [ ] **Step 5: Run peer, resolver and ledger suites**

Run: `cd starter/backend && python -m pytest tests/test_cohorts.py tests/test_peer_api.py tests/test_assignment_invariants.py tests/test_resolver.py tests/test_ledger_invariants.py -v`

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/cohorts.py starter/backend/app/routes/assignments.py starter/backend/app/routes/contributions.py starter/backend/app/resolver.py starter/backend/app/api_types.py starter/backend/app/main.py starter/backend/tests/test_cohorts.py starter/backend/tests/test_peer_api.py
git commit -m "Peers: add closed-cohort assignment and real verifier API"
```

---

### Task 6: Consent, recording and verification frontend

**Files:**
- Create: `starter/frontend/src/api/contracts.ts`
- Create: `starter/frontend/src/api/client.ts`
- Create: `starter/frontend/src/features/consent/ConsentRoute.tsx`
- Create: `starter/frontend/src/features/consent/ConsentRoute.test.tsx`
- Create: `starter/frontend/src/features/recording/RecordingRoute.tsx`
- Create: `starter/frontend/src/features/recording/RecordingRoute.test.tsx`
- Create: `starter/frontend/src/features/verification/VerificationRoute.tsx`
- Create: `starter/frontend/src/features/verification/VerificationRoute.test.tsx`
- Modify: `starter/frontend/src/App.tsx`
- Modify: `starter/frontend/src/HomeRoute.tsx`

**Interfaces:**
- Consumes the exact API routes from Tasks 2, 4 and 5.
- Produces routes `/consent`, `/record/:contributionId`, `/verify`, `/result/:contributionId`.

- [ ] **Step 1: Write failing separate-opt-in consent test**

```tsx
it("allows round consent while model-development retention stays off", async () => {
  render(<ConsentRoute api={fakeApi} />);
  await user.click(screen.getByRole("checkbox", { name: /use my recording to improve models/i }));
  await user.click(screen.getByRole("checkbox", { name: /use my recording to improve models/i }));
  await user.click(screen.getByRole("button", { name: /continue/i }));
  expect(fakeApi.grantConsent).toHaveBeenCalledWith(expect.objectContaining({
    scopes: ["RECORD_PROCESS_ROUND", "ASSIGNED_VERIFIER_PLAYBACK"],
  }));
});
```

- [ ] **Step 2: Implement typed client and visible error mapping**

```ts
export type ApiErrorCode =
  | "CONSENT_REQUIRED" | "AUDIO_HASH_MISMATCH" | "AUDIO_DURATION_INVALID"
  | "AUDIO_NOT_AUTHORISED" | "AUDIO_UNAVAILABLE" | "NO_ASSIGNMENT";

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api${path}`, init);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new ApiError(response.status, body.code ?? "UNKNOWN", body);
  return body as T;
}
```

- [ ] **Step 3: Implement recording without offline raw-audio persistence**

From the home mission/card action, call `POST /contributions` first and navigate to `/record/{returnedId}` only after server-side consent and persisted reward-rule checks pass. Then use `MediaRecorder`, keep the blob in component memory only, provide playback/retry, calculate SHA-256 with `crypto.subtle.digest`, upload raw bytes, and finalise. On reload, raw audio is lost and the UI says so honestly.

- [ ] **Step 4: Implement verifier playback and answer flow**

Request the current authenticated user's assignment, request short-lived playback, render `<audio controls>`, submit answer and violation vote, and show pending state until authoritative result exists. The client never sends a user/verifier ID to select authority. Never show transcript or AI score before the peer result.

- [ ] **Step 5: Run frontend tests and build**

Run: `cd starter/frontend && npm test`
Run: `cd starter/frontend && npm run build`
Expected: both pass.

- [ ] **Step 6: Commit**

```bash
git add starter/frontend/src
git commit -m "UI: add governed consent recording and verifier flows"
```

---

### Task 7: Stage 1–3 end-to-end acceptance and documentation

**Files:**
- Create: `starter/backend/tests/test_governed_peer_e2e.py`
- Create: `starter/backend/GOVERNED_FLOW_README.md`
- Modify: `05_amazwi/P0.md`
- Modify: `05_amazwi/BUILD_LOG.md`
- Modify: `HANDOVER_SBU.md`
- Modify: `CLAUDE.md`

**Interfaces:**
- Verifies the full persisted path and the revocation/error matrix.

- [ ] **Step 1: Write the full failing acceptance test**

Create a campaign with one persisted active reward rule, a card, a speaker and two distinct users with persisted active language qualifications. Exercise the API through three authenticated dependency overrides: grant round/playback consent but not training consent; create the contribution through `POST /contributions`; upload and finalise private audio; create two assignments; submit matching answers; resolve concurrently from two database sessions; and assert exactly one eligibility decision and one reward event with the snapshotted configured amount/version. Then issue a playback URL, revoke playback, and assert both a third assignment and the already-issued URL fail while the reward remains. Finally assert there is no active `RETAIN_MODEL_DEVELOPMENT` grant; Plan 02's export acceptance test will consume this exact state and prove exclusion.

- [ ] **Step 2: Run the acceptance test**

Run: `cd starter/backend && python -m pytest tests/test_governed_peer_e2e.py -v`
Expected after Tasks 1–6: PASS.

- [ ] **Step 3: Run all verification gates**

Run: `cd starter/backend && python -m pytest -q`
Run: `cd starter/frontend && npm test && npm run build`
Run migration roundtrip twice against `AMAZWI_TEST_DATABASE_URL` when configured.

- [ ] **Step 4: Update truth documents**

Record exact commands/counts, local-storage-only status, no deployment claim, no training claim, and cross-lane pending-Sbu-review status. Document any untested target-device or browser permissions as open.

- [ ] **Step 5: Commit and push**

```bash
git add starter/backend/tests/test_governed_peer_e2e.py starter/backend/GOVERNED_FLOW_README.md 05_amazwi/P0.md 05_amazwi/BUILD_LOG.md HANDOVER_SBU.md CLAUDE.md
git commit -m "Docs: verify governed private peer flow"
git push origin main
```
