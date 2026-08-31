# AMAZWI — ONE-RUN BUILD PLAN
### Priority gates, ownership, integration contract and kill rules

**Parent:** `00_MASTER_PLAN.md`
**No timeline:** progress is controlled by working exit conditions, not optimistic clock estimates.

---

## 1. RULES BEFORE THE BUILD

The public terms say submissions must be original and created during the hackathon unless organisers approve otherwise. Open-source libraries are permitted.

The team has chosen not to seek written answers before the event. The following therefore remain unknown and must not be assumed; confirm them from official on-site briefing or authorised mentors before depending on them:

- whether non-code planning, cards, design and pitch preparation are allowed;
- whether a generic public starter is allowed;
- whether the repository must be empty at submission;
- which Mini App bridge/CSP/heartbeat specification applies;
- Collections and South African Disbursement sandbox availability;
- submission close and pitch start;
- the scope of the IP clause's “exclusive” marketing licence.

No written approval will be sought before the event. Therefore **no product-specific application code and no Gate A–H implementation begins before the event opens**. The invitation also says all competition work must be completed on-site by the two-person team without outside assistance; a teammate cannot waive that condition by recording an internal "accepted risk."

Pre-event research, plans, reviewed language content, design explorations and mockups are **preparation/reference only**. They are not competition implementation, running-product evidence or submission artifacts. At the event, Sbu and Lethabo must create the competition implementation themselves, on-site, and may use only material the organisers' rules permit. Keep the existing history intact and disclose the preparation boundary honestly; never relabel pre-event work as event-built.

---

## 2. CONFIRMED OWNERSHIP

### Sbu — Platform, MoMo and Trust

Owns:

- FastAPI and API examples;
- PostgreSQL schema/migrations;
- contribution, eligibility, reward and payment states;
- assignment and resolver logic;
- consent enforcement and audit events;
- campaign funding, MoMo adapters, idempotency and reconciliation;
- deployment and backend reliability;
- isiZulu cards and copy;
- technical proof and money/security Q&A.

Sbu has final say on money, data integrity and deployment safety.

### Lethabo — Product, Experience and Demo

Owns:

- React app and frontend state;
- design tokens and screen implementation;
- recorder, learner and verifier interactions;
- wallet, receipt, Impact Map and accessibility;
- guest path, error copy and demo reset UI;
- fallback recording and pitch deck;
- Setswana cards and copy;
- opening, live narration, close and product/culture Q&A.

Lethabo has final say on scope and user experience.

### Shared

- agree JSON examples before code;
- never edit the same file simultaneously;
- both can run the full demo;
- both know the exact sandbox/demo-provider disclosure;
- Sbu breaks integrity ties; Lethabo breaks experience ties;
- either may call a scope cut when a gate cannot close.

---

## 3. CONTENT CONTRACT

Build eight hero cards per language first.

Each card requires:

```text
target
blocked_words[4]
accepted_answers[]
distractors[3]
language
campaign_or_deck
```

Sbu authors and approves isiZulu. Lethabo authors and approves Setswana. Cross-read aloud for playability, but the first-language owner has final linguistic sign-off.

No placeholder card reaches the pitch. No illustration appears on a listener screen if it leaks the target.

---

## 4. BUILD GATES

Every gate leaves one integrated, demoable product. Do not begin the next gate while the current exit condition is false.

### Gate A — running shell

**Sbu:** API health, database connection, migrations, deployment, provider configuration.
**Lethabo:** routes, design tokens, API client, Mini App/browser-mode label.

**Exit:** the same commit runs on both laptops, deploys, resets and loads on the target phones.

### Gate B — deterministic golden path

**Sbu:** seeded campaign, user, cards, contribution, two assignments, reward and receipt endpoints.
**Lethabo:** clickable end-to-end screens with loading, empty and error states.

**Exit:** one tap sequence reaches a receipt from deterministic seed data, and reset restores it.

**Seed data is pre-resolved, not resolver-produced.** Gate B's contribution/assignments/receipt rows are inserted already in their final state (`CORPUS_ELIGIBLE`, `RewardEvent` credited) by a seed script — the real resolver from Gate E does not exist yet and Gate B does not call it. This is a fixture, not a shortcut through the state machine; Gate E later replaces the seed path with the live one end to end.

### Gate C — identity and consent

**Sbu:** session adapter, versioned consent grants, server-side enforcement and revocation.
**Lethabo:** adult gate, language selection, consent UX and browser-demo disclosure.

**Exit:** a user without required consent cannot create a contribution; revoked audio cannot be assigned.

### Gate D — real recording

**Sbu:** contribution creation, upload, private playback URL and persisted physical quality metrics.
**Lethabo:** permission, card, timer, real waveform, record/retry and upload UX.

**Exit:** audio recorded on one phone plays on another after refresh.

### Gate E — real verification

**Sbu:** assignment transaction, no-self-assignment, conservative answer matching, two-verifier resolver, `VOIDED`, `REVIEW_REQUIRED`, `EXPIRED` and `UNVALIDATED`.
**Lethabo:** free-text verifier flow, answer lock, reveal, referee tap and honest result states.

**Exit:** two independent devices make one real clip `CORPUS_ELIGIBLE`; MCQ cannot do so.

### Gate F — money and receipt

**Sbu:** campaign budget, immutable reward event, available balance, cash-out reservation, provider adapter, callback/polling reconciliation and retry tests.
**Lethabo:** wallet states, credited-vs-paid copy, Voice Value Receipt and provider-mode label.

**Exit:** repeated resolver/payment actions cannot create extra money and the UI never overstates settlement.

### Gate G — fintech proof

**Sbu:** Collections sandbox integration if confirmed; otherwise labelled seeded funding. One sandbox call path only.
**Lethabo:** “Fund a language mission” screen and compact funds-remaining view.

**Exit:** the funding leg and reward commitment are traceable through one campaign. Every simulated leg is disclosed.

### Gate H — pitch hardening

**Sbu:** consent-export test, log sanitisation, rate limits, deployment recovery and backend demo script.
**Lethabo:** mobile pass, guest MCQ mode if safe, Impact Map, failure copy, deck screenshots and fallback video.

**Exit:** judge-only demo works repeatedly from reset; fallback recording exists on both laptops and a phone.

---

## 5. P0 ACCEPTANCE TESTS

- no consent → no contribution;
- revoked consent → no playback assignment or export;
- one proficient verifier → no automatic resolution;
- learner MCQ → `PLAYED`, never `UNDERSTOOD`;
- two accepted free-text answers → `UNDERSTOOD`;
- two violation votes → `VOIDED`;
- split violation vote → `REVIEW_REQUIRED`;
- expired without two verifiers → `UNVALIDATED`, no export;
- duplicate resolver calls → one reward;
- duplicate callback → one settlement;
- payment failure → reservation released;
- provider `202` → submitted/pending, not paid;
- deterministic reset → known demo state;
- direct audio URL without assignment → denied.

Automated payment tests always use the demo provider. Maintain a manual sandbox-call budget and reserve a clean credential/user for the pitch where organisers permit it.

---

## 6. KILL RULES

Cut in this order:

1. room-wide play; use judge-only golden path;
2. league;
3. gold/honeypot checks;
4. buyer dashboard beyond funds remaining and eligible seconds;
5. Impact Map animation; keep a static aggregate SVG;
6. real Disbursement; keep labelled demo provider;
7. real Collections only if unavailable; keep labelled funded seed.

Never cut:

- purpose consent;
- real recording;
- two proficient verification events;
- conservative matching;
- idempotent reward ledger;
- honest provider state;
- Voice Value Receipt;
- deterministic reset and fallback demo.

Do not revive story chain, public archive, IRT/Elo, ASR training, active learning, paid listeners or additional languages during the competition.

---

## 7. DEMO MODES

### Primary — judge-only

One speaker phone, two proficient-verifier phones, one display. This is the product proof and must work without the room.

### Optional — room guest

Audience scans into MCQ learner mode. It awards XP/popularity only. It cannot make a contribution corpus-eligible or trigger cash.

### Seeded recovery

Deterministic local/demo-provider data fills only the unavailable external leg. The speaker recording and stored evidence remain real where possible. State the substitution aloud.

---

## 8. HANDOVER PROTOCOL

At each integration boundary, leave:

- the exact commit/hash or working-tree note;
- endpoints and example payloads changed;
- environment variables added without secret values;
- one success path and one known failure;
- the next owner and next exit condition.

Lethabo's incoming notes remain in `../../HANDOVER_SBU.md`. Sbu's reciprocal decisions and implementation handback live in `../../HANDOVER_LETHABO.md`.
