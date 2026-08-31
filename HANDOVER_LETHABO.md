# HANDOVER → LETHABO

**From:** Sbu
**Date:** Monday 31 August 2026
**Based on:** Lethabo's handover through repository commit `9653725`

---

## HEADLINE

I reviewed the original submission, the complete research pack, all planning documents, your red team, the completed gamification research, the ten mockup sources and the refinement brief.

I accept the describe-and-guess reframe. I also accepted a narrower, judge-defensible version and reconciled the plan around it.

> **Play a voice challenge in your language. When two people understand you, your reward is credited through MoMo.**

> **Speak. Be understood. Earn.**

Read [`05_amazwi/README.md`](05_amazwi/README.md), then [`05_amazwi/plan/00_MASTER_PLAN.md`](05_amazwi/plan/00_MASTER_PLAN.md). Those now contain the accepted source of truth.

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
5. Pre-event code/content rule.
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
