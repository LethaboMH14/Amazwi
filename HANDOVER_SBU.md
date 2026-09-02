# HANDOVER → SBU

## 🔴 PING — 03 Sep ~01:30 · RECORDING HAD NEVER WORKED · and one money trap that needs your call

**Read the money trap first.**

### 🔴 DO NOT wire MoMo Collections to the redeem path

You landed live Collections (`app/momo.py`, `5ac45cf`) — good work, and the WAF/empty-body diagnosis is a genuinely nice catch. It is currently called from nowhere.

I built `POST /rewards/{key}/redeem` in the same window: it reserves against the ledger, then calls the payment provider adapter. Pointing that at your `MomoClient` would take five minutes. **I deliberately did not, and neither should you:**

> **Collections takes money IN. Redeeming a contributor's credit pays money OUT — that is Disbursement.** Wiring `request_to_pay` into the redeem path would *charge the person you meant to pay*.

Where Collections genuinely belongs is **Gate G — funding a mission**, where a sponsor pays in. That is your call per `05_BUILD.md` §2, so I flagged it rather than guessed.

### ✅ FIXED — recording had never worked, for anyone

`api/client.ts` sent `duration_ms: 0` on finalise while the recorder computed the real elapsed time and threw it away. `app/contributions.py` rejects anything outside `500..20000ms`, so **every recording ever made through the UI failed at the last step**. The upload itself succeeded, so the symptom was a silently orphaned `.pending` file rather than a visible error — bytes on disk, rename to `.bin` never happened, no verifier could ever play the clip.

Proven at the API boundary against the running backend, both directions:

| finalise body | result |
|---|---|
| `duration_ms: 0` (what shipped) | **HTTP 422 `AUDIO_DURATION_INVALID`** |
| real duration | **HTTP 200, state `AVAILABLE`** |

Same commit also fixes the phone path hardcoding 1000ms, and `codec` hardcoded to `"webm"`. The missing test is added — nothing asserted the request body, which is exactly why this shipped.

### 🔴 MY OWN BUG, found and fixed — the seeded audio did not exist

`seed_activity.py` (mine) wrote `AudioObject` rows with `sha256 = "0"*64` and **never wrote a byte**. 27 audio rows, 2 files on disk. A row asserting something exists when it does not — the other half of "the other person cannot hear it". Now writes a real deterministic WAV per clip, with hash and length measured from what was actually written. 25/25 verified.

### ⚠️ The test suite wipes the demo database

`tests/conftest.py` drops the public schema **per test**. If the demo backend points at `AMAZWI_TEST_DATABASE_URL`, running `pytest` destroys every seeded card, user and reward — surfacing as a confusing `401` from every authenticated route. Split into `postgres` (tests) and `amazwi_demo` (demo). Steps in `starter/backend/DEMO_RUNBOOK.md`.

### Architecture check is now runnable

`uvx archy score .` on the backend: **0.686**, acyclicity **1.000**, 80 modules / 182 edges. It found a real import cycle (`app.main` ↔ `app.routes.arcade`) that was mine; fixed with the `app/providers.py` leaf module. Worth keeping in CI.

### For your review — new, cross-lane

- **`/arcade`** publishes contributor display names on a leaderboard. Privacy posture; scoped to the caller's own language cohort, never a provider subject. Your call.
- **`/rewards` thresholds** (R5 / R10 / R20) are placeholders chosen to be obviously round rather than researched. API returns `thresholds_are_proposed: true`; the screen says so on the page.
- **`app/llm.py`** — Featherless/AIML client for the advisory Council. Three switches must all be on before a byte leaves the machine. Featherless serves text, TTS and private HF models but **not ASR**, so nothing routed through it can listen to a contribution.

---


> **Sbu response incorporated 2026-08-31.** The role split was reversed and the product decisions were accepted/reconciled. Read [`HANDOVER_LETHABO.md`](HANDOVER_LETHABO.md) and [`05_amazwi/plan/00_MASTER_PLAN.md`](05_amazwi/plan/00_MASTER_PLAN.md) before acting on older instructions below. This file remains Lethabo's incoming context and historical reasoning; where it conflicts with the canonical plan, the canonical plan wins.

---

## 🔴 PING — 02 Sep ~13:45 · YOUR CRITICAL PATH IS STILL THE BLOCKER. Everything else is ready for it.

**Read this one first.** You named the seed script as the real demo blocker and you were right. Since then the frontend side has been closed out, so the *only* thing between us and a demo that looks finished is your four steps. Nothing here is asking you to redo work — it is telling you exactly what state you are dropping into.

### What changed on the frontend while you were on the seed script

1. **The craft layer finally landed in the real app.** This is the big one. Three separate gaps were closed:
   - **Archivo and Instrument Serif were never actually loaded.** `tokens.css` declared `--font: 'Archivo'` but no `<link>` or `@font-face` existed anywhere in `starter/frontend`, so every screen had been rendering in the OS default font since the app was created. Archivo is a *variable* font with a width axis, so `font-stretch: 125%` on the display type had been silently doing nothing.
   - **`signal-flow.css` had no craft layer at all** — it was `.route` layout, 44px targets, focus outlines and contrast fixes. Pure a11y remediation, zero visual design.
   - **`HomeRoute` was a debug shell.** Now built to the v2 grammar (`04_assets/mockups_v2/README.md`): overlapping-listeners signature device, hairline meta strip, asymmetric circle+type CTA, editorial serif accent.
   - Gate A diagnostics (host mode, backend health, theme switch) are all **still visible** — moved to a footer, not removed. That evidence stays.

2. **The craft layer applies to every route automatically.** You do not need to style anything. `/verify` already picks up the display type, eyebrow and ground with zero per-route work.

3. **Which is exactly why your seed script is now the whole game.** The routes look sparse because they render *empty states*, not because they are unstyled. `/verify` currently says **"Loading the next peer card… A contribution is required."** That is a data problem with a finished UI behind it. Seed real content and the screens fill in.

4. **Figma design system consolidated** (Lethabo upgraded to Professional): four near-identical `Theme A/B/C/D` collections merged into one `AMAZWI Theme` collection with five real modes; 19 component paints rebound; legacy collections deleted; new **Theme Modes** page (`16:2`) proves all four components render correctly across all five grounds with brand colour invariant. Detail in `04_assets/FIGMA.md`.

### Your four steps, unchanged and still the critical path

1. `python -m app.seed_demo` against real local Postgres. Confirm it succeeds **and that re-running it is a true no-op** (you built it idempotent; prove it).
2. Verify the CHECK constraints actually hold against the loaded card content (`blocked_words` exactly 4, `accepted_answers` ≥ 2, `distractors` exactly 3). You traced these by hand — "should" is not "does".
3. LAN reachability: `uvicorn --host 0.0.0.0`, frontend `vite --host`, `API_PROXY_TARGET` pointed at the backend laptop's LAN IP, so the phone (speaker) and second laptop (verifier) can reach it.
4. **Run the real golden path end to end against seeded data** — record on the phone → two verifiers on the laptops → resolver → reward → receipt. This has never been run against real seeded content; the tests use fixtures, not this.

### Two things worth knowing before you run the suites

- **One accessibility test fails and it is NOT a regression.** `e2e/accessibility.spec.ts` → "ops reaches every interactive control by Tab" at `chromium-390`. It counts 0 focusable controls on `/ops`, though the captured page snapshot shows a "Review mission" button present. I verified this by `git stash`-ing the craft-layer changes and re-running on the clean baseline: **it fails identically there.** Pre-existing, most likely a race between the stub resolving and the count. 194 of 195 pass.
- **Playwright was in `package.json` but never installed** in the main working tree, so those gates could not be run there at all until I ran `npm install` + `playwright install chromium`. If you get "unknown command 'test'" from `npm run test:a11y`, that is what it is — and note it exits **0** on that failure, so check the output, not the exit code.

### Untouched, still yours

Money/legal/deployment-safety calls, per `05_BUILD.md` §2. Specifically still open for you: the `/impact` endpoint being deliberately unauthenticated, whether a mission must always attach to a funded campaign, and **the Kaggle honesty item** — `starter/ml/runs/README.md` and `kaggle/budget.json` both still state no run happened while real GPU hours were spent. Your own review commit flagged that independently; it is Plan 02's one unticked acceptance item and it is a claim-calibration judgement, not something a test settles.

---

## ⚠️ FOR YOUR REVIEW — 02 Sep · Plan 02 acceptance checklist verified; one item is yours

Cross-lane backend/ML work, **pending your review**. Plan 02's Final Acceptance
Checklist has been verified item-by-item against the tests that actually exist
(not the filenames the plan prescribes — substitutions are documented inline in
the plan doc). 15 of 16 items are ticked with named proving tests. Backend 168
passed against real embedded PostgreSQL 16 before merging `main`, and 210 passed
after two merges — the growth is the parallel agents' Tasks 7–10 tests arriving,
**not** coverage I wrote (mine is three tests: one backend, two ML). ML 40 passed
before and after.

Four real bugs were found and fixed in the process, all detailed in
`05_amazwi/BUILD_LOG.md`'s newest entry: a `None + 1` crash that made the
Council's `PARTIAL` state unreachable, `AI_COUNCIL_MAX_ATTEMPTS` being dead
config that left the API's `FAILED` branch unreachable, rollback tests that
never asserted the outbox event was gone, and untested calibration/attribution
evidence in the tabular challengers.

**The one open item is genuinely yours:** checklist item 16 — no external
download, GPU run, alias change, deployment, payment or campaign launch claimed
without exact evidence. It is a claim-calibration judgement over prose a reader
sees (`STAGE_4_6_EVIDENCE.md`, the model cards, `BUILD_LOG.md`) against the real
Kaggle runs in `a792049`/`6f03710`/`d3bc55a`. No test can discharge it, so it is
deliberately left unticked rather than ticked optimistically. Nothing touching
Kaggle, Vercel, money or campaigns was changed.

> **Update after merging Sbu's review (same day).** Sbu's review below
> independently found the concrete instance of exactly this: `runs/README.md`
> and `kaggle/budget.json` both still say no run happened while real GPU hours
> were spent. That is item 16's failure mode, found by a human reading the prose
> — which is the argument for having left it unticked rather than ticking it on
> the strength of the passing mechanical tests. It still needs reconciling
> before any evidence pack or model card is generated.

---

## ✅ REVIEWED 2 Sep by Sbu — mission authorisation (money-adjacent)

> **Verdict: ACCEPTED**, with one ruling and one pitch-wording correction. Full review in [`HANDOVER_LETHABO.md`](HANDOVER_LETHABO.md) § "2 SEP — SBU'S REVIEW OF THE CROSS-LANE WORK".
>
> - **Ruling on `campaign_id`:** nullable is correct. Propose without a funded campaign; **never disburse** without one. Put the budget check in the disbursement path when it's built — do not retrofit `NOT NULL` onto the proposal table.
> - **Pitch wording:** this gate rests on header-only identity (`app/identity.py`, no signature) until Plan 04 Task 2 lands. Say *"human-in-the-loop by design — an automated actor structurally cannot authorise a mission."* Do **not** say *"only an authorised MTN operator can."*
> - Separately flagged, unrelated to this item: `runs/README.md` and `kaggle/budget.json` both still say no run happened, while real GPU hours were spent. Reconcile before any evidence pack or model card is generated. See the review section for the reasoning.

### Original request (kept for history) — 02 Sep ~06:00

Plan 03 Tasks 9+10 are built and green: mission proposals plus a **human-only** MTN Language Ops authorisation gate (`app/missions.py`, `app/routes/ops.py`, migration `e0f1a2b3c4d5`). Full detail in `05_amazwi/BUILD_LOG.md`'s newest entry.

**What I did NOT decide, because it is yours:**
- Authorisation records human intent only. It moves **no money** — no `funded_cents`/`committed_cents` write, no payment adapter call. Disbursing against an authorised mission is unbuilt and left to you.
- `mission_proposals.campaign_id` is a **nullable** FK to the existing `campaigns` table (reusing your model rather than inventing a parallel budget concept). Whether a mission must always be attached to a funded campaign is a money decision I deliberately did not make.

**What to attack when reviewing:** the gate is four layers — persisted `users.principal_kind` (CHECK-constrained), the `MTN_LANGUAGE_OPS` role, a keyword-only no-default exact confirmation echo, and a source-tree scan test asserting `authorise_mission` has exactly one caller (`routes/ops.py`). The test that matters most is `test_automated_actor_cannot_authorise_without_the_human_step`, which gives an automated actor the role *and* the correct confirmation text and still refuses it. Backend 135/135, frontend 65/65, typecheck clean.

---

## ✅ RULED ON 2 Sep by Sbu — Impact Map backend (`GET /impact`)

> **Both questions answered, plus one thing you didn't ask about that I think is a real leak.**
>
> **1. Unauthenticated: APPROVED for the competition build.** The privacy work is genuinely sound — I read `impact.py` rather than the summary: `MIN_CELL_SIZE = 5` filters before banding, counts publish as bands, `model_gap_percent` is null rather than inferred from volume, `missions_completed` is 0 rather than approximated. That's the right instinct on all three.
>
> **But the exposure you should actually be worried about isn't personal data — it's commercial.** Each node publishes `campaign`. A public, unauthenticated endpoint therefore discloses which funding campaigns exist and roughly how much volume each has. That's sponsor-relations information, and no sponsor has agreed to it being public. For the demo with seeded data this is fine. Before any real sponsor's campaign is in there, either drop `campaign` from the public projection or put the endpoint behind identity.
>
> **2. 🔴 NEW — the bands are partially defeatable, and this one I'd fix.** `verified_total` is published **exactly**, and `coverage_percent` is `round(100 * verified_count / verified_total)`. Given both, you can solve backwards for `verified_count` within a narrow range. At demo-scale totals (a few hundred), one percentage point ≈ 2–3 clips, so a "5–9" band collapses to an almost-exact number — which defeats the point of banding, and by extension the k≥5 protection it's there to provide. Fix: band `coverage_percent` too, or round it hard (nearest 5%), or drop it and let the client derive a rough share from the band. Cheap fix, and it closes the hole properly.
>
> **3. Cell key deviation: APPROVED, and it was the right call.** Refusing to fabricate a province field you don't collect is exactly correct — `geography_available: false` plus "province-level coverage is not collected yet" is honest and costs nothing. **Do not add a province column for the competition.** A coarse geographic field on voice contributions is a POPIA consent question and a fresh consent-surface design, and it is not P0. Ship it null.

### Original request (kept for history) — 02 Sep

Plan 03 Tasks 7–8 (aggregate Coverage Constellation) are built and green: backend
121 passed against real PostgreSQL, frontend 74 passed + clean typecheck. Full
detail in `05_amazwi/BUILD_LOG.md` [02 Sep ~05:40]. Two things in your lane that
I built to spec but should not be the one to finalise:

1. **`GET /impact` is unauthenticated.** Rationale: every field has already passed
   a ≥5-contribution minimum-cell-size suppression in `app/impact.py`, counts are
   published as bands not exact values, and no user id, contribution id,
   coordinate, audio key or transcript is present (asserted against the raw
   response text in `tests/test_impact_api.py`). That is still a data-exposure
   judgement — confirm or overrule it.
2. **The cell key deviates from the plan.** The plan specifies
   `(language, province, domain)`. `app/models.py` has no geographic column and no
   domain vocabulary anywhere, so rather than fabricate a location field I
   aggregate **declared language × funding campaign**, leave `province_code` null,
   set `geography_available: false`, and have the UI say "province-level coverage
   is not collected yet". `model_gap_percent` is null ("Model evidence
   unavailable") and `missions_completed` is 0 — neither is inferred. If you want
   real geography, that needs a consented, coarse province column and a migration,
   which is your decision, not mine.

---

## ✅ CURRENT — 01 Sep · implementation programme approved; autonomous execution starting

### Implementation update — 01 Sep

Sbu's lane has now shipped the first executable frontend contribution slice and
the first Council data-plane slice. `ae606d4` adds the typed API client and
scoped consent UI; `e18f1cc` adds memory-only recording, SHA-256 upload
integrity and peer-verification UI; `5e7c245` adds PostgreSQL outbox/Council
models and migration `c8d9e0f1a2b3`. The resolver now enqueues a deduplicated
`ContributionResolved` event in the same transaction as the eligibility and
reward decision, including recovery for previously-resolved rows.

The next review gate is real PostgreSQL migration/concurrency verification,
then an outbox worker with `FOR UPDATE SKIP LOCKED`. The frontend still needs a
dedicated result route and browser-level MediaRecorder tests. No Council output
may alter peer truth, consent, audio retention, rewards or model aliases.

Outbox leasing primitives are now implemented in `app/outbox.py` with
`claim_events`, ownership-checked completion, exponential retry backoff capped
at five minutes, and audited administrative release via
`scripts/recover_outbox.py`. These remain pending real PostgreSQL concurrency
verification before being called production-ready.

The deterministic advisory Council contract layer is now shipped in
`app/council.py` (`d779217`): versioned Data Steward, Sound Sentinel, Language
Scout and Explainer baselines, canonical input hashing, idempotent output
persistence and explicit authority isolation. This is a rules baseline, not
an AI performance claim. The worker process, read-only Council status route,
dataset provenance/export schema and ML manifest/evidence package remain
unfinished and require focused tests before acceptance.

Dataset provenance schema is now drafted in migration `d9e0f1a2b3c4` with
source classes, licence/review metadata, export lifecycle state, manifest
fields and a database check preventing external rows from carrying AMAZWI
contribution IDs (or vice versa). Export candidate/approval services,
immutability triggers and PostgreSQL schema tests are still required.

The provenance firewall service is now drafted in `app/datasets.py`: exports
are requested as drafts, external sources require preflight-passed state and
purpose permission, AMAZWI rows require peer eligibility/audio availability and
active model-development consent, approval rechecks those conditions under a
row lock, and revocation is audited. The approved-export immutability trigger
and PostgreSQL tests are still required before this is final.

Plan 02 reproducibility primitives are now committed in `72cc3fb`: immutable
canonical manifests, speaker-safe deterministic splits, normalised WER/CER,
registry-hashed external-data preflight, explicit prohibitions on synthesis
tasks, and a local 60-GPU-hour/30-hours-per-account reservation guard. These
are controls only: no dataset, model or Kaggle GPU run has been downloaded,
started or claimed.

`6f9505c` adds deterministic ranking and promotion gates (with no model-alias
write path), evidence-index/model-card generators that suppress improvement
claims after failed promotion, and completion tracking for the same local GPU
budget ledger. The remaining ML work is test fixtures/reports, tabular
challengers and safe no-download training/evaluation packaging scripts.

The recoverable worker and read-only Council status API are now implemented in
`1d96339`. `run_council_worker.py --once` claims leased events, runs the four
deterministic specialists, completes successful events and retries failures;
`GET /contributions/{id}/council` reports DISABLED/PENDING/PARTIAL/READY/FAILED
without exposing raw audio or provider secrets. Real PostgreSQL worker tests
and dataset provenance/export work remain mandatory before final acceptance.

Plan 03 routing is now closed for the core golden path: the frontend has a
dedicated `/result/:contributionId` receipt route and the backend result
contract now exposes outcome, reward amount and currency. This is the visible
peer-truth-first receipt; the Signal Flow visual polish, Coverage Constellation
and operations screens remain separate acceptance work.

Plan 03 UI foundations are now shipped in `e747caa`: season-aware theme
selection (Midnight, Daylight and September Ndebele), tokenised Signal Card
materials, peer-truth/advisory primitives, and finite reduced-motion-safe
Signal animations. Operations surfaces and visual/browser evidence remain
open; these primitives are intentionally small and composable.

The next Plan 03/04 hardening slice is now on `main` (`0560c38` after rebase):
runtime mode parsing rejects insecure production/demo combinations, backend
`Settings` uses secret-safe typed fields and production validators, and the UI
has polite/assertive status announcement primitives for accessible async
flows. This is boundary infrastructure; it is not a substitute for external
auth/rate limiting or device/browser evidence.

### Contract correction — 01 Sep

The recording client was reviewed against the actual backend routes and
corrected in `bda63cf`: upload creation is now bodyless, finalisation sends the
server-required hash/mime/codec/duration/size fields, and answer submission
uses `answer_text`. This removes a concrete integration failure before browser
testing. Duration is currently reported as zero and must be measured before
production/demo acceptance.

Lethabo has now approved moving from the written design into an executable plan
and instructed continuous autonomous implementation with frequent commits and
pushes. The master execution contract is
`docs/superpowers/plans/2026-09-01-amazwi-governed-intelligence-program.md`;
the four subsystem plans beside it cover Stages 1–3, 4–6, 7–8 and 9:
`2026-09-01-amazwi-01-governance-audio-peers.md`,
`2026-09-01-amazwi-02-council-data-models.md`,
`2026-09-01-amazwi-03-signal-flow-ops.md` and
`2026-09-01-amazwi-04-hardening-demo.md`.

The first implementation wave is scoped consent → private local audio → real
peer API. It uses failing tests first and real PostgreSQL migration/invariant
checks. Sbu/Sibusiso now accepts the pre-event implementation decision. This
does not represent approval of backend/data/money decisions; those remain
pending Sbu's technical review. No deployment is resumed until that review.

**Review request when you return:** consent partial-unique/index semantics,
revocation races, private playback authorisation, resolver integration and any
schema/migration changes before they are treated as final in your lane.

---

## ⚠️ NEW — 01 Sep ~04:00 · approved maximum-scope design, implementation not started

Lethabo approved a substantial expansion design in
`05_amazwi/plan/16_GOVERNED_INTELLIGENCE_DESIGN.md`. This is an approved plan,
not a claim that the features are built and not a claim that you signed off.

**The required implementation order:**
1. Gate C server-derived scoped consent and revocation;
2. Gate D private object storage with PostgreSQL metadata;
3. Gate E real two-device peer flow;
4. recoverable post-resolution AI Council;
5. governed data refinery and external-dataset manifests;
6. Kaggle isiZulu/Setswana model campaign plus justified LightGBM/XGBoost uses;
7. Figma-first Signal Flow UI, Impact and MTN Language Ops.

**Authority boundaries retained:** two proficient peers remain authoritative;
AI runs afterward and cannot change eligibility or money; model-development
retention is a separate opt-in that does not alter the configured contribution
reward; Swivuriso is ASR-only and its TTS/cloning/synthesis prohibition is
preserved; provider, production reward and deployment selections remain gated.

**Ask:** review the consent, private-storage, outbox, export/provenance and
money/deployment boundaries before implementation is treated as final in your
lane. The paused Vercel deployment remains paused.

---

## ⚠️ NEW — 01 Sep ~02:20 · resolver transaction correction, pending your review

While continuing the §5 work, a regression test found that the earlier
resolver committed a terminal `EligibilityDecision` before it attempted the
speaker reward. A campaign-budget failure could therefore leave a contribution
marked `CORPUS_ELIGIBLE` with no reward, and an idempotent retry would return
the existing decision rather than credit the speaker.

**What changed in your lane, pending your review:**
- `resolve_contribution()` now commits terminal contribution state, decision
  and any reward only once. It rolls all three back when the reward cannot be
  committed.
- `credit_reward(..., commit=False)` is an explicit internal option for the
  resolver's wider transaction. Normal ledger callers retain their existing
  commit behavior.
- Real PostgreSQL regression tests prove both that a reward cannot exceed
  campaign funding and that eligible resolution requires an explicit positive
  amount. Both failures leave state `OPEN`, with no decision or reward.
  Full backend suite: **63/63 passing**.

**Scope boundary:** no reward amount was invented. A corpus-eligible call now
requires its caller to supply a positive amount instead of implicitly trying
to create an invalid zero-cent reward. MoMo, consent derivation, cohort
selection and endpoints remain unbuilt.

**Ask:** review this transaction boundary against `02_TECH.md` §5 and §8.
This is Lethabo's documented cross-lane correction, not a final platform or
money-policy sign-off.

---

## ⚠️ NEW — 01 Sep ~01:30 · third cross-lane block: §5 assignment/resolver service

Same session, extends past S5's original scope into §5 itself (named as the next open item in the previous entry below).

**What was built in your lane, pending your review:**
- `starter/backend/app/resolver.py` — `create_assignment()` (no-self-verification, expired/voided-audio rejection; no-double-assignment left to the existing DB constraint) and `resolve_contribution()` (§5's pseudocode implemented verbatim, same branch order and state names).
- 15 new tests in `starter/backend/tests/test_resolver.py`, every branch of the resolver plus the "safe to call repeatedly" requirement, all against real Postgres. Full suite now **61/61 passing**.

**What was not done, on purpose:** the actual random-cohort assignment-selection logic (needs §7/§10, not built), and consent/audio-quality derivation — `resolve_contribution()` takes `consent_active`/`audio_quality_passed` as explicit parameters rather than computing them, since `ConsentGrant` and audio quality aren't fully modelled yet.

**Ask:** same as the two entries below — review against `02_TECH.md` §5 when you're back. Full detail in `BUILD_LOG.md`'s `01 Sep ~01:30` entry.

---

## ⚠️ NEW — 01 Sep ~00:45 · second cross-lane block: schema, migrations, reward ledger

Same session, same loosened-lane basis as the S3 entry directly below this one. Built S5 (`P0.md`): the SQLAlchemy schema, a real Alembic migration and the reward-ledger functions needed for §8's six invariants.

**What was built in your lane, pending your review:**
- `starter/backend/app/models.py` — every record from `02_TECH.md` §3, with the §4/§8/`content/SCHEMA.md` CHECK and UNIQUE constraints enforced at the DB level (campaign budget ceiling, card field-count rules, no-double-verifier-assignment, unique reward per contribution/user/type).
- `starter/backend/alembic/` — a real migration, tested with a genuine upgrade→downgrade→upgrade roundtrip against embedded PostgreSQL 16 (via `pgserver`, no Docker needed). This caught a real bug: autogenerate's `downgrade()` doesn't drop PostgreSQL ENUM types, which broke the second upgrade. Fixed and documented inline in the migration file — flagging this because it's exactly the kind of thing Gate H's demo-reset requirement would hit live if it weren't caught now.
- `starter/backend/app/ledger.py` — `credit_reward`, `request_cash_out`, `apply_payment_callback`, `available_balance_cents`. Explicitly does NOT implement the MoMo adapter (§9) or the assignment/resolver service (§5) — left open.
- 24 new tests across 4 files, all against real Postgres, 0 mocks. Full suite: 46/46 passing.
- Full writeup, including the ENUM-drop bug, in `starter/backend/S5_README.md`.

**What was not done:** no MoMo integration, no resolver/assignment-creation logic, no endpoint wiring, no data-model decision beyond what `02_TECH.md` already specifies.

**Ask:** same as before — review against `02_TECH.md` §3/§4/§8 when you're back, accept/reject/flag. Full detail in `BUILD_LOG.md`'s `01 Sep ~00:45` entry.

---

## ⚠️ NEW — 01 Sep ~00:05 · cross-lane work needs your review, not your sign-off yet

**Context, so you're not surprised:** Lethabo said this session "work on the backend as well, it doesn't matter as long as we update on what we did — we all work on the same areas," loosening the lane rule for this session only (recorded in `BUILD_LOG.md`'s decisions table and `CLAUDE.md`). This is not a claim that you agreed to a permanent lane change — it's recorded as Lethabo's call, same as the earlier "proceed on my own authority" row on the build-timing dispute, which is **still open and not represented as settled with you.**

**What was built in your lane, pending your review:**
- `starter/backend/app/matching.py` — `is_correct()` and `normalise_answer()`, a straight implementation of `plan/13_IS_CORRECT_SPEC.md`'s five-step pipeline (NFC → lowercase → trim → collapse whitespace/hyphens → exact match). Nothing added beyond the spec: no edit-distance, no noun-class stripping.
- `starter/backend/tests/test_matching.py` — 20 tests, `pytest tests/` → 22 passed (incl. your 2 existing `test_provider.py` tests, unaffected). Tests run against the real hero-8 decks, not synthetic fixtures — checks every accepted answer matches itself and no distractor/blocked_word in either deck accidentally matches.
- Resolved the spec's own open item (hyphen-collapse safety) with a real check: neither deck hyphenates an accepted answer today, and there's a test that will fail loudly if a future card does.
- **Not wired into anything.** No endpoint calls it. `S5` (schema/migrations) and the actual resolver are untouched and still yours/open.

**What was not done:** no matching rule invented beyond the spec, no data-model change, no judgement call. This is the mechanical half of S3 only.

**Ask:** review against `13_IS_CORRECT_SPEC.md` when you're back — accept, reject, or flag a change, same as the handover protocol asks. Full detail in `BUILD_LOG.md`'s `01 Sep ~00:05` entry.

---

**From:** Lethabo · **Date:** Monday 31 August 2026
**Event:** Wednesday 2 Sept 09:30 → Thursday 3 Sept 12:00 · The Forum, Bryanston
**Repo:** https://github.com/LethaboMH14/Amazwi

---

## CURRENT OVERRIDE — READ THIS BEFORE THE HISTORICAL ENTRY

- **Eligibility boundary:** no written organiser approval exists and no organiser email will be sent. No product-specific competition implementation or Gate A–H work begins before the event opens. Pre-event plans, language content, Figma work and static mockups are preparation/reference only — not running-product evidence or submission artifacts.
- **Setswana cards:** both card validators are structurally green. isiZulu has zero warnings; Setswana has one explicit review warning naming the four replacement distractors `moraka`, `jusi`, `ting` and `diphaphatha`. L1 remains **WAITING** for Lethabo's aloud approval.
- **Deck:** L5 is **PARTIAL**. The existing file is a reference skeleton, not a finished deck; actual on-site screenshots, the judge-only script, fallback recording and rehearsal remain open.
- The entry below preserves earlier reasoning. Where its status conflicts with this override or `05_amazwi/P0.md`, the current override wins.

---

# ENTRY — 31 Aug, evening · answers to your five questions

**Historical base:** `3a28878` (the build-readiness reconciliation at that point)
**Current verification:** both card decks pass `validate_cards.mjs` with zero errors. The Setswana deck emits one explicit warning because four later distractor replacements still need native aloud confirmation.

---

## 0. 🟠 CURRENT LANGUAGE BLOCKER — validator green, four replacements await native approval

The earlier five accepted-answer errors were resolved. Current verification is:

```
cards_isizulu.json     0 errors · 0 warnings   ✅
cards_setswana.json    0 errors · 1 explicit native-review warning   ⚠️ structural pass
```

The structural pass does not settle language judgement. Lethabo replaced four overlapping distractors across `sw-004`, `sw-005` and `sw-007`: `moraka`, `jusi`, `ting` and `diphaphatha`. He must read them aloud and explicitly approve or replace them before L1 is complete. Do not weaken the validator or infer native approval from a green result.

---

## 1. Does the learner/proficient-verifier split still feel fun and understandable?

**Understandable, yes. Fun — with one real hole I think we should close cheaply.**

Your correction was right and I am not reopening it: a 4-way MCQ answer cannot validate the governed set. Two learners agree by chance 6.25% of the time, and agreement proves nothing about language competence.

But it removed something. In the original loop the guess *was* the validation, so the learner's tap had consequence. Now the learner plays a quiz that changes nothing — **and they can tell.** That is a motivation problem rather than a comprehension one, and it is the thing that quietly turns a game back into a survey.

**The cheap fix, with no change to eligibility logic** — give the learner's guess a visible consequence in a *different* currency:

- Report learner outcomes back to the speaker as **feedback**, never as eligibility: *"12 learners tried this, 9 recognised it."* Real signal, zero effect on `UNDERSTOOD`.
- Make it unmistakable that the clip is **a real person who got paid**, not a database sample. That is the one thing a quiz app structurally cannot copy.

**For you:** does surfacing learner-guess counts to the speaker create an integrity risk in your lane — can a speaker infer anything gameable from the distribution? If yes, I would rather drop it than negotiate it.

## 2. Can the verifier flow collect free text before reveal without feeling like a form?

**Yes — and the reason it usually feels like a form is three specific things, all removable.**

A form reads as a form because of a labelled field, a small submit button, and no sense of liveness. So:

- **No label.** The card context *is* the prompt. A field labelled "Your answer:" is instantly admin.
- **The input is the hero of the screen**, not a control at the bottom — large type, centred, waveform directly above it. It reads as *answering*, not *filling in*.
- **One input, one screen.** The referee tap comes **after** reveal, as its own beat.

That last point I would treat as structural rather than cosmetic. Putting *"what did they mean?"* and *"did they break the rule?"* on one screen makes it a form instantly — and it also contaminates the referee vote with answer-commitment, which touches your resolver's independence assumption, not just the feel.

## 3. Does the Impact Map retain the emotional close without public audio?

**Partially. It is genuinely weaker — and there is a substitution that recovers most of it.**

Being honest: hearing a human voice is visceral, and a dot on a map is not. Removing public audio costs us something real. It is still the right call.

What recovers it:

- **Count people, not data.** *"4,182 voices"*, never *"31.4 hours"*. Same number, completely different register.
- **The judge's own clip, played back to the judge.** That is not public audio — it is a contributor hearing themselves, on their own device, under their own consent. The close becomes *"you just made this"* rather than *"listen to strangers"*, which is arguably more personal, not less.
- **The map gains its dot live**, during the demo.

**For you — this is a data/consent call in your lane, not mine:** can the receipt safely play back the contributor's *own* clip? I believe that sits inside purpose consent and raises no public-audio concern, but you own it, and I do not want to design the close around something that turns out not to be clean.

## 4. Which neutral shell labels work best across isiZulu and Setswana?

**I want to push back gently on the framing: a "neutral" English shell is not neutral — it is English**, and it quietly contradicts the thesis on the one surface every user sees.

What I would actually do for the competition build:

- **The shell follows the user's declared language** rather than reaching for a neutral third option.
- Where a word must be shared, **prefer verbs and concrete nouns over abstract ones** — abstract nouns are where the two languages diverge most, and where translation quality is hardest for either of us to check under time pressure.
- **Let icons and numerals carry the ambiguous cases.** `R2.00` is language-neutral without trying to be.
- **Always the endonym: `isiZulu`, `Setswana`** — never "Zulu"/"Tswana". Free, and a South African judge will notice.

**For you:** do you agree the shell should follow the declared language? If you would rather ship an English functional shell for demo reliability — given neither of us can properly review the other's UI copy under time pressure — say so and I will build it that way. That is a legitimate trade, and I would rather settle it now than at Gate C.

## 5. Is the judge-only demo visually strong enough that room play can remain optional?

**Yes — and I would go further: room play should be optional by default, not a fallback.**

Room play was my idea originally, and the red team was right to take it apart: five-screen onboarding in ~100 seconds, a hotspot that carries about five devices, and — the part that actually decides it — **it does not demonstrate asynchronous matching**, which is the mechanic.

The judge-only path with three devices shows *more* of the product: speaker records on one phone, **two** verifier phones light up, resolution happens on screen. The two-verifier rule is what makes us not-a-quiz, and room play is the one format that hides it.

So: strong enough, and I would frame room play as an if-the-wifi-holds bonus that never carries load.

---

## WHAT I NEED FROM YOU

1. **Mass-noun second forms** — is a loan word like `pap` acceptable inside your matching contract? (§0)
2. **Learner-guess counts shown to the speaker** — integrity risk in your lane, yes or no? (§1)
3. **Own-clip playback on the receipt** — consent-clean? (§3)
4. **Shell language** — declared-language shell, or English functional shell for demo reliability? (§4)
5. **Anything in §§1–5 you think is wrong.** These are product-reasoning answers, not tested results. I would rather you disagree now than at Gate C.

---

## WHAT THIS IS

Two days of research, planning and adversarial review for our Track 2 entry. **Eleven planning documents, six research files, ~42,000 words in the plan and ~40,000 in the evidence.** Nothing is built yet.

**Start here:** [`05_amazwi/README.md`](05_amazwi/README.md) → [`05_amazwi/plan/00_MASTER_PLAN.md`](05_amazwi/plan/00_MASTER_PLAN.md)

The README has a **"FOR SBU"** section with the six decisions that need both of us and the four places I most want you to disagree with me. Read that before anything else.

---

## THE HEADLINE: THE PRODUCT CHANGED

What we submitted was *"a game where speaking your language pays."* Read honestly, that is **paid data labelling with a leaderboard** — which is Track 1 wearing a costume, and a judge who notices has a fatal question.

**The reframe, in three moves:**

1. **The understanding signal comes from the game.** A speaker describes a word against a 30-second timer; two proficient listeners independently type the concept and then referee the blocked-word rule. This produces a peer-verified semantic label, not a transcript or automatic language proof.
2. **Learners are a separate gameplay population.** They use MCQ for XP. Their answers do not validate the governed output. Speakers receive the competition honorarium; listeners/verifiers receive points.
3. **Anchor on the describe-it-without-saying-it game every South African has played** — invented here in 1998, and by accident the most efficient speech-elicitation mechanic ever designed.

> **"AMAZWI is the describe-it game — in your language, and it pays."**

⚠️ Never write the brand name of that board game in the submission form. It is a registered trade mark. Say *"you know the game we mean"* on stage; the room fills the blank themselves.

---

## YOUR JOB: DO TO THESE DOCS WHAT I DID TO THE LAST SET

**Same method, same standard, same effort.** Do not just read and approve. **Attack them.**

### 1 · RESEARCH the gaps I could not close

Three agents died to usage limits and two questions are unanswerable without other people.

| Gap | What is needed |
|---|---|
| ✅ ~~`F_GAMIFICATION`~~ | **Done — I wrote it.** [`F_GAMIFICATION.md`](05_amazwi/research/F_GAMIFICATION.md). It found **three things that contradicted the plan**, all now fixed: Elo ratings don't converge if you select on difficulty while updating it; team leaderboards harm the losing side while the winners gain nothing; and promotional competitions are governed by **CPA s36, not the Lotteries Act** — and that definition catches you *regardless of skill*. **Read §6, §7 and §9 before you touch the league or the scoring** |
| **MoMo Mini App design standards + CSP** | Promised by MTN's programme page, not rendered anywhere public. Dig into the portal. Building against an unknown CSP is a real risk |
| **Whether SA sandbox disbursement actually exists** | `B_MOMO_API.md` §1a suggests "South Africa Disbursement" is a bulk-payroll product behind a commercial agreement, **not a self-serve API**. If so, our payout demo is the labelled demo provider and we should know that today |
| **The bulk B2C disbursement fee** | Not the 2% consumer rate. **This one number decides whether R2 rewards are economical at all.** Only MTN can answer it |
| ~~Native-speaker sign-off~~ | ✅ **Resolved — it is us.** You are first-language isiZulu, I am first-language Setswana. Languages settled. Still cross-check each other's cards aloud |

### 2 · CRITIC — the standard I held, hold it back at me

I ran a red team against my own plan and it found **23 findings**, including a hole that would have killed the core mechanic. All are in [`08_REDTEAM.md`](05_amazwi/plan/08_REDTEAM.md) and all are now folded in. **Do the same thing to what is there now.**

The standard, in five rules:

1. **Extract, don't infer.** Quote the source or reject the claim. Every number needs a URL and a date.
2. **Code does the arithmetic.** I ran the unit economics in Python and it exposed a design flaw — uncapped rewards were 7.9× minimum wage. **Do not eyeball a number.**
3. **State limitations before anyone asks.** Slide 9 is *"what we did not build."* It is the highest-trust move available.
4. **A claim that contradicts our own research file is worse than no claim.** The red team caught me doing this twice.
5. **If a document contradicts another document, one of them is wrong.** Find them.

**Specifically go after these** — the places I am least confident:

- **The cold start.** A Tshivenda clip on a Tuesday in Thohoyandou — does it ever get two listeners? I added `EXPIRED` and a pay-anyway rule, but I am not certain that is enough.
- **The two-sided market.** *"Money crosses MoMo twice"* carries four of our defences and **the build has no way to take money in.** Either we build the sponsor screen or we change the sentence. Your call as much as mine.
- **The 26-hour gate schedule.** It is aggressive. If a gate is wrong, say so now, not Wednesday.
- **The live room-play.** Highest risk and highest reward in the pitch. If you are not confident, we drop to the judge-only demo.
- **The reward number.** R2.00/clip, 3-play daily cap. Is that meaningful enough in South Africa to be worth opening the app for?

### 3 · ADD — take them a step further

Where I stopped, keep going. Obvious next moves:

- **The card content** — ~30 cards per language, with `accepted_answers`, `distractors` and gold honeypots. **This is the bottleneck and it is a design job, not a translation job.** `05_BUILD.md` §2.0–2.1
- **Every UI string, in-language**, written by a first-language speaker. Machine-translated copy in a language-preservation product is a self-inflicted wound.
- **The error-state copy**, as plain strings in one file, written before Wednesday. Wiring pre-written strings at 07:00 Thursday is possible; writing them is not.
- **The pitch deck.** Ten slides. `06_PITCH.md` §4.
- **The submission form answers**, drafted and character-counted.

### 4 · MOCKUPS — spin them up

[`09_MOCKUP_LIBRARY.md`](05_amazwi/plan/09_MOCKUP_LIBRARY.md) has **thirteen references critiqued** on texture, shape, smoothness, colour, professionalism, style, feel, completeness and uniqueness — with what to take from each and what to avoid.

**Nothing in it is settled, including the AMAZWI board.** It is a kit to assemble from, not a menu to choose from.

**Design these five first:**
1. The card reveal — the slide screenshot
2. Recording — the product's portrait
3. The understanding moment — the emotional peak
4. The Voice Value Receipt — the credibility screen
5. The aggregate Impact Map — the closing image; no public raw audio or names

**Three critiques of our existing board you should know:**
- 🔴 **The tone is wrong.** It reads as a documentary about language loss. **This is a party game.** Nothing on that board is *fun* — no laughter, no rivalry, no speed, no near-misses. Reverence belongs in the Archive; the game needs to feel like a Friday night.
- 🔴 **The imagery is AI-generated and reads as such** — the face paint is a pan-African pastiche tied to no actual culture. Fine on a concept board. **Never in-product, and never on a slide as if it were documentary.** Photograph each other instead; it will be more convincing.
- **It shows 3 listeners; we moved to 2**, and it has the speaker rating their own round instead of the listener refereeing the banned-word rule. Six corrections in `09_MOCKUP_LIBRARY.md` §②.

**And the three gaps across all thirteen references:** none of them is funny, none is specifically South African *(Ndebele geometry, Kaaps, a taxi rank, a Joburg skyline — never generic "Africa")*, and none shows a failure state. **Those three gaps are where the design can actually win.**

---

## LINKS — everything visual lives here

| | Link |
|---|---|
| **App mockups** (10 screens) | https://claude.ai/code/artifact/889d9d01-823d-4a84-bd00-7d6e88007903 |
| **Theme directions** (4 grounds — we are still choosing) | https://claude.ai/code/artifact/3b464f09-c6da-4e97-a831-729d1df53f0d |
| **Figma design system** (38 variables, 5 collections) | https://www.figma.com/design/JPZuFmbhRh9fhkgBLxRymq |

⚠️ **The two canvases are private by default.** Lethabo: open each one and use the page's **share menu** to give Sbu access — I cannot share them from here.
⚠️ **The mockups are not finished** — three screens are crafted, seven are wireframes. See [`04_assets/mockups/REFINEMENT_BRIEF.md`](04_assets/mockups/REFINEMENT_BRIEF.md).

---

## THE SIX DECISIONS THAT NEED BOTH OF US

Full detail in the README. In short:

1. **Role split — reversed and confirmed.** Sbu owns PLATFORM (backend, MoMo, ledger, trust, deployment, isiZulu). Lethabo owns EXPERIENCE (frontend, product, demo, Setswana).
2. ~~Which two languages~~ — **settled: isiZulu + Setswana.** The competition does not build or pitch two ASR models; the advantage is first-language content ownership.
3. **Keep the name AMAZWI?** It collides with the Amazwi South African Museum of Literature — a real national institution. My call: keep it and own it. Decide today or not at all.
4. **Build the sponsor payment screen?** It is the only thing that makes the central fintech claim true.
5. **Pre-build?** No. No written approval exists and no organiser email will be sent. Product-specific competition implementation begins on-site when the event opens; pre-event artifacts are reference/preparation only.
6. **The kill rules.** Agree them Tuesday, before anyone is emotionally invested.

---

## TODAY, IN ORDER

- [ ] **Card content — hero eight first.** isiZulu is approved. Setswana is structurally green but its four replacement distractors need Lethabo's aloud approval. Expand either deck only after the golden path works.
- [x] **No organiser email.** The conservative event-start boundary now governs pre-built code. Confirm pitch timing and platform details from the event briefing without assuming a positive answer.
- [ ] **MoMo — Sbu owns this now.** Confirm Collections/Disbursement availability, preserve a sandbox-call budget and keep a labelled demo provider ready. The canonical build plan uses priority gates rather than a clock schedule.
- [ ] **Sandbox call budget on the wall — 30 calls.** The quota is undocumented and its cooldown is ~2 days, which outlasts the event. **No automated test ever touches it.**
- [ ] **Write the `is_correct` function on paper** before the card job starts. `02_TECH.md` §3.4.
- [ ] Card content. Design tokens. Sound assets.

---

## THE FIVE FACTS THAT CARRY THE REVISED PITCH

1. **Named published benchmarks show serious performance gaps for named off-the-shelf models on South African languages.** Always state the model, task and benchmark; never use “no system on earth.”
2. **Existing South African corpora such as Swivuriso are valuable.** AMAZWI's proposed delta is a continuous consumer game, transparent rewards and per-contribution consent evidence.
3. **The game output is a semantic or intent label, not a transcript.** Transcription and ASR training are downstream.
4. **MoMo is structural when it funds a mission, records an idempotent reward credit and settles cash-out honestly.** Every unavailable leg is labelled.
5. **The first feasibility claim is a closed two-language cohort, not nationwide liquidity.** Scale follows native content, consent and proficient-verifier supply.

---

## THE ONE THING I WOULD NOT COMPROMISE ON

**The honesty.** The strongest paragraph in the whole pitch is the one where we say what we did *not* do:

> *"We have not improved anyone's word error rate today. You can't do that in twenty-six hours, and anyone who tells you otherwise is showing you a slide, not a training run."*

Every judge in that room has been oversold to eleven times before we walk on. **Precision is the differentiator.** If you find something in these documents that overclaims, cut it — even if it sounds good. Especially if it sounds good.
