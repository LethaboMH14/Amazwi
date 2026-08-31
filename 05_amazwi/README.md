# AMAZWI — Team Sonar · Track 2 · MoMo Mini App Hackathon 2026

**Team:** Sbu + Lethabo
**Languages:** isiZulu + Setswana
**Track:** Entertainment & Lifestyle
**Status:** planning and mockups only; no competition application is built.

---

## START HERE

The earlier plan was reconciled after Sbu's review. Read the canonical documents in this order:

| # | File | Purpose |
|---|---|---|
| **1** | [00_MASTER_PLAN.md](plan/00_MASTER_PLAN.md) | Accepted product, scope, judging alignment and ownership |
| **2** | [01_PRODUCT.md](plan/01_PRODUCT.md) | Speaker, proficient-verifier and learner contracts; screens and reward rules |
| **3** | [02_TECH.md](plan/02_TECH.md) | Thin-slice architecture, data/state model, ledger and MoMo safety |
| **4** | [03_BUSINESS.md](plan/03_BUSINESS.md) | Sponsored missions, pilot economics and MTN value |
| **5** | [04_DESIGN.md](plan/04_DESIGN.md) | Visual system and updated Impact Map direction |
| **6** | [05_BUILD.md](plan/05_BUILD.md) | One-run priority gates, acceptance tests and kill rules—no timeline |
| **7** | [06_PITCH.md](plan/06_PITCH.md) | Reliable judge-only demo, speaking ownership, claims and Q&A |
| **8** | [07_TRUTH.md](plan/07_TRUTH.md) | Claims, competitors, law, ethics and explicit limits |
| **9** | [08_REDTEAM.md](plan/08_REDTEAM.md) | Historical R1–R23 plus accepted second-pass findings R24–R28 |
| 10 | [09_MOCKUP_LIBRARY.md](plan/09_MOCKUP_LIBRARY.md) | Design-reference library, not product scope |
| **11** | [10_SBU_REVIEW.md](plan/10_SBU_REVIEW.md) | Accepted decision overlay and rationale |
| Roadmap | [11_EXPANSION.md](plan/11_EXPANSION.md) | Roadmap ideas and design/tooling notes; not competition scope and subject to the critique in `HANDOVER_LETHABO.md` |
| Execution | [P0.md](P0.md) | Current ownership allocation and gate summary; not a timeline |
| Sbu runbook | [SBU_PLATFORM_RUNBOOK.md](SBU_PLATFORM_RUNBOOK.md) | MoMo, trust and platform checklist with no secrets |
| Organiser draft | [ORGANISER_EMAIL_DRAFT.md](ORGANISER_EMAIL_DRAFT.md) | Preserved reference only; the team decided not to send it |
| isiZulu authoring | [content/CARDS_ISIZULU_AUTHORING.md](content/CARDS_ISIZULU_AUTHORING.md) | Historical worksheet; the reviewed source is `cards_isizulu.json` |
| isiZulu draft | [content/cards_isizulu.json](content/cards_isizulu.json) | Structured hero-eight draft; blocked from import until spoken native review passes |
| Card review | [content/CARD_REVIEW_2026-08-31.md](content/CARD_REVIEW_2026-08-31.md) | Structural critique and validation command for both hero decks |
| Lethabo handoff | [LETHABO_NEXT_WORK.md](LETHABO_NEXT_WORK.md) | Prioritised experience-lane tasks with testable exits |

Evidence lives in [`research/`](research/). All seven research files are present, including source-graded gamification work in [`F_GAMIFICATION.md`](research/F_GAMIFICATION.md).

Mockup sources live in [`../04_assets/mockups/`](../04_assets/mockups/). The `.dc.html` sources have been reconciled; the bundled canvas HTML must be regenerated before it is treated as current.

---

## PRODUCT CONTRACT

> **Play a voice challenge in your language. When two people understand you, your reward is credited through MoMo.**

> **Speak. Be understood. Earn.**

The speaker describes a target without using the target or four blocked words. Two proficient listeners independently type the concept and referee the rule. Audio quality plus active consent produces a corpus-eligible contribution and exactly one reward credit.

Learners play four-option MCQ for XP. MCQ never validates the governed output.

The output is **elicited spontaneous speech with a peer-verified semantic or intent label**. The target is not a transcript and the prototype does not claim ASR-ready hours or WER improvement.

---

## SETTLED DECISIONS

| Decision | Accepted answer |
|---|---|
| Roles | **Sbu:** Platform, MoMo, ledger, trust, deployment, isiZulu. **Lethabo:** Product, frontend, experience, demo, Setswana |
| Languages | isiZulu + Setswana; eight hero cards per language first |
| Cash | Speakers receive the contribution honorarium; listeners/verifiers receive Voice Points in the competition build |
| Validation | Two proficient free-text matches; MCQ is gameplay only |
| Data | Semantic/intent label, not transcript |
| Public view | Aggregate Impact Map; raw audio and names private by default |
| Fintech | Funded mission + immutable reward ledger + honest MoMo provider state |
| Cash-out | Immediate ledger credit; provider settlement at a viable threshold |
| Demo | Judge-only golden path first; room MCQ is optional |
| Scope | One mode and one end-to-end loop; ML, IRT/Elo, public archive and extra modes removed |

---

## P0 BUILD

- Mini App host adapter plus visibly labelled browser demo mode
- isiZulu and Setswana hero decks
- adult gate and purpose-specific versioned consent
- real card/timer/recording/audio-quality/upload flow
- two independent proficient-verifier flows
- conservative accepted-answer matching and referee decision
- `VOIDED`, `REVIEW_REQUIRED`, `EXPIRED` and `UNVALIDATED`
- immutable integer-cent reward ledger and campaign budget
- Collections if confirmed; labelled demo provider for unavailable legs
- wallet, Voice Value Receipt and aggregate Impact Map
- deterministic reset, mobile error states and fallback recording

Anything outside that list is P1 or cut. Full gates and tests: [05_BUILD.md](plan/05_BUILD.md).

---

## TEAM SONAR

### Sbu — Platform, MoMo and Trust

Backend/API, database/states, verification resolver, ledger, campaign funding, payment adapters, consent enforcement, audit, deployment, technical tests, isiZulu content and technical/business proof.

### Lethabo — Product, Experience and Demo

React/frontend state, design system, recording/verifier/learner UX, wallet/receipt/Impact Map UI, accessibility, demo runbook/fallback, Setswana content and the narrative/product presentation.

Both must be able to run the full demo alone.

---

## HANDOVERS

- Lethabo's continuously updated incoming context: [`../HANDOVER_SBU.md`](../HANDOVER_SBU.md)
- Sbu's accepted decisions and handback: [`../HANDOVER_LETHABO.md`](../HANDOVER_LETHABO.md)

Use both as a reciprocal, commit-referenced protocol: read the latest incoming handover before crossing lanes, record accepted/rejected decisions in the outgoing handover, and update the canonical document whenever a decision is accepted. A handover proposal alone does not override the canonical plan.

The handover documents provide collaboration context. `00_MASTER_PLAN.md`–`07_TRUTH.md` are the source of truth for implementation.

---

## EXTERNAL ANSWERS STILL REQUIRED

- current Mini App bridge, heartbeat and CSP specification;
- Collections availability in the event sandbox;
- South African Disbursement availability;
- currency, minimum amount and bulk B2C fee;
- pre-event code/content rule;
- submission close and pitch start;
- scope of the IP clause's “exclusive” marketing licence.

Until confirmed, every unavailable external leg has a visibly labelled provider-adapter fallback.

---

## NON-NEGOTIABLE PITCH TRUTH

- no real-money claim for a sandbox/demo-provider leg;
- no transcript claim;
- no live WER improvement;
- no automatic language proof;
- no public raw-audio archive;
- no proficiency credential;
- no claim that MTN is already a buyer;
- no criticism of MTN's prior products as the reason to choose AMAZWI;
- no service or model named as built unless it is running.
