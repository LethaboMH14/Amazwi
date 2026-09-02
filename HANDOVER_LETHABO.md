# HANDOVER → LETHABO

**From:** Sbu
**Date:** Wednesday 2 September 2026 (latest section); earlier sections dated inline
**Based on:** repository work through `96e2fae` (CI green, both jobs, real Postgres service container)

---

## 2 SEP — SBU'S REVIEW OF THE CROSS-LANE WORK

I reviewed the items filed "pending Sbu's review" by reading the code and tracing the actual paths, not by reading the log entries describing them. Verdicts below are binding for money, data-integrity and deployment-safety per `05_BUILD.md` §2.

### ✅ ACCEPTED — mission authorisation gate (Plan 03 Tasks 9+10)

I traced the whole path before accepting it, and the gate holds:

- `OperatorPrincipal` is only ever built by `principal_for_user()` from a persisted `users` row. There is no constructor path, and no request field, that sets `principal_kind` or `roles`. I checked `routes/ops.py` specifically for a header-injection route in — there isn't one; the route reads `principal.kind` for output only.
- The gate is in the service layer (`authorise_mission`), not just the UI, which is the conservative reading and the right one. A UI-only gate would have left the API auto-approvable.
- `confirmation_text` being keyword-only with no default is a genuinely good structural choice — it makes "authorise without naming what you're authorising" un-callable rather than merely discouraged.
- The strongest test is `test_automated_actor_cannot_authorise_without_the_human_step`: it hands an automated actor *both* the role and the correct confirmation string and still refuses. That's testing the actual threat model, not the happy path.
- The source-tree scan asserting `authorise_mission` has exactly one caller is the thing that keeps this true six commits from now, when someone adds a worker.

**Ruling on the `campaign_id` nullable FK — this was correctly left to me, so here is the decision:** a mission may be *proposed* without a funded campaign (nullable is right — proposal is cheap and should not be blocked on budget). A mission must **not** be *disbursed* against without a campaign with sufficient uncommitted budget. Put that check in the disbursement path when it's built, not in the authorisation path. Authorisation records human intent; funding is a separate assertion. Don't retrofit a NOT NULL onto the proposal table.

**One correction, and it matters for the pitch:** this gate rests on `app/identity.py`, which is `X-User-ID` + `X-Provider-Subject` headers with **no signature or secret**. Pairing the UUID against the persisted provider subject stops one user casually presenting as another, but it is not authentication — anyone who knows a valid pair can present as a human MTN operator. Plan 04 Task 2 (injectable auth, no production impersonation path) is still open.

> **So: never describe this in the pitch as a security control.** It is a *governance* and *correctness* control, and an excellent one. Say "human-in-the-loop by design — an automated actor structurally cannot authorise a mission." Do not say "only an authorised MTN operator can." The second sentence is not true until Plan 04 Task 2 lands, and it is exactly the kind of overclaim `07_TRUTH.md` exists to stop.

### 🔴 NEEDS RECONCILING BEFORE ANY EVIDENCE PACK — the governance ledger contradicts reality

This is the one real problem I found, and it is a documentation-integrity problem, not a code problem.

Real GPU hours were spent on `lethabomh14` across kernel versions v3/v5/v6/v7. Meanwhile, in the repository:

- `starter/ml/runs/README.md` still records **both** runs as `status: BLOCKED`, with `reservation ID: pending budget reservation`.
- `starter/ml/kaggle/budget.json` contains only caps and an account list — **no reservations array, no consumed hours, no record that any run ever happened.**

Both canonical governance artefacts state in writing that no run occurred. The `00:15` log entry flags this honestly as provisional — but that flag lives in a log entry, and these two files are what a reviewer, a model card generator, or a judge would actually read. This is precisely the failure `08_REDTEAM.md`'s standard names: *a document that contradicts another document means one of them is wrong.*

**Ruling:** reconcile both files against the run's actual output before anything generates an evidence pack, model card or acceptance write-up from this run. A model card built on top of a ledger that says `BLOCKED` inherits a false provenance chain, and provenance is the entire product claim. Until reconciled, this run produces **no promotable candidate**.

Related, and worth saying plainly: the preflight evidence itself is clean and I have no issue with it — `preflight_swivuriso.json` pins an exact revision (`3f988acc…`), an allowed task (`ASR_TRAINING`), accepted terms, a named reviewer and the registry hash. The gate did its job. It's the *ledger* that's behind, not the approval.

### ⚠️ Kaggle run outcome is still unverified

v7 was `RUNNING` as of the ~05:00 entry and no later entry confirms completion. Nothing in the repo yet proves a checkpoint or metric report exists, or what the real GPU-hour spend was (the reservation was a 10-hour *request*, which is not evidence of consumption). Pull `kaggle kernels output`, verify the artefacts are non-trivial rather than a silent no-op success, then record actual hours.

The promotion gate correctly requires artefact hashes, so an unfinished run **cannot** leak into a promotion by accident — that design is holding, and it's why this is a "verify it" note and not an alarm.

### ✅ ACCEPTED — removal of my `test_external.py`

No objection. It was written against the simpler `external.py` that got discarded in favour of the fuller gated implementation, and its coverage is superseded by `test_external_preflight.py`. Verified: `starter/ml` 38/38 green on current `main`. Don't re-add it.

### What was done well, specifically

- **The `BUILD_LOG.md` merge catch.** Resolving 23 add/add conflicts with `--ours` and then noticing this file needed the *opposite* resolution — because jcode's local copy was 63 lines against origin's 1517 — is the best process decision in this whole log. Applying one blanket rule would have silently deleted every earlier session's history on push. Checking each conflict's actual content before picking a strategy is the habit that caught it.
- **Declining to write a Kaggle API token** even when asked directly. Correct. Hold that line permanently.
- **Bounding the run scope** to dev splits (~683MB, ~8k clips) instead of the full ~3,000-hour corpus, on a real non-renewable overnight resource, after actually inspecting the dataset structure rather than trusting the design doc's figure.
- **Finding three real bugs before spending quota** by running the failing cases locally — particularly the `sys.path[0]` one that the existing test suite structurally could not catch, because `test_kaggle_scripts.py` only invokes `--help`, which exits before the import runs. That's a genuine test-coverage blind spot worth remembering.

### Housekeeping

Four `worktree-agent-*` branches are still on `origin`. They were WIP-checkpoint rescues and their work has landed on `main`. Merge-or-delete them before the event so nobody branches off a stale one by accident.

---

## CURRENT OVERRIDE — READ THIS BEFORE OLDER SECTIONS

- **Build decision (1 Sep 2026):** Sbu/Sibusiso accepts proceeding with product-specific implementation before the event. Existing code and assets may be the team's working baseline. The hackathon's in-person/no-outside-assistance rule still applies during the event, and the actual build history must remain honest.
- **Setswana cards:** both card validators are structurally green. isiZulu has zero warnings; Setswana has one explicit review warning naming `moraka`, `jusi`, `ting` and `diphaphatha`. L1 is **WAITING** for Lethabo's aloud/native approval.
- **Deck:** L5 is **PARTIAL**. The ten-slide file is a reference skeleton; the actual competition deck, on-site screenshots, judge-only script and no-network fallback recording remain open.
- Older review snapshots below preserve decision history. Where their status wording conflicts with this override, this override and `05_amazwi/P0.md` govern.

---

## HEADLINE

I reviewed the original submission, the complete research pack, all planning documents, your red team, the completed gamification research, the ten mockup sources and the refinement brief.

I accept the describe-and-guess reframe. I also accepted a narrower, judge-defensible version and reconciled the plan around it.

> **Play a voice challenge in your language. When two people understand you, your reward is credited through MoMo.**

> **Speak. Be understood. Earn.**

Read [`05_amazwi/README.md`](05_amazwi/README.md), then [`05_amazwi/plan/00_MASTER_PLAN.md`](05_amazwi/plan/00_MASTER_PLAN.md). Those now contain the accepted source of truth.

---

## REVIEW OF CURRENT BUILD PROGRESS (`4cfbd92`)

### Accepted

- S1 is correctly marked as Sbu's first external decision: preserve the sandbox-call budget, prove only an available leg, and label the fallback.
- Gate B is now honestly described as a seeded, pre-resolved fixture; Gate E remains the first live verification proof.
- The generic host bridge is an adapter with an explicit unverified-protocol label, and the content schema rejects under-filled hero cards.
- The P0 list now uses canonical gates, safe accepted-answer matching and the sponsored-mission pilot economics.

### Corrections made by Sbu

- `error_states.json` no longer promises offline clip storage, automatic notification, automatic payment retry or an unverified content-release cadence. Those promises contradicted the no-offline/no-durable-worker P0.
- The current handover base is updated to the latest reviewed commit. Continue logging a concise PING whenever a cross-lane contract changes; the build log is active context, not a substitute for reconciling the canonical documents.

### Your next dependencies

1. Read aloud and approve or replace the four new Setswana distractors: `moraka`, `jusi`, `ting` and `diphaphatha`; record the decision in `BUILD_LOG.md`.
2. Setswana error copy is reviewed. isiZulu error copy remains Sbu's first-language approval task; do not literal-translate either pack.
3. Continue wiring AMAZWI-specific screens/content into `starter/` under the accepted 1 September build decision. Keep unknown provider/host capabilities labelled and preserve honest build-history disclosure.

### Portal outcome shared with Lethabo

- The authenticated MoMo Developer Portal catalog visibly lists **Collection**, **Disbursements**, **Remittance** and **Sandbox User Provisioning**.
- This is catalog visibility only; subscription, provisioning and event-sandbox callability remain unconfirmed.
- Until an explicit entitlement or safe test result exists, implement the provider boundary so `DEMO_PROVIDER` is the honest fallback and keep currency disclosure unresolved.

### Current card status (supersedes review of draft `5959df1`)

- Both hero-eight decks now pass `content/validate_cards.mjs` with zero errors. Setswana deliberately emits one native-confirmation warning until the four replacements are approved.
- The original Setswana targets, blocked words and accepted-answer forms were reviewed. Four later distractor replacements remain a substantive language check even though the validator is green.
- Do not mark L1 complete until Lethabo approves `moraka`, `jusi`, `ting` and `diphaphatha` aloud and records that decision.

### isiZulu content approval

- Sbu approved the full isiZulu hero-eight deck on 31 August 2026: targets, blocked words, accepted answers and distractors.
- `content/cards_isizulu.json` is now the reviewed source and must pass `node content/validate_cards.mjs content/cards_isizulu.json` before import.

### Current cross-lane handoff

- Sbu will not send organiser questions. The build decision is now accepted: product-specific implementation may continue before the event, with the in-person/no-outside-assistance rule and honest build-history disclosure retained.
- Lethabo's immediate language deliverable is the aloud decision on the four replacement distractors. Structural validation is already green.
- Setswana error copy is reviewed; isiZulu remains pending Sbu's first-language approval. Structural error-state validation is green across all three language fields.
- The authenticated MoMo profile has no subscriptions. Build the receipt and wallet against `DEMO_PROVIDER`; do not imply a live Collections or Disbursements leg unless organisers provide a different provisioned account.

### Sbu decisions on the current handover questions

- Keep learner-guess counts out of P0. Learner MCQ remains XP-only and never becomes speaker feedback or eligibility evidence.
- The contribution receipt may privately replay the contributor's own clip only while recording consent is active; revocation removes that replay path along with future playback/export.
- Ship an English functional shell for competition-demo reliability. Keep first-language card and error copy in isiZulu/Setswana; a fully declared-language shell is post-P0.

### Assigned next work

Use `05_amazwi/P0.md` as the current status summary. `LETHABO_NEXT_WORK.md` remains useful as acceptance criteria, but items 3–5 produced pre-event reference assets only. Remaining experience work is native approval of four distractor replacements, on-site accessibility/resilience evidence, the finished deck/script/fallback pack and rehearsal.

---

## REVIEW OF YOUR LATEST PUSH (`d33094a`)

### Keep

- The Figma token system is a useful design asset. Keeping brand tokens invariant across grounds makes the visual identity less likely to drift.
- Deferring a Figma-plan upgrade is the right call. The build needs working screens, not a more elaborate design-tool configuration.
- The task-based model-routing principle is strong: escalate when a decision or claim is hard to verify; stay fast for work against a settled spec.
- The build log is a good collaboration mechanism. Its rule that a `PING` requires action is especially valuable in a two-person overnight build.

### Integrated corrections

1. `12_MODEL_ROUTING.md` now maps to canonical priority gates A–H, not the retired timed G0–G8 schedule.
2. The immediate Figma component set is card, banned-word chip, wallet/receipt state and button. League UI is not P0.
3. The build log now states that offline audio persistence, service-worker work, daily-quest/R11 mechanics and leagues are cut from P0.
4. The current content target is eight excellent hero cards per language. A 30-card pack is a follow-on expansion once the recording and verification path works.
5. The build log's active tech table no longer presents FastAPI background tasks as durable processing or unselected providers as shipped technology.

### Remaining risks

- The economic document is already correctly rebuilt around sponsored semantic-label missions. Do not reopen the old transcribed-hour comparison or add a margin claim before actual provider fees and acceptance rates are known.
- The product is now an active implementation baseline. The next valid proof is a Gate A shell connected to the backend, then the deterministic golden path; do not call a gate complete until its exit condition is verified.
- I reviewed the Figma system from its documented token/component contract, not from a rendered interactive file or captured device flow. Contrast, focus, hit-area, reduced-motion and sunlight legibility still need visual testing on the actual screens.

---

## REVIEW OF THE ROADMAP ADDENDUM (`ed1254b`)

### Keep

- Rejecting a chance-based spin is the right call. A published fixed-rate redemption is a cleaner future loyalty pattern than wagering a monetary credit.
- Correcting an overly absolute earlier view is good research practice. The expansion document is stronger when it distinguishes data provenance, consent and product risk.

### Do not adopt yet

1. **Consent is necessary, not a blanket approval.** Separate consent does not itself settle purpose limitation, retention, security, third-party rights, community expectations, consumer protection or the specific legal/contractual requirements for biometric/video/synthesis processing. “Viable” and “allowed” remain hypotheses requiring specialist review and a concrete rights design.
2. **A provenance firewall is an architectural requirement, not a sentence.** A future synthesis feature would need enforceable dataset separation, use restrictions, withdrawal behaviour, access controls and an auditable training-data register. It must not be implied by today’s consent lineage alone.
3. **Fixed-rate airtime/data redemption is roadmap only.** Do not claim MTN marginal-cost economics, an in-ecosystem redemption benefit or a reduced B2C-fee problem until MTN confirms the commercial model and the product actually implements it.
4. **No `MODALITY_VALUE` multiplier is accepted.** It needs evidence about contribution cost, data use, participant risk, consent burden, verification burden and campaign budget. “Richer data is worth more” is not a safe payout rule by itself.
5. **Learn/Activities must not reshape P0 navigation.** Keep the learning purpose visible through MCQ and the existing flow. Add a dedicated surface only after the golden path earns its place.

The addendum remains a useful roadmap discussion. It does not override the private-by-default audio P0, speaker-only reward rule, or the canonical business and consent model.

---

## REVIEW OF P0 AND ECONOMICS PUSH (`9c3727c`)

### Keep

- A concise P0 allocation and a token-based theme switcher are useful implementation aids.
- Protecting a sandbox-call budget and freezing an honest demo-provider fallback when a provider leg is unavailable are both sound operational practices.

### Corrections applied

1. `P0.md` is now priority-gated, with no clock, hour estimates or dated theme deadline. This preserves the user-requested one-run plan without a timeline.
2. The accepted-answer rule now uses normalisation plus native-curated answers/reviewed aliases. Blanket prefix stripping and broad Levenshtein are explicitly excluded.
3. No organiser permission exists and none will be requested. Pre-event work is preparation/reference only; a generic starter does not authorise product-specific AMAZWI code or count as submission implementation.
4. The hour-based rework was converted to a historical, unadopted scenario. It cannot supersede the sponsored-mission pilot model because its output unit, costs, fees, margin and redemption assumptions are not measured.
5. P0 does not make airtime/data redemption, provider marginal cost, production verifier payment or `MODALITY_VALUE` a build or pitch claim.

The P0 document is now safe to execute: recording, two proficient verifiers, one eligibility decision, one ledger credit, an honest provider state, receipt and reset. That is the only proof that matters before roadmap economics.

---

## REVIEW OF YOUR LATEST PUSH (`d8a1e82`)

### Keep

- Rejecting face-capture avatars and voice cloning is exactly right. Both contradict the minimum-data, no-biometric trust position.
- The four visual directions give the frontend a useful decision set. Theme A has the clearest product potential; a high-contrast day mode is an accessibility requirement, not just an aesthetic alternative.
- SASL is strategically promising **only as a partnership-led roadmap**. The modality argument is memorable if framed as a future possibility, not as something this prototype has validated.
- A click-consonant learning aid and private self-comparison could become strong learner features after the core loop works.

### Correct before treating any of it as product or pitch truth

1. **No expansion is competition scope.** SASL, click training, archive queries, dialect mapping, proficiency certification and all computer-vision work stay roadmap. P0 remains one audio loop in isiZulu and Setswana.
2. **Do not turn the private-by-default Impact Map back into an archive.** “Ask the Archive” and a dialect map require separate contributor rights, moderation, retention, location minimisation and community governance. They are not free by-products of the current data model.
3. **Do not imply semantic agreement validates language, dialect or proficiency.** Two verifiers establish that they recovered the card concept. That is not a certified language label, dialect finding or employability credential.
4. **Move every new factual claim through `07_TRUTH.md` and a primary source before use.** This includes “no SASL corpus,” “nobody has built one,” the voice-cloning percentage, the Duolingo/date assertion, the BPO figures and claims about other products. Until then, they are research hypotheses, not slide facts.
5. **Theme references need cultural and accessibility checks.** Attribute any specific tradition accurately, do not treat a living cultural form as a generic skin, test contrast and reduced-motion states, and keep the neutral UI shell co-equal for isiZulu and Setswana.
6. **The model/tooling recommendations are optional.** Do not install a plugin, proxy or workflow tool during the competition without reading it and agreeing it is permitted. The repository plan, tests and handovers are the operating system; model branding is not part of the product.

I added a canonical-status note to `11_EXPANSION.md` and an implementation guardrail to the themes README. If you disagree with any correction, append the evidence and the affected canonical section to `HANDOVER_SBU.md`.

---

## ROLE SWAP — CONFIRMED

### Sbu owns Platform, MoMo and Trust

- FastAPI/backend and API examples
- PostgreSQL and all state machines
- assignment and verification resolver
- immutable reward ledger and campaign budget
- MoMo Collections/Disbursement adapters and reconciliation
- consent enforcement, privacy and audit
- deployment, reliability and technical tests
- isiZulu content and copy
- technical/business proof and Q&A

### Lethabo owns Product, Experience and Demo

- React/frontend and client state
- design system and recorder interaction
- learner, proficient-verifier and referee UX
- wallet, Voice Value Receipt and Impact Map UI
- accessibility, error states and browser/Mini App disclosure
- demo runbook, fallback recording and pitch deck
- Setswana content and copy
- opening, live game narration, close and product/culture Q&A

You break product/experience ties. I break money, data-integrity and deployment-safety ties. We both must be able to run the demo alone.

---

## FIVE ACCEPTED PRODUCT CORRECTIONS

### 1. Semantic label, not transcript

The card target is the concept listeners recovered; it is not what the speaker said verbatim. The output is:

> **consented, quality-filtered, elicited spontaneous speech with a peer-verified semantic or intent label.**

ASR transcription/training is downstream. We do not sell or price ASR-ready hours in the pitch.

### 2. Learner and verifier are different roles

- MCQ learner play → `PLAYED`, XP only.
- Two proficient free-text matches → `UNDERSTOOD`.
- Quality + active consent + no joint rule violation → `CORPUS_ELIGIBLE`.

A learner answer cannot validate the governed set. A correct guess does not prove the declared language.

### 3. Speakers earn; listeners receive points

The competition removes R0.50 listener cash. Speakers receive the published contribution honorarium only after corpus eligibility. This makes “speaking pays; listening teaches” literally true and simplifies the ledger.

### 4. Aggregate Impact Map, not a public voice archive

Raw voice and names are private by default. The public visual contains aggregate dots/counts. Public audio/attribution would require a separate opt-in, moderation and legal path and is not built.

### 5. One thin slice

P0 is one real recording, two proficient verifiers, one eligibility decision, one reward, one honest provider state, one receipt and deterministic reset.

IRT/Elo, proficiency, ASR training, active learning, speaker biometrics, paid listeners, story chain, public archive, nationwide matching and extra languages are cut from the competition build.

---

## MOMO DECISION

- Collections is the preferred real sandbox proof if enabled.
- South African Disbursement remains unconfirmed.
- The ledger credits the reward immediately.
- Provider cash-out occurs at a viable threshold; no R2 transfer-per-clip promise.
- Every sandbox/demo/production mode is labelled.
- Say “money crossed MoMo twice” only when both legs actually ran.

I own this lane and will publish the exact API examples and provider states before frontend integration.

---

## YOUR NEXT EXPERIENCE PASS

The `.dc.html` sources in [`04_assets/mockups/`](04_assets/mockups/) were corrected for the accepted product:

- `Listen` now says learner XP and non-validation;
- `Referee` no longer pays R0.50 or reveals the other verifier first;
- `Receipt` says semantic label, two independent matches, credited and provider mode;
- `Consent` removes named Archive consent and explains retirement;
- `Archive.dc.html` is now the aggregate Impact Map, although the filename is retained for the canvas.

Please apply your craft pass to those sources, then regenerate `amazwi-app-mockups.html`. Do not style the old bundled canvas as though it is current before regeneration.

Your five hero screens are now:

1. card reveal;
2. real recording;
3. proficient verifier/referee;
4. Voice Value Receipt;
5. aggregate Impact Map.

The understanding moment may still animate two verifier ticks and the speaker reward credit.

---

## CONTENT HANDSHAKE

- I author/approve eight isiZulu hero cards first.
- You author/approve eight Setswana hero cards first.
- Each card: target, four blocked words, accepted answers, three distractors and deck/campaign.
- We cross-read for playability, but the first-language owner has linguistic final say.
- No placeholder word or unverified translation reaches the pitch.

---

## DEMO HANDSHAKE

Primary demo: one speaker phone, two proficient-verifier phones and one display. Room-wide MCQ is optional after the golden path works.

You narrate the product and live interaction. I monitor the resolver/provider state and explain the ledger, consent enforcement and MoMo truth.

Every fallback must be said aloud: browser demo mode, seeded campaign, sandbox Collections or demo-provider cash-out.

---

## EXTERNAL QUESTIONS STILL OPEN

1. Mini App bridge, heartbeat and CSP specification.
2. Collections event-sandbox availability.
3. South African Disbursement availability.
4. Currency, minimum amount and bulk B2C fee.
5. Mini App/build rules to confirm at the event; until then, the no-product-code-before-event boundary holds.
6. Submission close and pitch start.
7. Meaning of the “exclusive” marketing licence.

Nothing in frontend scope should depend on one of these being answered positively.

---

## WHAT I NEED YOU TO REVIEW

1. Does the learner/proficient-verifier split still feel fun and understandable?
2. Can the verifier flow collect free text before reveal without feeling like a form?
3. Does the Impact Map retain the emotional close without public audio?
4. Which neutral shell labels work best across isiZulu and Setswana?
5. Is the judge-only demo visually strong enough that room play can remain optional?

Please record disagreements in your next `HANDOVER_SBU.md` update and reference the exact canonical section you want changed. Do not revive an older feature only because it still appears in git history or the stale compiled canvas.

---

## CONTINUOUS HANDOVER PROTOCOL

`HANDOVER_SBU.md` is Lethabo's live handover to Sbu. `HANDOVER_LETHABO.md` is Sbu's live handover to Lethabo. Before changing an interface owned by the other person, read that person's latest handover and the canonical plan.

Each new handover entry must state:

1. the commit it is based on;
2. what changed and which files changed;
3. any API, state, copy or demo-contract change;
4. what was verified and what is still unverified;
5. blockers, questions and the exact action requested from the other person.

Append new dated entries above older historical detail; do not erase reasoning that the other person may still be reconciling. A proposal in either handover does not silently override the canonical plan. The receiving teammate records **accepted**, **rejected** or **needs evidence**, and an accepted decision updates the relevant canonical document in the same change.

Keep commits narrow enough to review. Do not change the other person's owned implementation lane without calling it out in the handover. Shared API examples, state names and demo copy are frozen only when both handovers agree and the canonical files reflect the agreement.
