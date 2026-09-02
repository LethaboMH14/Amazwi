# AMAZWI Council, Governed Data and Model Campaign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Stages 4–6 so every committed peer resolution emits a recoverable advisory event, only approved and reproducible data reaches model development, and deterministic ASR/tabular tournaments produce evidence-backed promotion decisions within a 60 GPU-hour aggregate budget.

**Architecture:** Extend the PostgreSQL authority plane with an outbox row written in the resolver transaction, claim work with `FOR UPDATE SKIP LOCKED`, and persist independently versioned Council outputs without allowing AI to change peer truth, consent, money, audio state, exports, or model aliases. Build a provenance firewall in the backend and a separate `starter/ml` package for canonical manifests, speaker-safe splits, external-source preflight, metrics, deterministic tournaments, Kaggle-compatible scripts, challengers, model cards, and hashed evidence.

**Tech Stack:** Python 3.11+, FastAPI, Pydantic, SQLAlchemy 2, Alembic, PostgreSQL 16, pytest, canonical JSON/SHA-256, PyYAML, NumPy, scikit-learn, LightGBM, XGBoost, Hugging Face Transformers/PEFT, Kaggle scripts.

## Global Constraints

- All constraints in `2026-09-01-amazwi-governed-intelligence-program.md` apply.
- Plan 01 must be green first. This plan consumes server-derived consent, private `AudioObject` metadata, closed-cohort peer decisions, and `resolve_from_persisted_state(...)`.
- Peer verification is authoritative. Council work starts only from a committed `ContributionResolved` event and remains advisory.
- The resolver transaction writes contribution state, eligibility decision, reward/campaign commitment, and outbox event atomically. A rollback leaves none of those new writes committed.
- Council-disabled, Council-pending, Council-failed, and worker-crash states must preserve peer decision, reward, wallet, receipt, and result polling.
- `SELECT ... FOR UPDATE SKIP LOCKED` must be tested against real PostgreSQL 16. SQLite is forbidden for schema, resolver, outbox, consent, export, and concurrency tests.
- No Council specialist may change eligibility, money, consent, audio retention, campaign launch, export approval, or model aliases.
- Every advisory output is idempotent on `(event_id, specialist, model_version)` and records canonical input hash, structured output, timestamps, retry count, and failure evidence.
- Training reads only approved immutable manifests. It never queries unrestricted production audio or infers model-development consent from application state.
- Every row has exactly one source class: `EXTERNAL_LICENSED`, `AMAZWI_OPTED_IN`, `EVALUATION_ONLY`, or `SYNTHETIC_FIXTURE`.
- Revoked or missing `RETAIN_MODEL_DEVELOPMENT` consent blocks new AMAZWI export inclusion without changing earned rewards or historical audit evidence.
- No external dataset bytes may be downloaded until an exact registry revision, licence, restrictions, intended task, reviewer, and approved preflight artefact exist.
- Swivuriso data is ASR-only. TTS, voice cloning, synthesis, and human-voice replication use are prohibited.
- AfriSwitch is evaluation-only unless a later reviewed registry commit explicitly approves the exact training use.
- NCHLT, Lwazi, and FLEURS remain blocked until exact hosted versions and licences pass preflight.
- The two Kaggle account aliases are `team-sonar-a` and `team-sonar-b`, each capped at 30 GPU hours; aggregate reserved plus completed GPU time may never exceed 60 hours.
- No real Kaggle GPU run, external download, deployment, payment, campaign launch, or model-alias change occurs without its explicit gate approval.
- TDD is mandatory. Every task begins with a failing test, reaches green, runs its relevant broader suite, and ends in a focused commit.
- Cross-lane backend, data, money, and deployment work remains pending Sbu review and must be labelled accurately in evidence documents.

---

## Locked File Structure

### Backend

- `starter/backend/app/models.py`: outbox, Council, dataset source, export, and approval records.
- `starter/backend/app/outbox.py`: enqueue, `SKIP LOCKED` claim, lease, retry, completion, and recovery.
- `starter/backend/app/council.py`: specialist contracts, deterministic baselines, orchestration, and advisory-output persistence.
- `starter/backend/app/datasets.py`: source registry, consent/licence filtering, export drafting, and human approval.
- `starter/backend/app/routes/council.py`: read-only contribution Council status.
- `starter/backend/scripts/run_council_worker.py`: recoverable one-shot or polling worker.
- `starter/backend/scripts/recover_outbox.py`: audited administrative lease release/retry.
- `starter/backend/alembic/versions/c8d9e0f1a2b3_council_outbox.py`: Stage 4 schema.
- `starter/backend/alembic/versions/d9e0f1a2b3c4_dataset_exports.py`: Stage 5 schema.

### ML and data

- `starter/ml/requirements.txt`: CPU orchestration, metrics, tests, and tabular challengers.
- `starter/ml/requirements-kaggle.txt`: pinned speech-training dependencies layered on the CPU file.
- `starter/ml/amazwi_ml/manifest.py`: manifest schema, canonical bytes, hashing, and immutable writes.
- `starter/ml/amazwi_ml/splits.py`: deterministic speaker-safe split assignment.
- `starter/ml/amazwi_ml/external.py`: registry loading, preflight validation, and download gate.
- `starter/ml/amazwi_ml/metrics.py`: WER, CER, embedded-span error, calibration, and tabular metrics.
- `starter/ml/amazwi_ml/tournament.py`: deterministic candidate ordering and promotion policies.
- `starter/ml/amazwi_ml/budget.py`: 60-hour reservation/completion ledger.
- `starter/ml/amazwi_ml/tabular.py`: rule baseline, LightGBM/XGBoost challengers, calibration, and leakage evidence.
- `starter/ml/amazwi_ml/evidence.py`: model-card and evidence-index generation.
- `starter/ml/registry/external_datasets.yaml`: reviewed source metadata and blocked/allowed task policy.
- `starter/ml/kaggle/*.py`: notebook-compatible preflight, ASR, tabular, evaluation, and packaging entry points.
- `starter/ml/model_cards/README.md`: generated-card contract and claim rules.

---

### Task 1: Add the PostgreSQL outbox and Council schema

**Files:**
- Modify: `starter/backend/app/models.py`
- Create: `starter/backend/alembic/versions/c8d9e0f1a2b3_council_outbox.py`
- Create: `starter/backend/tests/test_council_schema.py`
- Modify: `starter/backend/tests/test_migrations.py`

**Interfaces:**
- Produces: `OutboxEvent`, `CouncilOutput`, `CouncilOutputState`.
- Enforces: unique `OutboxEvent.dedupe_key` and unique `(CouncilOutput.event_id, specialist, model_version)`.
- Migration: `revision = "c8d9e0f1a2b3"`, `down_revision = "b7c8d9e0f1a2"`.

- [ ] **Step 1: Write failing schema tests**

```python
from sqlalchemy.exc import IntegrityError
from app.models import CouncilOutput, CouncilOutputState, OutboxEvent


def test_outbox_dedupe_key_is_unique(db_session, contribution):
    for _ in range(2):
        db_session.add(OutboxEvent(
            event_type="ContributionResolved",
            aggregate_type="Contribution",
            aggregate_id=contribution.id,
            dedupe_key=f"contribution-resolved:{contribution.id}",
            payload_json={"contribution_id": str(contribution.id)},
        ))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_council_output_is_unique_per_event_specialist_version(db_session, outbox_event):
    db_session.add(CouncilOutput(event_id=outbox_event.id, specialist="DATA_STEWARD", model_version="rules-1", state=CouncilOutputState.SUCCEEDED, input_sha256="a" * 64, output_json={}))
    db_session.commit()
    db_session.add(CouncilOutput(event_id=outbox_event.id, specialist="DATA_STEWARD", model_version="rules-1", state=CouncilOutputState.SUCCEEDED, input_sha256="a" * 64, output_json={}))
    with pytest.raises(IntegrityError):
        db_session.commit()
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/backend && python -m pytest tests/test_council_schema.py -v`
Expected: collection fails because the three model types do not exist.

- [ ] **Step 3: Add the minimal records**

```python
class CouncilOutputState(str, enum.Enum):
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"

class OutboxEvent(Base):
    __tablename__ = "outbox_events"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    event_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    aggregate_type: Mapped[str] = mapped_column(String, nullable=False)
    aggregate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    dedupe_key: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    payload_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
    available_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False, index=True)
    claimed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    claimed_by: Mapped[str | None] = mapped_column(String)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    attempt_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_error: Mapped[str | None] = mapped_column(Text)

class CouncilOutput(Base):
    __tablename__ = "council_outputs"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("outbox_events.id"), nullable=False)
    specialist: Mapped[str] = mapped_column(String, nullable=False)
    model_version: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[CouncilOutputState] = mapped_column(SAEnum(CouncilOutputState, name="council_output_state"), nullable=False)
    input_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    output_json: Mapped[dict | None] = mapped_column(JSONB)
    confidence: Mapped[float | None] = mapped_column(Float)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    failure_reason: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (UniqueConstraint("event_id", "specialist", "model_version", name="uq_council_event_specialist_version"),)
```

- [ ] **Step 4: Write the manual migration and extend migration expectations**

Create both tables, the named enum, foreign key, unique constraints, and an outbox-ready partial index on `(available_at, occurred_at)` where `completed_at IS NULL`. Add `outbox_events` and `council_outputs` to the expected-table set. Downgrade drops tables before `council_output_state`.

- [ ] **Step 5: Run schema and migration tests**

Run: `cd starter/backend && python -m pytest tests/test_council_schema.py tests/test_migrations.py -v`
Expected: all pass against PostgreSQL 16, including downgrade then upgrade.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/models.py starter/backend/alembic/versions/c8d9e0f1a2b3_council_outbox.py starter/backend/tests/test_council_schema.py starter/backend/tests/test_migrations.py
git commit -m "Council: add transactional outbox and advisory schema"
```

---

### Task 2: Emit `ContributionResolved` in the resolver transaction

**Files:**
- Create: `starter/backend/app/outbox.py`
- Modify: `starter/backend/app/resolver.py`
- Create: `starter/backend/tests/test_resolver_outbox.py`
- Modify: `starter/backend/tests/test_resolver.py`

**Interfaces:**
- Produces: `enqueue_event(session, *, event_type: str, aggregate_type: str, aggregate_id: UUID, dedupe_key: str, payload: dict) -> OutboxEvent` with no commit.
- Modifies: `resolve_from_persisted_state(...)` to enqueue exactly one event after a final decision is formed and before the single commit.
- Event payload keys: `contribution_id`, `decision`, `understood`, `corpus_eligible`, `consent_version`, `decided_at`.

- [ ] **Step 1: Write failing atomicity and idempotency tests**

```python
def test_resolver_commits_one_event_with_decision_and_reward(db_session, resolved_fixture):
    decision = resolved_fixture.resolve()
    events = db_session.scalars(select(OutboxEvent)).all()
    assert len(events) == 1
    assert events[0].dedupe_key == f"contribution-resolved:{decision.contribution_id}"
    assert events[0].payload_json["decision"] == "CORPUS_ELIGIBLE"
    assert db_session.scalar(select(func.count()).select_from(RewardEvent)) == 1


def test_reward_failure_rolls_back_decision_state_and_outbox(db_session, underfunded_fixture):
    before = underfunded_fixture.contribution.state
    with pytest.raises(InsufficientCampaignFunds):
        underfunded_fixture.resolve()
    assert underfunded_fixture.reload().state == before
    assert db_session.get(EligibilityDecision, underfunded_fixture.contribution.id) is None
    assert db_session.scalar(select(func.count()).select_from(OutboxEvent)) == 0
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/backend && python -m pytest tests/test_resolver_outbox.py -v`
Expected: the success case finds zero outbox rows.

- [ ] **Step 3: Add a no-commit enqueue helper**

```python
def enqueue_event(session: Session, *, event_type: str, aggregate_type: str, aggregate_id: UUID, dedupe_key: str, payload: dict) -> OutboxEvent:
    existing = session.scalar(select(OutboxEvent).where(OutboxEvent.dedupe_key == dedupe_key))
    if existing:
        return existing
    event = OutboxEvent(event_type=event_type, aggregate_type=aggregate_type, aggregate_id=aggregate_id, dedupe_key=dedupe_key, payload_json=payload)
    session.add(event)
    return event
```

- [ ] **Step 4: Insert the event before the resolver's existing single commit**

After decision and optional `credit_reward(..., commit=False)` using the contribution's snapshotted `CampaignRewardRule`, call `session.flush()` so `decided_at` exists, enqueue the event, then retain the single commit/rollback block. `resolve_from_persisted_state` continues to return `EligibilityDecision`; on retry it returns the existing decision and separately verifies that the matching deduplicated outbox event exists, creating it only as a repair inside the same locked transaction if a pre-Stage-4 historical decision has none. `ResolutionNotReadyError` remains the sole precondition outcome before two completed proficient answers and emits no event.

- [ ] **Step 5: Run focused and broader authority tests**

Run: `cd starter/backend && python -m pytest tests/test_resolver_outbox.py tests/test_resolver.py tests/test_ledger_invariants.py -v`
Expected: resolver, reward, and event counts remain one under retries.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/outbox.py starter/backend/app/resolver.py starter/backend/tests/test_resolver_outbox.py starter/backend/tests/test_resolver.py
git commit -m "Council: emit resolver event in the authority transaction"
```

---

### Task 3: Claim outbox work with `SKIP LOCKED`, leases, retry, and recovery

**Files:**
- Modify: `starter/backend/app/outbox.py`
- Create: `starter/backend/tests/test_outbox.py`
- Create: `starter/backend/tests/test_outbox_concurrency.py`
- Create: `starter/backend/scripts/recover_outbox.py`

**Interfaces:**
- Produces: `claim_events(session, *, worker_id: str, now: datetime, limit: int = 10, lease_seconds: int = 60) -> list[OutboxEvent]`.
- Produces: `complete_event(session, event_id: UUID, worker_id: str, now: datetime) -> None`.
- Produces: `retry_event(session, event_id: UUID, worker_id: str, now: datetime, error: str) -> datetime`.
- Produces: `release_event_for_admin_retry(session, event_id: UUID, actor_id: UUID, reason: str, now: datetime) -> None` and an `OUTBOX_ADMIN_RETRY` audit row.

- [ ] **Step 1: Write failing two-worker concurrency test**

```python
def test_two_workers_never_claim_the_same_rows(db_engine, seeded_outbox_ids):
    barrier = Barrier(2)
    def claim(worker):
        with Session(db_engine) as session:
            barrier.wait()
            return {row.id for row in claim_events(session, worker_id=worker, now=NOW, limit=2)}
    with ThreadPoolExecutor(max_workers=2) as pool:
        a, b = [f.result() for f in [pool.submit(claim, "w1"), pool.submit(claim, "w2")]]
    assert a.isdisjoint(b)
    assert len(a | b) == 4
```

Also test expired leases become claimable, active leases do not, completion checks worker ownership, retry increments `attempt_count`, and delays are exactly `min(2 ** attempt_count, 300)` seconds.

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/backend && python -m pytest tests/test_outbox.py tests/test_outbox_concurrency.py -v`
Expected: imports fail because claim/retry functions do not exist.

- [ ] **Step 3: Implement the PostgreSQL claim transaction**

```python
stmt = (
    select(OutboxEvent)
    .where(
        OutboxEvent.completed_at.is_(None),
        OutboxEvent.available_at <= now,
        or_(OutboxEvent.claimed_at.is_(None), OutboxEvent.claimed_at < now - timedelta(seconds=lease_seconds)),
    )
    .order_by(OutboxEvent.occurred_at, OutboxEvent.id)
    .with_for_update(skip_locked=True)
    .limit(limit)
)
rows = list(session.scalars(stmt))
for row in rows:
    row.claimed_at = now
    row.claimed_by = worker_id
session.commit()
```

`complete_event` and `retry_event` lock the row, require matching `claimed_by`, and commit their state transition. Retry clears the lease, stores a 2,000-character maximum error, and sets deterministic `available_at`.

- [ ] **Step 4: Implement audited administrative recovery**

The script requires `AMAZWI_DATABASE_URL`, `AMAZWI_ADMIN_ACTOR_ID`, `--event-id`, and `--reason`. It calls only `release_event_for_admin_retry`; it never edits peer, reward, consent, audio, or Council output rows.

Run dry help: `cd starter/backend && python scripts/recover_outbox.py --help`

- [ ] **Step 5: Run focused and broader PostgreSQL tests**

Run: `cd starter/backend && python -m pytest tests/test_outbox.py tests/test_outbox_concurrency.py tests/test_resolver_outbox.py tests/test_migrations.py -v`
Expected: no duplicate claims and no lost events.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/outbox.py starter/backend/tests/test_outbox.py starter/backend/tests/test_outbox_concurrency.py starter/backend/scripts/recover_outbox.py
git commit -m "Council: add skip-locked worker recovery"
```

---

### Task 4: Add versioned advisory specialist contracts and deterministic baselines

**Files:**
- Modify: `starter/backend/app/config.py`
- Create: `starter/backend/app/council.py`
- Create: `starter/backend/tests/test_council.py`

**Interfaces:**
- Produces: `ResolutionFacts`, `SpecialistResult`, `CouncilSpecialist`.
- Produces specialists `DataStewardRulesV1`, `SoundSentinelRulesV1`, `LanguageScoutRulesV1`, `ExplainerRulesV1`.
- Produces: `run_council_event(session, event: OutboxEvent, specialists: Sequence[CouncilSpecialist], now: datetime) -> list[CouncilOutput]`.
- Config: `AI_COUNCIL_ENABLED: bool = False` by default and `AI_COUNCIL_MAX_ATTEMPTS: int = 5`.

- [ ] **Step 1: Write failing contract, idempotency, and authority-isolation tests**

```python
def test_council_outputs_are_advisory_and_idempotent(db_session, resolved_event, specialists):
    before = authority_snapshot(db_session, resolved_event.aggregate_id)
    first = run_council_event(db_session, resolved_event, specialists, NOW)
    second = run_council_event(db_session, resolved_event, specialists, NOW)
    assert [(x.specialist, x.model_version) for x in first] == [(x.specialist, x.model_version) for x in second]
    assert authority_snapshot(db_session, resolved_event.aggregate_id) == before


def test_data_steward_never_converts_missing_training_consent_to_ready(facts_without_training_consent):
    result = DataStewardRulesV1().run(facts_without_training_consent)
    assert result.code == "BLOCKED_CONSENT"
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/backend && python -m pytest tests/test_council.py -v`
Expected: import failure for `app.council`.

- [ ] **Step 3: Add exact contracts and canonical hashing**

```python
@dataclass(frozen=True)
class SpecialistResult:
    code: str
    evidence: dict[str, Any]
    confidence: float | None = None

class CouncilSpecialist(Protocol):
    name: str
    version: str
    def run(self, facts: ResolutionFacts) -> SpecialistResult: ...

def canonical_sha256(value: dict[str, Any]) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
```

The Data Steward returns only `TRAINING_READY`, `BLOCKED_CONSENT`, `BLOCKED_LICENCE`, `BLOCKED_REVOKED`, or `REVIEW_REQUIRED`. Sound Sentinel emits a bounded `re_record_risk` and explanation from persisted deterministic features. Language Scout emits blind-spot/code-switch categories without changing the peer label. Explainer consumes redacted structured specialist results, not raw audio.

- [ ] **Step 4: Persist each specialist independently**

Lock or create the unique output row, mark it `RUNNING`, execute the specialist, then persist `SUCCEEDED`. On exception, persist `FAILED`, increment `retry_count`, and retain the other specialists' successful outputs. A rerun skips already successful `(event, specialist, version)` rows.

- [ ] **Step 5: Run Council and authority suites**

Run: `cd starter/backend && python -m pytest tests/test_council.py tests/test_resolver_outbox.py tests/test_ledger_invariants.py -v`
Expected: Council retries do not change any authority-plane row.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/config.py starter/backend/app/council.py starter/backend/tests/test_council.py
git commit -m "Council: add versioned advisory specialists"
```

---

### Task 5: Add the recoverable worker, read API, and AI-disabled isolation

**Files:**
- Create: `starter/backend/scripts/run_council_worker.py`
- Create: `starter/backend/app/routes/council.py`
- Modify: `starter/backend/app/api_types.py`
- Modify: `starter/backend/app/main.py`
- Create: `starter/backend/tests/test_council_worker.py`
- Create: `starter/backend/tests/test_council_api.py`
- Create: `starter/backend/tests/test_ai_disabled_e2e.py`

**Interfaces:**
- Worker flags: `--once`, `--worker-id`, `--batch-size`, `--poll-seconds`.
- API: `GET /contributions/{contribution_id}/council`.
- Response: `CouncilStatusDTO(state: Literal["DISABLED","PENDING","PARTIAL","READY","FAILED"], outputs: list[CouncilOutputDTO])`.
- Output ordering: `DATA_STEWARD`, `SOUND_SENTINEL`, `LANGUAGE_SCOUT`, `EXPLAINER`.

- [ ] **Step 1: Write failing worker and disabled-mode acceptance tests**

```python
def test_ai_disabled_preserves_complete_peer_reward_path(client, resolved_fixture, settings):
    settings.AI_COUNCIL_ENABLED = False
    result = client.get(f"/contributions/{resolved_fixture.id}/result").json()
    council = client.get(f"/contributions/{resolved_fixture.id}/council").json()
    assert result["peer_decision"] == "CORPUS_ELIGIBLE"
    assert result["reward_state"] == "CREDITED"
    assert council == {"state": "DISABLED", "outputs": []}


def test_one_failed_specialist_does_not_erase_successful_outputs(worker_fixture):
    worker_fixture.run([DataStewardRulesV1(), RaisingSpecialist(), LanguageScoutRulesV1()])
    assert worker_fixture.states() == {"DATA_STEWARD": "SUCCEEDED", "RAISING": "FAILED", "LANGUAGE_SCOUT": "SUCCEEDED"}
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/backend && python -m pytest tests/test_council_worker.py tests/test_council_api.py tests/test_ai_disabled_e2e.py -v`
Expected: route and worker imports fail.

- [ ] **Step 3: Implement worker completion rules**

When disabled, the process exits 0 without claiming rows. When enabled, it claims a batch, runs all configured specialists, completes the event only when all configured outputs succeeded, and retries the event while any output is failed and `attempt_count < AI_COUNCIL_MAX_ATTEMPTS`. After the limit, leave structured successful outputs readable, retain failed evidence, mark the event completed with `last_error="COUNCIL_ATTEMPTS_EXHAUSTED"`, and never block the peer result.

- [ ] **Step 4: Implement read-only status mapping**

Return `PENDING` for no outputs on an enabled event, `PARTIAL` for mixed success/running/failure before exhaustion, `READY` when all configured outputs succeeded, and `FAILED` when attempts are exhausted with no successful output. Never return raw audio keys, unrestricted payloads, prompts, or provider secrets.

- [ ] **Step 5: Run Stage 4 broader verification**

Run: `cd starter/backend && python -m pytest tests/test_council_schema.py tests/test_resolver_outbox.py tests/test_outbox.py tests/test_outbox_concurrency.py tests/test_council.py tests/test_council_worker.py tests/test_council_api.py tests/test_ai_disabled_e2e.py -v`
Run: `cd starter/backend && python scripts/run_council_worker.py --help`
Expected: all tests pass; help performs no database mutation.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/scripts/run_council_worker.py starter/backend/app/routes/council.py starter/backend/app/api_types.py starter/backend/app/main.py starter/backend/tests/test_council_worker.py starter/backend/tests/test_council_api.py starter/backend/tests/test_ai_disabled_e2e.py
git commit -m "Council: expose recoverable advisory status"
```

---

### Task 6: Add dataset provenance, licence, consent, and export registry schema

**Files:**
- Modify: `starter/backend/app/models.py`
- Create: `starter/backend/alembic/versions/d9e0f1a2b3c4_dataset_exports.py`
- Create: `starter/backend/tests/test_dataset_schema.py`
- Modify: `starter/backend/tests/test_migrations.py`

**Interfaces:**
- Produces enums: `DatasetSourceClass`, `DatasetSourceState`, `DatasetExportState`.
- Produces records: `DatasetSource`, `DatasetExport`, `DatasetExportRow`.
- Migration: `revision = "d9e0f1a2b3c4"`, `down_revision = "c8d9e0f1a2b3"`.

- [ ] **Step 1: Write failing source-class and immutability tests**

```python
def test_export_row_has_exactly_one_source_class(db_session, draft_export):
    row = DatasetExportRow(export_id=draft_export.id, source_class=DatasetSourceClass.AMAZWI_OPTED_IN, source_record_id="c1", contribution_id=None, object_sha256="a" * 64, included=True)
    db_session.add(row)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_approved_export_hash_cannot_be_replaced(db_session, approved_export):
    with pytest.raises(IntegrityError):
        db_session.execute(update(DatasetExport).where(DatasetExport.id == approved_export.id).values(manifest_sha256="b" * 64))
        db_session.commit()
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/backend && python -m pytest tests/test_dataset_schema.py -v`
Expected: imports fail for dataset models.

- [ ] **Step 3: Add exact records and constraints**

`DatasetSource` stores immutable `source_id`, `version`, repository URL, exact revision, SPDX licence identifier, restrictions JSON, allowed-task array, language/domain arrays, state, registry SHA-256, reviewer, and review timestamp. `DatasetExport` stores state, requested/approved actors, approval timestamp, canonical manifest ID/hash, and purpose. `DatasetExportRow` stores one source class, one stable source record ID, optional contribution ID only for `AMAZWI_OPTED_IN`, source/object hashes, consent version, inclusion decision, and exclusion reason.

Add database checks:

```sql
(source_class = 'AMAZWI_OPTED_IN' AND contribution_id IS NOT NULL)
OR (source_class <> 'AMAZWI_OPTED_IN' AND contribution_id IS NULL)
```

Approved rows require non-null approval actor/time and 64-character manifest hash. Add a PostgreSQL trigger that rejects changes to `manifest_id`, `manifest_sha256`, `purpose`, or approval fields after state becomes `APPROVED`; revocation changes only state and revocation audit fields.

- [ ] **Step 4: Write migration and roundtrip expectations**

Create/drop the three named enums and tables in dependency order. Extend expected tables and enum cleanup tests.

- [ ] **Step 5: Run schema and migration tests**

Run: `cd starter/backend && python -m pytest tests/test_dataset_schema.py tests/test_migrations.py -v`
Expected: all pass against PostgreSQL 16.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/models.py starter/backend/alembic/versions/d9e0f1a2b3c4_dataset_exports.py starter/backend/tests/test_dataset_schema.py starter/backend/tests/test_migrations.py
git commit -m "Data: add provenance and immutable export registry"
```

---

### Task 7: Build export candidates from persisted licence and consent state

**Files:**
- Create: `starter/backend/app/datasets.py`
- Create: `starter/backend/tests/test_datasets.py`
- Create: `starter/backend/tests/test_dataset_export_concurrency.py`

**Interfaces:**
- Produces: `register_source(session, spec: DatasetSourceSpec, actor_id: UUID) -> DatasetSource`.
- Produces: `draft_export(session, *, purpose: str, source_ids: Sequence[str], contribution_ids: Sequence[UUID], actor_id: UUID, now: datetime) -> DatasetExport`.
- Produces: `approve_export(session, *, export_id: UUID, manifest_id: str, manifest_sha256: str, actor_id: UUID, now: datetime) -> DatasetExport`.
- Produces: `revoke_export(session, *, export_id: UUID, actor_id: UUID, reason: str, now: datetime) -> DatasetExport`.

- [ ] **Step 1: Write failing consent/licence matrix tests**

```python
def test_draft_includes_only_separately_opted_in_unrevoked_amazwi_rows(db_session, export_fixture):
    draft = draft_export(db_session, purpose="ASR_TRAINING", source_ids=[], contribution_ids=export_fixture.ids, actor_id=export_fixture.actor, now=NOW)
    rows = {row.source_record_id: row for row in draft.rows}
    assert rows[export_fixture.ready].included is True
    assert rows[export_fixture.no_training_consent].exclusion_reason == "BLOCKED_CONSENT"
    assert rows[export_fixture.revoked].exclusion_reason == "BLOCKED_REVOKED"
    assert rows[export_fixture.not_peer_decided].exclusion_reason == "REVIEW_REQUIRED"


def test_blocked_external_source_cannot_enter_approved_export(db_session, blocked_source, actor):
    draft = draft_export(db_session, purpose="ASR_TRAINING", source_ids=[blocked_source.source_id], contribution_ids=[], actor_id=actor.id, now=NOW)
    with pytest.raises(ExportApprovalError, match="BLOCKED_LICENCE"):
        approve_export(db_session, export_id=draft.id, manifest_id="sha256:" + "a" * 64, manifest_sha256="a" * 64, actor_id=actor.id, now=NOW)
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/backend && python -m pytest tests/test_datasets.py -v`
Expected: import failure for `app.datasets`.

- [ ] **Step 3: Implement the provenance firewall**

For AMAZWI rows require: final peer decision, acceptable deterministic audio state/quality, active `RETAIN_MODEL_DEVELOPMENT`, no later revocation, available private object, and no audit block. Re-evaluate all rows inside `approve_export` while locking the export and source rows; a draft created before revocation must fail approval or retain the row as excluded. External sources require `DatasetSource.state == PREFLIGHT_PASSED` and the requested purpose in `allowed_tasks`.

- [ ] **Step 4: Make approval human, audited, and concurrency-safe**

Two concurrent approvals of one draft must converge on one approved record with the first actor/hash, or one success plus one deterministic `ExportAlreadyFinalisedError`. Write `DATASET_EXPORT_REQUESTED`, `DATASET_EXPORT_APPROVED`, `DATASET_EXPORT_REJECTED`, and `DATASET_EXPORT_REVOKED` audit events with actor, purpose, manifest, rule version `export-rules-1`, and reason.

- [ ] **Step 5: Run export, consent, and concurrency suites**

Run: `cd starter/backend && python -m pytest tests/test_datasets.py tests/test_dataset_export_concurrency.py tests/test_consent.py tests/test_governance_schema.py -v`
Expected: revocation blocks new inclusion and leaves rewards unchanged.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/datasets.py starter/backend/tests/test_datasets.py starter/backend/tests/test_dataset_export_concurrency.py
git commit -m "Data: enforce licence consent and export approval"
```

---

### Task 8: Create immutable canonical manifests and speaker-safe splits

**Files:**
- Create: `starter/ml/requirements.txt`
- Create: `starter/ml/amazwi_ml/__init__.py`
- Create: `starter/ml/amazwi_ml/manifest.py`
- Create: `starter/ml/amazwi_ml/splits.py`
- Create: `starter/ml/tests/test_manifest.py`
- Create: `starter/ml/tests/test_splits.py`
- Create: `starter/ml/tests/fixtures/records.json`

**Interfaces:**
- Produces: `ManifestRecord`, `DatasetManifest`, `canonical_bytes(manifest) -> bytes`, `manifest_sha256(manifest) -> str`, `write_immutable_manifest(manifest, path) -> str`.
- Produces: `assign_speaker_splits(records, *, seed: str, train_ratio: float = 0.8, dev_ratio: float = 0.1) -> tuple[ManifestRecord, ...]`.
- Canonical encoding: UTF-8 JSON, sorted keys, compact separators, NFC strings, records sorted by `(source_id, record_id)`, one trailing newline.

- [ ] **Step 1: Write failing byte-identity and speaker-isolation tests**

```python
def test_manifest_rebuild_is_byte_identical(tmp_path, fixture_records):
    a = build_manifest(fixture_records, generated_at="2026-09-01T00:00:00Z")
    b = build_manifest(list(reversed(fixture_records)), generated_at="2026-09-01T00:00:00Z")
    assert canonical_bytes(a) == canonical_bytes(b)
    assert manifest_sha256(a) == manifest_sha256(b)


def test_no_speaker_crosses_splits(fixture_records):
    rows = assign_speaker_splits(fixture_records, seed="amazwi-split-v1")
    memberships = defaultdict(set)
    for row in rows:
        memberships[(row.source_id, row.speaker_id)].add(row.split)
    assert all(len(splits) == 1 for splits in memberships.values())
```

Also test an existing path with different bytes raises `ImmutableManifestConflict`, while identical bytes are accepted idempotently.

- [ ] **Step 2: Add exact CPU dependencies and run failure**

`starter/ml/requirements.txt`:

```text
pytest==8.4.1
pydantic==2.11.7
PyYAML==6.0.2
numpy==2.2.6
scikit-learn==1.6.1
lightgbm==4.6.0
xgboost==3.0.4
```

Run: `cd starter/ml && python -m pip install -r requirements.txt && python -m pytest tests/test_manifest.py tests/test_splits.py -v`
Expected: imports fail because manifest and split modules do not exist.

- [ ] **Step 3: Implement canonical schema and immutable write**

```python
def canonical_bytes(manifest: DatasetManifest) -> bytes:
    value = normalise_nfc(manifest.model_dump(mode="json", exclude_none=False))
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")

def write_immutable_manifest(manifest: DatasetManifest, path: Path) -> str:
    raw = canonical_bytes(manifest)
    if path.exists():
        if path.read_bytes() != raw:
            raise ImmutableManifestConflict(str(path))
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()
```

The schema includes dataset ID/version, source repository/revision, licence/restrictions, allowed tasks, language/domain, AMAZWI consent version, transforms/tool versions, source/output hashes, split, exclusions/revocations, approval actor/time, and export registry ID.

- [ ] **Step 4: Implement deterministic speaker splits**

Group by `(source_id, speaker_id)`. Hash `f"{seed}\0{source_id}\0{speaker_id}"` with SHA-256, map the first 8 bytes to `[0,1)`, assign `<0.8` train, `<0.9` dev, otherwise test, then sort records canonically. Reject missing speaker IDs for trainable/evaluation records instead of creating row-random splits.

- [ ] **Step 5: Run tests twice and compare hashes**

Run: `cd starter/ml && python -m pytest tests/test_manifest.py tests/test_splits.py -v`
Run: `cd starter/ml && python -m pytest tests/test_manifest.py tests/test_splits.py -v`
Expected: both runs pass and fixture manifest hashes match.

- [ ] **Step 6: Commit**

```bash
git add starter/ml/requirements.txt starter/ml/amazwi_ml starter/ml/tests/test_manifest.py starter/ml/tests/test_splits.py starter/ml/tests/fixtures/records.json
git commit -m "Data: add canonical manifests and speaker-safe splits"
```

---

### Task 9: Add the external dataset registry and hard preflight download gate

**Files:**
- Create: `starter/ml/registry/external_datasets.yaml`
- Create: `starter/ml/amazwi_ml/external.py`
- Create: `starter/ml/kaggle/preflight_external.py`
- Create: `starter/ml/kaggle/download_external.py`
- Create: `starter/ml/tests/test_external_registry.py`
- Create: `starter/ml/tests/test_external_preflight.py`

**Interfaces:**
- Produces: `load_registry(path) -> ExternalRegistry`.
- Produces: `approve_preflight(registry, *, dataset_id, exact_revision, intended_task, reviewer, reviewed_at, terms_accepted) -> PreflightEvidence`.
- Produces: `require_download_preflight(registry, evidence, *, dataset_id, intended_task) -> ExternalDatasetSpec`.
- Download command refuses network access unless evidence decision is `APPROVED`, registry hash matches, exact revision is non-empty, and intended task is allowed.

- [ ] **Step 1: Write failing blocked-download tests**

```python
@pytest.mark.parametrize("dataset_id", ["swivuriso", "afriswitch", "common-voice-26-setswana", "nchlt", "lwazi", "fleurs"])
def test_download_without_approved_preflight_is_refused(registry, dataset_id):
    with pytest.raises(PreflightRequired):
        require_download_preflight(registry, None, dataset_id=dataset_id, intended_task="ASR_TRAINING")


def test_swivuriso_rejects_synthesis_task(registry):
    with pytest.raises(TaskProhibited):
        approve_preflight(registry, dataset_id="swivuriso", exact_revision="0123456789abcdef", intended_task="TTS", reviewer="data-steward@example.test", reviewed_at="2026-09-01T00:00:00Z", terms_accepted=True)
```

- [ ] **Step 2: Write the exact registry policy**

Registry entries:

- `swivuriso`: `https://huggingface.co/datasets/dsfsi-anv/za-african-next-voices-compressed`, gated `CC-BY-4.0`, allowed `ASR_TRAINING` and `ASR_EVALUATION`, prohibited `TTS`, `VOICE_CLONING`, `SPEECH_SYNTHESIS`, `HUMAN_VOICE_REPLICATION`, exact commit required at preflight.
- `afriswitch`: `https://arxiv.org/abs/2608.26434`, `CC-BY-4.0`, allowed `ASR_EVALUATION` only, acquisition blocked until an exact dataset-card URL and revision are reviewed into the registry.
- `common-voice-26-setswana`: Mozilla Data Collective dataset `cmqi705f100gemf07q1khput8`, release `26.0`, `CC0-1.0`, allowed `ASR_TRAINING` and `ASR_EVALUATION`, speaker-safe split required.
- `nchlt`, `lwazi`, `fleurs`: state `BLOCKED_METADATA_REVIEW`, no allowed tasks, with the exact reason `Exact hosted version and licence not approved.`

- [ ] **Step 3: Run and verify failure**

Run: `cd starter/ml && python -m pytest tests/test_external_registry.py tests/test_external_preflight.py -v`
Expected: imports fail for `amazwi_ml.external`.

- [ ] **Step 4: Implement registry hashing and gate scripts**

`preflight_external.py` reads only metadata, writes canonical JSON evidence, and performs no download. `download_external.py` validates the evidence before importing a network client; `--dry-run` prints dataset, exact revision, task, destination, and registry hash without network access.

Run: `cd starter/ml && python kaggle/download_external.py --dataset swivuriso --task ASR_TRAINING --dry-run`
Expected: exit 2 and `PREFLIGHT_REQUIRED` when no evidence path is supplied.

- [ ] **Step 5: Run registry tests and safe CLI checks**

Run: `cd starter/ml && python -m pytest tests/test_external_registry.py tests/test_external_preflight.py -v`
Run: `cd starter/ml && python kaggle/preflight_external.py --help && python kaggle/download_external.py --help`
Expected: tests pass; help and refused dry-run perform no download.

- [ ] **Step 6: Commit**

```bash
git add starter/ml/registry/external_datasets.yaml starter/ml/amazwi_ml/external.py starter/ml/kaggle/preflight_external.py starter/ml/kaggle/download_external.py starter/ml/tests/test_external_registry.py starter/ml/tests/test_external_preflight.py
git commit -m "Data: gate external datasets on reviewed preflight"
```

---

### Task 10: Add ASR WER, CER, and embedded-span metrics

**Files:**
- Create: `starter/ml/amazwi_ml/metrics.py`
- Create: `starter/ml/tests/test_metrics.py`
- Create: `starter/ml/tests/fixtures/asr_cases.json`

**Interfaces:**
- Produces: `normalise_transcript(text: str) -> str` using Unicode NFC, casefold, punctuation-to-space, and collapsed whitespace.
- Produces: `word_error_rate(reference: str, hypothesis: str) -> float`.
- Produces: `character_error_rate(reference: str, hypothesis: str) -> float` excluding spaces after normalisation.
- Produces: `embedded_span_error(reference: str, hypothesis: str, spans: Sequence[TokenSpan]) -> float`.
- Produces: `evaluate_asr(cases: Sequence[AsrCase]) -> AsrMetricReport` with aggregate, language, domain, acoustic-condition, and code-switch slices.

- [ ] **Step 1: Write failing exact-value tests**

```python
def test_wer_cer_and_embedded_span_are_exact():
    ref = "ngicela buy airtime manje"
    hyp = "ngicela bye airtime manje"
    assert word_error_rate(ref, hyp) == pytest.approx(0.25)
    assert character_error_rate(ref, hyp) == pytest.approx(1 / 23)
    assert embedded_span_error(ref, hyp, [TokenSpan(start=1, end=3, language="en")]) == pytest.approx(0.5)


def test_empty_reference_policy_is_explicit():
    assert word_error_rate("", "") == 0.0
    with pytest.raises(InvalidReference):
        word_error_rate("", "speech")
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/ml && python -m pytest tests/test_metrics.py -v`
Expected: import failure for `amazwi_ml.metrics`.

- [ ] **Step 3: Implement deterministic Levenshtein alignment**

Use dynamic programming with tie-break order `equal`, `substitute`, `delete`, `insert`. WER denominator is reference words; CER denominator is reference non-space characters. Embedded-span error counts substitutions/deletions aligned to reference tokens inside declared spans plus insertions whose left alignment point is inside the span, divided by span reference-token count.

- [ ] **Step 4: Implement slice reports**

Report raw counts and rates for `zu`, `tn`, each domain, each acoustic condition, aggregate, and embedded code-switch spans. Refuse duplicate case IDs or missing language/speaker IDs. Keep untouched evaluation membership from the manifest and do not resplit in metric code.

- [ ] **Step 5: Run metric tests**

Run: `cd starter/ml && python -m pytest tests/test_metrics.py -v`
Expected: exact fixture values and deterministic slice ordering pass.

- [ ] **Step 6: Commit**

```bash
git add starter/ml/amazwi_ml/metrics.py starter/ml/tests/test_metrics.py starter/ml/tests/fixtures/asr_cases.json
git commit -m "ML: add ASR and embedded-span metrics"
```

---

### Task 11: Add deterministic tournaments and promotion gates

**Files:**
- Create: `starter/ml/amazwi_ml/tournament.py`
- Create: `starter/ml/tests/test_tournament.py`
- Create: `starter/ml/tests/fixtures/tournament_asr.json`
- Create: `starter/ml/tests/fixtures/tournament_tabular.json`

**Interfaces:**
- Produces: `CandidateEvidence`, `PromotionPolicy`, `PromotionDecision`.
- Produces: `rank_candidates(candidates: Sequence[CandidateEvidence], metric: str, lower_is_better: bool) -> tuple[CandidateEvidence, ...]`.
- Produces: `evaluate_asr_promotion(baseline, candidate) -> PromotionDecision`.
- Produces: `evaluate_tabular_promotion(baseline, candidate, task: Literal["QUALITY_RISK","MISSION_RANKING"]) -> PromotionDecision`.

- [ ] **Step 1: Write failing threshold and deterministic tie-break tests**

```python
def test_asr_candidate_is_blocked_when_only_wer_passes():
    decision = evaluate_asr_promotion(
        baseline=asr(wer=.40, cer=.20, embedded=.30, worst_slice=.45),
        candidate=asr(wer=.36, cer=.206, embedded=.30, worst_slice=.45),
    )
    assert decision.promoted is False
    assert "CER_REGRESSION" in decision.reason_codes


def test_equal_candidates_use_candidate_id_tie_break():
    ranked = rank_candidates([candidate("b", .2), candidate("a", .2)], "wer", True)
    assert [x.candidate_id for x in ranked] == ["a", "b"]
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/ml && python -m pytest tests/test_tournament.py -v`
Expected: import failure for `amazwi_ml.tournament`.

- [ ] **Step 3: Implement exact ASR gate**

Promote per language only when all conditions hold:

1. held-out WER relative reduction is at least `5.0%`;
2. CER regression is at most `0.5` absolute percentage points;
3. embedded-span error regression is at most `1.0` absolute percentage point;
4. no declared slice with at least 30 references regresses by more than `2.0` absolute WER points;
5. manifest, config, checkpoint, predictions, and metric-report SHA-256 values are present and valid;
6. candidate and baseline use the same immutable evaluation manifest hash.

- [ ] **Step 4: Implement exact tabular gates**

`QUALITY_RISK`: Brier score relative improvement at least `2.0%`, AUCPR not lower, ECE at most `0.05`, and maximum protected-language false-positive-rate gap no more than baseline gap plus `0.02`.

`MISSION_RANKING`: NDCG@10 relative improvement at least `2.0%`, MAP@10 not lower, and maximum protected-language exposure gap no more than baseline gap plus `0.02`.

A failed gate returns `promoted=False`; it never changes a deployment alias. Store every reason code in stable sorted order.

- [ ] **Step 5: Run tournament tests twice**

Run: `cd starter/ml && python -m pytest tests/test_tournament.py -v`
Run: `cd starter/ml && python -m pytest tests/test_tournament.py -v`
Expected: byte-identical decision JSON for both runs.

- [ ] **Step 6: Commit**

```bash
git add starter/ml/amazwi_ml/tournament.py starter/ml/tests/test_tournament.py starter/ml/tests/fixtures/tournament_asr.json starter/ml/tests/fixtures/tournament_tabular.json
git commit -m "ML: add deterministic promotion tournament"
```

---

### Task 12: Add Kaggle scripts and the 60-hour aggregate budget ledger

**Files:**
- Create: `starter/ml/requirements-kaggle.txt`
- Create: `starter/ml/amazwi_ml/budget.py`
- Create: `starter/ml/kaggle/budget.json`
- Create: `starter/ml/kaggle/reserve_run.py`
- Create: `starter/ml/kaggle/train_asr.py`
- Create: `starter/ml/kaggle/evaluate_asr.py`
- Create: `starter/ml/kaggle/package_run.py`
- Create: `starter/ml/tests/test_budget.py`
- Create: `starter/ml/tests/test_kaggle_scripts.py`

**Interfaces:**
- Produces: `reserve_gpu_run(ledger_path, *, run_id, account_alias, phase, requested_hours, manifest_sha256, config_sha256) -> BudgetReservation`.
- Produces: `complete_gpu_run(ledger_path, *, run_id, actual_gpu_hours, artefact_sha256) -> BudgetEntry`.
- Ledger allocations: `0–6` preflight/splits, `6–14` fixed tournament, `14–30` isiZulu adaptation, `30–46` Setswana adaptation, `46–54` tabular challengers, `54–60` reproducibility/cards/export.

- [ ] **Step 1: Write failing budget refusal tests**

```python
def test_aggregate_budget_cannot_exceed_sixty_hours(tmp_path):
    ledger = seeded_ledger(tmp_path, completed_a=30, completed_b=29)
    with pytest.raises(BudgetExceeded):
        reserve_gpu_run(ledger, run_id="run-60", account_alias="team-sonar-b", phase="REPRODUCIBILITY", requested_hours=2, manifest_sha256="a" * 64, config_sha256="b" * 64)


def test_each_account_is_capped_at_thirty_hours(tmp_path):
    ledger = seeded_ledger(tmp_path, reserved_a=29.5)
    with pytest.raises(AccountBudgetExceeded):
        reserve_gpu_run(ledger, run_id="run-a", account_alias="team-sonar-a", phase="ISIZULU_ADAPTATION", requested_hours=1, manifest_sha256="a" * 64, config_sha256="b" * 64)
```

- [ ] **Step 2: Pin Kaggle model dependencies and run failure**

`requirements-kaggle.txt` starts with `-r requirements.txt` and pins:

```text
torch==2.6.0
transformers==4.53.2
datasets==3.6.0
accelerate==1.8.1
peft==0.16.0
safetensors==0.5.3
soundfile==0.13.1
librosa==0.11.0
```

Run: `cd starter/ml && python -m pytest tests/test_budget.py tests/test_kaggle_scripts.py -v`
Expected: imports fail for budget and Kaggle entry points.

- [ ] **Step 3: Implement atomic ledger transitions**

Use canonical JSON with entries sorted by `run_id`, write to a sibling temporary file, `flush`, `os.fsync`, then `os.replace`. Count active reservations plus completed actual hours. Reject duplicate run IDs, unknown account aliases, non-positive requests, missing hashes, per-account totals over 30, aggregate totals over 60, and phase totals beyond their declared ranges.

- [ ] **Step 4: Implement notebook-compatible scripts**

Every script exposes `main(argv: Sequence[str] | None = None) -> int`, accepts explicit seed, manifest path/hash, config path/hash, output directory, run ID, and budget reservation. `train_asr.py` supports candidate IDs `whisper-large-v3-turbo-peft`, `w2v-bert-2-african`, and `xls-r-mms-comparator`; it performs no model download before external/model licence preflight succeeds. `package_run.py` hashes config, checkpoint, predictions, metrics, logs, and environment lock.

- [ ] **Step 5: Run only CPU-safe verification**

Run: `cd starter/ml && python -m pytest tests/test_budget.py tests/test_kaggle_scripts.py -v`
Run: `cd starter/ml && python kaggle/reserve_run.py --ledger kaggle/budget.json --show`
Run: `cd starter/ml && python kaggle/train_asr.py --help && python kaggle/evaluate_asr.py --help && python kaggle/package_run.py --help`
Expected: tests and help pass; no GPU reservation, external download, model download, or Kaggle submission occurs.

- [ ] **Step 6: Commit**

```bash
git add starter/ml/requirements-kaggle.txt starter/ml/amazwi_ml/budget.py starter/ml/kaggle starter/ml/tests/test_budget.py starter/ml/tests/test_kaggle_scripts.py
git commit -m "ML: add Kaggle campaign budget controls"
```

---

### Task 13: Add deterministic LightGBM and XGBoost challengers

**Files:**
- Create: `starter/ml/amazwi_ml/tabular.py`
- Create: `starter/ml/kaggle/train_tabular.py`
- Create: `starter/ml/tests/test_tabular.py`
- Create: `starter/ml/tests/fixtures/tabular_quality.csv`
- Create: `starter/ml/tests/fixtures/tabular_missions.csv`

**Interfaces:**
- Produces: `train_quality_challengers(train, dev, *, seed: int) -> tuple[TabularRun, ...]`.
- Produces: `train_mission_challengers(train, dev, *, seed: int) -> tuple[TabularRun, ...]`.
- Produces candidates `RULE_BASELINE`, `LIGHTGBM`, `XGBOOST` with calibrated probabilities, held-out metrics, feature attribution, and leakage report.

- [ ] **Step 1: Write failing determinism and prohibited-feature tests**

```python
def test_quality_challengers_are_deterministic(fixture_quality_rows):
    first = train_quality_challengers(fixture_quality_rows.train, fixture_quality_rows.dev, seed=20260901)
    second = train_quality_challengers(fixture_quality_rows.train, fixture_quality_rows.dev, seed=20260901)
    assert [run.prediction_sha256 for run in first] == [run.prediction_sha256 for run in second]


def test_protected_and_identity_fields_are_not_features():
    assert set(QUALITY_FEATURES).isdisjoint({"user_id", "speaker_id", "provider_subject", "language", "province", "age", "gender", "reward_amount_cents"})
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/ml && python -m pytest tests/test_tabular.py -v`
Expected: import failure for `amazwi_ml.tabular`.

- [ ] **Step 3: Implement fixed features and models**

Quality features are exactly `duration_ms`, `silence_ratio`, `clipping_ratio`, `snr_db`, `sample_rate_hz`, `codec_code`, `duplicate_score`, and `peer_disagreement`. Mission features are aggregate-only counts/rates for coverage, model error, completion, and sponsor priority; no individual reward or identity feature is accepted.

Use `random_state=seed`, one thread, deterministic histogram settings, sorted columns, and fixed hyperparameters. Fit a sigmoid calibrator on dev predictions. Produce Brier, AUCPR, ECE, NDCG@10/MAP@10 as applicable, permutation importance, and protected-language slice gaps. Models can rank re-record review or mission proposals only; they cannot set eligibility or individual reward.

- [ ] **Step 4: Connect challengers to the tournament and budget ledger**

`train_tabular.py` requires a valid `46–54` phase reservation, immutable manifest hash, explicit task, seed, and output directory. It writes candidate evidence consumed by `evaluate_tabular_promotion`; it does not update production rules or aliases.

- [ ] **Step 5: Run tabular and tournament tests**

Run: `cd starter/ml && python -m pytest tests/test_tabular.py tests/test_tournament.py tests/test_budget.py -v`
Run: `cd starter/ml && python kaggle/train_tabular.py --help`
Expected: deterministic fixture hashes and explicit no-promotion evidence when thresholds fail.

- [ ] **Step 6: Commit**

```bash
git add starter/ml/amazwi_ml/tabular.py starter/ml/kaggle/train_tabular.py starter/ml/tests/test_tabular.py starter/ml/tests/fixtures/tabular_quality.csv starter/ml/tests/fixtures/tabular_missions.csv
git commit -m "ML: add LightGBM and XGBoost challengers"
```

---

### Task 14: Generate model cards, evidence hashes, and Stage 4–6 acceptance

**Files:**
- Create: `starter/ml/amazwi_ml/evidence.py`
- Create: `starter/ml/model_cards/README.md`
- Create: `starter/ml/tests/test_evidence.py`
- Create: `starter/backend/tests/test_council_data_e2e.py`
- Create: `starter/ml/STAGE_4_6_EVIDENCE.md`
- Modify: `05_amazwi/P0.md`
- Modify: `05_amazwi/BUILD_LOG.md`
- Modify: `HANDOVER_SBU.md`
- Modify: `CLAUDE.md`

**Interfaces:**
- Produces: `generate_model_card(run: EvidenceRun) -> str`.
- Produces: `write_evidence_index(paths: Sequence[Path], output: Path) -> str`.
- Verifies: peer resolution → reward → outbox → Council → approved export → immutable manifest → metrics → tournament decision → model card.

- [ ] **Step 1: Write failing claim-honesty and evidence-index tests**

```python
def test_failed_promotion_generates_no_improvement_card(no_promotion_run):
    card = generate_model_card(no_promotion_run)
    assert "Promotion decision: NOT PROMOTED" in card
    assert "No held-out improvement claim is made." in card
    assert "improved model deployed" not in card.lower()


def test_evidence_index_hashes_every_declared_artefact(tmp_path, evidence_files):
    digest = write_evidence_index(evidence_files, tmp_path / "evidence-index.json")
    index = json.loads((tmp_path / "evidence-index.json").read_text())
    assert digest == sha256_file(tmp_path / "evidence-index.json")
    assert sorted(index["artefacts"]) == sorted(str(p) for p in evidence_files)
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/ml && python -m pytest tests/test_evidence.py -v`
Expected: import failure for `amazwi_ml.evidence`.

- [ ] **Step 3: Generate cards from evidence, never from handwritten winner claims**

Every card contains: model/candidate ID, intended and prohibited uses, languages/domains, immutable dataset/evaluation manifest hashes, source classes, licence/restriction summary, speaker split policy, baseline, acceptance policy, WER/CER/embedded-span or tabular metrics, slice results, calibration, ablations, seed, config/checkpoint/prediction hashes, budget entry, promotion decision/reasons, limitations, consent/revocation statement, and exact run status. Missing required evidence raises `IncompleteEvidence` and emits no card.

- [ ] **Step 4: Write the full failing backend acceptance test**

```python
def test_resolver_to_council_and_approved_export(db_session, governed_fixture):
    decision = governed_fixture.resolve_with_two_peers(training_consent=True)
    assert governed_fixture.reward_count() == 1
    event = governed_fixture.single_outbox_event()
    governed_fixture.run_council(event)
    assert governed_fixture.council_codes()["DATA_STEWARD"] == "TRAINING_READY"
    export = governed_fixture.draft_and_approve_export()
    assert export.state.value == "APPROVED"
    assert export.manifest_sha256 == governed_fixture.rebuilt_manifest_sha256()
    assert governed_fixture.reward_count() == 1
```

Add paired cases for Council disabled, one specialist failed, training consent absent, consent revoked after draft, external preflight absent, and worker retry. Every case preserves peer decision and reward.

- [ ] **Step 5: Run complete Stage 4–6 verification**

Run: `cd starter/backend && python -m pytest tests/test_council_data_e2e.py -v`
Run: `cd starter/backend && python -m pytest -q`
Run: `cd starter/ml && python -m pytest -q`
Run migration roundtrip twice against `AMAZWI_TEST_DATABASE_URL` when configured.
Run: `cd starter/ml && python kaggle/download_external.py --dataset swivuriso --task ASR_TRAINING --dry-run`
Expected: backend and ML suites pass; the ungated download exits 2 with `PREFLIGHT_REQUIRED`; no network transfer starts.

- [ ] **Step 6: Record exact evidence and stop-state distinctions**

`STAGE_4_6_EVIDENCE.md` records command, UTC timestamp, exit code, test count, PostgreSQL version, manifest and registry hashes, Council enabled/disabled/failure results, export approval actor class, external preflight status, Kaggle budget reserved/completed totals, candidate IDs, metric report hashes, promotion decisions, model-card paths, and every action not run. It must state `No external dataset downloaded.` unless approved preflight and download evidence exist. It must state `No Kaggle GPU run performed.` unless a real ledger-backed run exists. It must state `No model alias changed.` and `No deployment performed.`

Update truth documents with exact implemented, locally verified, externally verified, GPU-run, promoted, and not-run states. Do not collapse them into one completion label.

- [ ] **Step 7: Commit without external execution or deployment**

```bash
git add starter/ml/amazwi_ml/evidence.py starter/ml/model_cards/README.md starter/ml/tests/test_evidence.py starter/backend/tests/test_council_data_e2e.py starter/ml/STAGE_4_6_EVIDENCE.md 05_amazwi/P0.md 05_amazwi/BUILD_LOG.md HANDOVER_SBU.md CLAUDE.md
git commit -m "Docs: record Council data and model evidence"
```

Do not run `git push`, `vercel`, `kaggle kernels push`, an external download command without approved evidence, a real payment command, a campaign launch command, or a model-alias update command.

---

## Broader Verification Matrix

| Requirement | Required command/evidence |
|---|---|
| Resolver and outbox are one transaction | `python -m pytest tests/test_resolver_outbox.py -v`; reward-failure rollback leaves zero decision/event rows |
| `SKIP LOCKED` prevents duplicate work | `python -m pytest tests/test_outbox_concurrency.py -v` against PostgreSQL 16 |
| Worker crash and retry are idempotent | `python -m pytest tests/test_outbox.py tests/test_council_worker.py -v` |
| AI-disabled isolation | `python -m pytest tests/test_ai_disabled_e2e.py -v` |
| Specialists cannot mutate authority | `python -m pytest tests/test_council.py tests/test_ledger_invariants.py -v` |
| Licence/consent/revocation firewall | `python -m pytest tests/test_datasets.py tests/test_dataset_export_concurrency.py -v` |
| Canonical manifest reproducibility | run `tests/test_manifest.py` twice and compare SHA-256 |
| Speaker-safe split | `python -m pytest tests/test_splits.py -v`; no `(source_id, speaker_id)` spans splits |
| No ungated external download | refused dry-run exits 2 with `PREFLIGHT_REQUIRED` before network import |
| WER/CER/embedded-span correctness | `python -m pytest tests/test_metrics.py -v` with exact fixture values |
| Deterministic promotion decision | run `tests/test_tournament.py` twice; decision JSON hashes match |
| 60-hour aggregate and 30-hour account caps | `python -m pytest tests/test_budget.py -v` |
| LightGBM/XGBoost evidence and leakage audit | `python -m pytest tests/test_tabular.py -v` |
| Honest cards and artefact hashes | `python -m pytest tests/test_evidence.py -v` |
| Full Stage 4–6 path | `python -m pytest tests/test_council_data_e2e.py -v` plus complete backend and ML suites |

## Stop Rules

- Stop Stage 4 if the outbox event can commit without its peer decision/reward transaction, if rollback leaves an event, if two workers claim the same row, or if AI-disabled mode breaks the peer/reward/result path.
- Stop Stage 4 if any specialist can write an authority-plane table, receives unrestricted raw audio unnecessarily, or loses successful sibling output when another specialist fails.
- Stop Stage 5 if an export can include revoked/missing model-development consent, an unapproved external source, a non-final contribution, a public/unavailable object, or a mutable approved manifest hash.
- Stop Stage 5 if canonical rebuilds differ, any speaker crosses train/dev/test, source classes are silently merged, or an external download starts before approved preflight validation.
- Stop Stage 6 before GPU execution if immutable train/dev/test manifests, untouched evaluation manifests, exact candidate/config hashes, and a valid budget reservation do not exist.
- Stop a Kaggle run before its next phase when aggregate reserved/completed time would exceed 60 hours, either account would exceed 30 hours, or the phase allocation would exceed its declared range.
- Stop promotion if WER, CER, embedded-span, tabular, calibration, slice, hash, or same-evaluation-manifest gates fail. Keep the baseline active and generate a no-improvement card.
- Stop all external execution if licence terms, gated access terms, account terms, reviewer identity, exact revision, or permitted task is unclear. Synthetic fixtures and CPU tests may continue.
- Stop evidence publication if a card lacks required hashes/metrics or claims a model, dataset download, GPU run, deployment, alias change, or improvement that did not occur.
- Do not resume the paused Vercel deployment or push these stages as part of this plan.

## Final Acceptance Checklist

**Verified 2 Sep 2026** against the real suites, not against the filenames this
plan prescribes — actual coverage lives under different names in several cases
and that is noted per item. Evidence: `starter/backend` 168 passed (real
embedded PostgreSQL 16), `starter/ml` 40 passed. Cross-lane work — **pending
Sbu's review**.

- [x] A final peer resolution, eligibility decision, reward/campaign commitment, and `ContributionResolved` event commit or roll back together. — `tests/test_resolver.py` (three rollback tests now each assert zero surviving `OutboxEvent` rows) plus `tests/test_council_data_e2e.py::test_resolver_reward_outbox_and_retry_are_idempotent`. There is no `test_resolver_outbox.py`; this is the same behaviour under the existing filenames.
- [x] PostgreSQL workers use `FOR UPDATE SKIP LOCKED`, leases, deterministic retry delays, and audited recovery without duplicate claims. — `tests/test_outbox.py`: `test_skip_locked_never_hands_the_same_row_to_two_workers`, `test_an_unexpired_lease_is_not_reclaimed_but_an_expired_one_is`, `test_retry_delay_is_a_deterministic_capped_power_of_two`, `test_claim_order_is_deterministic_across_repeat_runs`, `test_admin_recovery_reopens_an_exhausted_event_and_writes_an_audit_row`.
- [x] Council outputs are versioned, canonically hashed, independently retryable, and idempotent per event/specialist/version. — `tests/test_council.py`: `test_canonical_hash_ignores_key_order_but_not_values`, `test_council_run_is_idempotent_per_event_specialist_and_version`, `test_input_hash_is_the_canonical_hash_of_the_redacted_facts_only`, `test_a_failing_specialist_does_not_lose_its_siblings_and_is_retryable`.
- [x] AI-disabled, pending, partial, failed, and exhausted states preserve peer truth, reward, wallet, receipt, and result polling. — `tests/test_council.py` covers all five status states plus `test_worker_failure_preserves_peer_truth_and_reward_state` and `test_worker_main_is_a_no_op_when_the_council_is_disabled`. Note honestly: `AI_COUNCIL_ENABLED` defaults to `false`, so the *entire* backend suite (peer, reward, wallet, receipt paths) already runs in AI-disabled mode; there is no separate `test_ai_disabled_e2e.py`.
- [x] Dataset source, licence, restrictions, allowed tasks, consent version, transforms, hashes, exclusions, approval, and revocation evidence are persisted. — `tests/test_datasets.py`: `test_dataset_source_persists_licence_restrictions_and_allowed_tasks`, `test_export_row_persists_consent_version_hash_and_exclusion_evidence`, `test_approval_and_revocation_evidence_records_actor_and_time`.
- [x] Only peer-decided, quality-acceptable, separately opted-in, unrevoked AMAZWI rows can enter an approved export. — `tests/test_datasets.py`: `test_non_final_contributions_cannot_be_exported`, `test_unavailable_or_quarantined_audio_cannot_be_exported`, `test_consent_revoked_before_drafting_blocks_the_row`, `test_round_consent_alone_is_not_model_development_consent`, `test_an_export_with_any_excluded_row_cannot_be_approved`.
- [x] External licensed, AMAZWI opted-in, evaluation-only, and synthetic fixture rows remain explicitly distinguished. — `tests/test_datasets.py`: `test_each_source_class_is_stored_distinctly_and_not_merged`, `test_a_non_amazwi_row_may_not_smuggle_in_a_contribution_link`.
- [x] Approved manifests are immutable and rebuild to byte-identical canonical JSON and SHA-256. — `ml/tests/test_manifest.py::test_manifest_rebuild_is_byte_identical` and `::test_manifest_nfc_and_immutable_write`; the DB-side immutability is `tests/test_datasets.py::test_an_approved_manifest_hash_is_immutable`.
- [x] No speaker appears in more than one train/dev/test split. — `ml/tests/test_splits.py::test_no_speaker_crosses_splits` and `::test_split_assignment_is_deterministic`.
- [x] The external registry blocks all downloads without exact approved preflight; Swivuriso synthesis uses are prohibited and AfriSwitch remains evaluation-only. — `ml/tests/test_external_preflight.py`: the parametrised `test_download_without_approved_preflight_is_refused` covers all six datasets, `test_swivuriso_rejects_synthesis_task`, and `test_registry_has_exact_policy_and_stable_hash` asserts `afriswitch.allowed_tasks == ("ASR_EVALUATION",)`.
- [x] Per-language WER/CER, embedded code-switch span error, domain/acoustic slices, baselines, ablations, and hashes are recorded. — `ml/tests/test_metrics.py`: `test_wer_cer_and_embedded_span_are_exact`, `test_evaluate_asr_reports_deterministic_slices`, `test_normalisation_is_unicode_and_punctuation_stable`.
- [x] Tournament ordering and promotion decisions are deterministic; failed thresholds retain the baseline. — `ml/tests/test_tournament.py`: `test_asr_candidate_is_blocked_when_only_wer_passes`, `test_equal_candidates_use_candidate_id_tie_break`, `test_asr_pass_requires_evaluation_manifest_and_hashes`.
- [x] Kaggle account and aggregate budget caps are enforced before execution, with allocation and actual time evidence. — `ml/tests/test_budget.py` (60-hour aggregate, 30-hour per account, deterministic reserve/complete), `ml/tests/test_budget_actual_hours.py`, `ml/tests/test_kaggle_scripts.py::test_budget_json_declares_locked_allocations`.
- [x] LightGBM and XGBoost challengers use fixed non-identity features, calibration, held-out evaluation, attribution, and protected-language leakage audits. — `ml/tests/test_tabular.py`. **Gap found and closed 2 Sep:** calibration (`brier`/`ece`/`aucpr`) and `feature_attribution` were computed in `amazwi_ml/tabular.py` but asserted nowhere, so a regression dropping them would have passed; added `test_challengers_report_calibration_and_protected_language_slices` and `test_challenger_attribution_and_metrics_are_deterministic`.
- [x] Model cards and evidence indexes are generated from artefacts and honestly report promotion or no improvement. — `ml/tests/test_evidence.py`: `test_failed_promotion_is_honest`, `test_incomplete_evidence_is_rejected`, `test_evidence_index_hashes_declared_files`.
- [ ] No external download, real Kaggle GPU run, model alias change, deployment, payment, or campaign launch is claimed without exact evidence. — **deliberately left unticked.** The mechanical half is tested (`ml/tests/test_kaggle_scripts.py::test_kaggle_entrypoints_expose_help_without_side_effects`, `test_evidence.py::test_incomplete_evidence_is_rejected`), but this item is a claim-review item about prose that reaches a reader, and a test cannot discharge it. It needs a human honesty pass over `STAGE_4_6_EVIDENCE.md`, the model cards, and `BUILD_LOG.md` — particularly against the Kaggle GPU runs recorded in commits `a792049`/`6f03710`/`d3bc55a`. Sbu's call.
