# AMAZWI — TECHNICAL CONTRACT
### Thin-slice architecture, states, data model, MoMo safety and verification

**Parent:** `00_MASTER_PLAN.md`
**Technical owner:** Sbu
**Frontend counterpart:** Lethabo

---

## 1. ARCHITECTURE

Use a modular monolith.

```text
React + TypeScript Mini App/PWA
        │
        ▼
FastAPI application
  identity / consent / cards / contributions
  assignments / verification / campaigns
  rewards / wallet / payments / receipts
        │
        ├── PostgreSQL — source of truth
        ├── private audio storage
        └── MoMoProvider
              ├── sandbox
              └── clearly-labelled demo provider
```

No Redis, Celery, WebSockets or ML services are required for the competition path. Add a dependency only when the running demo needs it.

The host bridge, heartbeat and CSP are adapters configured from the organiser's current Mini App specification. Do not hard-code an unverified public-doc assumption as platform truth.

---

## 2. API-FIRST TEAM CONTRACT

Sbu publishes request/response examples before backend implementation. Lethabo builds the client against those examples and does not read database internals.

Minimal endpoints:

```text
POST /sessions/demo
GET  /cards/next
POST /consents
POST /contributions
POST /contributions/{id}/audio
GET  /assignments/next
POST /assignments/{id}/answer
POST /assignments/{id}/referee
GET  /contributions/{id}/result
GET  /wallet
POST /wallet/cash-outs
GET  /receipts/{contribution_id}
POST /campaigns/{id}/fund
GET  /impact
POST /demo/reset
```

The demo reset endpoint is authenticated, deterministic and unavailable in production mode.

---

## 3. DATA MODEL

### Core records

```text
User
  id, provider_subject, declared_languages[], age_confirmed_at

ConsentGrant
  id, user_id, version, scope, granted_at, revoked_at

Card
  id, language, target, blocked_words[], accepted_answers[],
  distractors[], campaign_id, active

Campaign
  id, name, language, budget_cents, funded_cents, committed_cents,
  provider_reference, provider_mode

Contribution
  id, speaker_id, card_id, declared_language, state,
  audio_key, duration_ms, quality_json, created_at, expires_at

Assignment
  id, contribution_id, verifier_id, mode,
  answer_text, answer_normalised, matched, violation_vote,
  answered_at

EligibilityDecision
  contribution_id, understood, corpus_eligible, reason,
  consent_version, decided_at

RewardEvent
  id, contribution_id, user_id, type, amount_cents,
  idempotency_key, created_at

PaymentAttempt
  id, user_id, amount_cents, provider_mode, provider_reference,
  state, requested_at, resolved_at

Receipt
  contribution_id, semantic_label, decision_evidence_json,
  reward_rule_version, consent_version, payment_state

AuditEvent
  id, actor_id, action, entity_type, entity_id, metadata, created_at
```

The semantic label is stored separately from any future transcript. In the competition build there is no transcript field populated by the game.

---

## 4. CONTRIBUTION AND PAYMENT STATES

Keep contribution, reward and provider settlement separate.

### Contribution

```text
DRAFT
  → RECORDED
  → QUALITY_PASSED
  → OPEN
  → UNDERSTOOD | REVIEW_REQUIRED | VOIDED | EXPIRED
  → CORPUS_ELIGIBLE | UNVALIDATED
```

### Reward

```text
NONE → CREDITED → RESERVED_FOR_CASH_OUT → SETTLED | RELEASED
```

### Payment attempt

```text
CREATED → SUBMITTED → PENDING → PAID | FAILED
```

An HTTP `202` means submitted, not paid. Only a provider callback or reconciliation result can set `PAID`.

---

## 5. ASSIGNMENT AND RESOLUTION

### Assignment invariants

- the speaker cannot verify their own contribution;
- the same verifier cannot receive the same contribution twice;
- exactly two completed proficient-verifier assignments are required for automatic resolution;
- learner MCQ assignments never count toward that two;
- revoked or expired audio cannot be assigned;
- assignment is random within the eligible closed cohort for the language.

A PostgreSQL `CHECK` cannot enforce no-self-assignment across another table. Enforce it in the assignment transaction and back it with a trigger or relational constraint where appropriate.

### Resolver

```text
if fewer than 2 proficient answers:
    remain OPEN until expiry
elif both violation votes are true:
    VOIDED
elif violation votes disagree:
    REVIEW_REQUIRED
elif both answers match accepted_answers:
    UNDERSTOOD
    if audio quality passes and required consent is active:
        CORPUS_ELIGIBLE
        credit speaker reward once
    else:
        UNVALIDATED
else:
    UNVALIDATED
```

Resolution runs in a database transaction and is safe to call repeatedly.

---

## 6. ANSWER MATCHING

Competition normalisation:

```text
NFC Unicode normalisation
lowercase
trim
collapse whitespace and hyphens
exact match against per-card accepted_answers
```

No generic noun-class stripping. No broad edit-distance threshold. Explicit native-reviewed aliases handle known forms and typos for the hero deck.

The raw answer, normalised answer and match rule version are stored for audit.

---

## 7. AUDIO

### Client checks

- microphone permission;
- supported recording format;
- duration within the card rule;
- non-silence threshold;
- clipping warning;
- playback before submission when possible.

These are physical quality checks, not language or intelligibility models.

### Upload

Choose the simplest reliable path after testing on the event network:

- direct multipart upload through FastAPI for fewer moving parts; or
- a short-lived presigned upload if direct upload is unreliable.

Audio is private, encrypted by the storage provider and exposed only through short-lived assigned-verifier playback URLs.

No public bucket, public archive URL or precise location metadata.

---

## 8. REWARD LEDGER

Use immutable signed events in integer cents. A reward row is not updated into a payment row.

Required database guarantees:

- unique reward on `(contribution_id, user_id, type)`;
- unique provider request reference;
- campaign committed amount changes in the same transaction as reward credit;
- available balance includes only posted credits minus reserved/settled debits;
- pending, failed and paid provider attempts do not get summed as equivalent money;
- a callback may arrive more than once without changing value twice.

Minimum property tests run against the demo provider only:

1. resolving the same contribution repeatedly creates one reward;
2. submitting the same cash-out repeatedly creates one reservation;
3. duplicate callbacks do not duplicate settlement;
4. a failed cash-out releases the reservation;
5. campaign commitments never exceed the funded budget;
6. revocation never deletes financial history.

Automated tests never call the MoMo sandbox.

---

## 9. MOMO PROVIDER

```text
MoMoProvider
  fund_campaign(...)
  request_cash_out(...)
  get_status(...)
  verify_callback(...)
```

Provider modes are visible in both API data and UI:

- `SANDBOX_COLLECTIONS`
- `SANDBOX_DISBURSEMENT`
- `DEMO_PROVIDER`
- `PRODUCTION` — not used at the event

Persist the idempotency/reference ID before the external call. Store the request and response metadata without secrets. Poll unresolved attempts and accept callbacks; either path calls the same idempotent state transition.

Actual South African API availability, currency, minimum amount and fee are external dependencies. The adapter prevents those unknowns from breaking the rest of the product.

---

## 10. CONSENT ENFORCEMENT

Required scopes are checked server-side at:

- contribution creation;
- audio playback assignment;
- eligibility decision;
- any export or research use.

Revocation:

- sets `revoked_at` on the relevant grants;
- blocks new assignments and export;
- removes or quarantines the audio according to the retention policy;
- preserves a non-audio audit tombstone and financial records.

Public audio sharing is not implemented. Voice is not used for authentication or uniqueness.

---

## 11. SECURITY AND PRIVACY

- no identity-document storage;
- no voice biometrics;
- no exact location;
- secrets only in server environment configuration;
- signed/short-lived audio access;
- rate limits on contribution, assignment and payment endpoints;
- structured logs exclude audio URLs, bearer tokens and phone numbers;
- provider callback authentication follows the event specification;
- all demo/provider substitutions are labelled.

---

## 12. RELIABILITY

Do not pretend FastAPI background tasks are durable. The competition path uses synchronous decisions where bounded, explicit status polling and an authenticated demo/admin action for deterministic recovery.

Every screen needs one human error state for:

- microphone denied;
- unsupported browser recording;
- network failure during upload;
- no verifier clips available;
- contribution waiting/expired;
- consent revoked;
- campaign empty;
- sandbox/demo provider unavailable;
- cash-out failed;
- duplicate action safely ignored.

---

## 13. TECHNICAL DEMO PROOF

The technical demonstration is complete when the team can show:

1. a real cross-device recording;
2. two stored independent verifier events;
3. an automatic eligibility decision;
4. one reward despite repeated resolver calls;
5. a funded campaign balance decrementing once;
6. a provider attempt whose state is not overstated;
7. a receipt rendered from database events;
8. a revoked clip excluded from assignment/export;
9. deterministic reset;
10. no ML or service named on a slide that is not running.
