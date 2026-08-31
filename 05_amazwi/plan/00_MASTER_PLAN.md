# AMAZWI — MASTER PLAN
### Team Sonar · Track 2: Entertainment & Lifestyle · accepted source of truth

**Team:** Sbu + Lethabo
**Decision overlay:** `10_SBU_REVIEW.md`
**Evidence:** `../research/`
**Build constraint:** one in-person competition run; no product-specific code before the event unless the organisers approve it in writing.

---

## 1. THE PRODUCT

> **Play a voice challenge in your language. When two people understand you, your reward is credited through MoMo.**

The memory line is:

> **Speak. Be understood. Earn.**

AMAZWI is a short describe-and-guess game in isiZulu and Setswana. A speaker describes a target without using the target or four blocked words. Two proficient listeners independently recover the intended concept and referee the rule. An accepted contribution earns a transparent reward credit and a Voice Value Receipt.

Learners can play a four-option guessing version for XP. Their answers are gameplay signals, not corpus validation.

**Name decision:** keep **AMAZWI** for the event. The team knows a South African museum already uses the name, will not imply any partnership and will revisit naming before a public launch.

---

## 2. WHAT THE PROTOTYPE PROVES

The competition prototype proves this complete loop:

```text
funded language mission
        ↓
purpose-specific consent
        ↓
voice challenge + basic audio quality checks
        ↓
two proficient free-text verifiers + rule referee
        ↓
semantic label + corpus-eligibility decision
        ↓
idempotent reward credit
        ↓
MoMo settlement state
        ↓
Voice Value Receipt + aggregate Impact Map
```

It does **not** prove a verbatim transcript, an ASR-ready training hour, a WER improvement, a proficiency credential, a public national voice archive, nationwide listener liquidity or production South African disbursement availability.

The honest data description is:

> **consented, quality-filtered, elicited spontaneous speech with a peer-verified semantic or intent label.**

The card target is not a transcript. ASR transcription and model training are downstream curation steps.

---

## 3. THE THREE PLAYER STATES

| State | Evidence | Use |
|---|---|---|
| `PLAYED` | Any completed guess, including MCQ | XP and game feedback |
| `UNDERSTOOD` | Two independent proficient listeners match a native-curated accepted answer and do not jointly flag a rule violation | Semantic understanding signal |
| `CORPUS_ELIGIBLE` | `UNDERSTOOD` + audio-quality pass + active purpose consent | Governed downstream curation |

A correct guess does not prove the clip is in the declared language. The competition build records the contributor's declaration and the human-verification evidence; it does not claim language identification.

---

## 4. THE PAYMENT RULE

- **Speakers earn cash.**
- **Learners and verifiers earn Voice Points, streak and status in the competition build.**
- A cash reward is credited only once, after `CORPUS_ELIGIBLE`.
- The published rate is an honorarium for an accepted contribution, not a wage or employment promise.
- The AMAZWI ledger credits the reward immediately; provider cash-out can be batched at a transparent minimum.
- A provider request is not labelled paid until the provider confirms it.
- Sandbox, demo-provider and production states are always visibly distinguished.

If paid verification is tested later, it receives its own capped policy and economics. It is not part of the competition claim.

---

## 5. WHY MOMO IS STRUCTURAL

The strongest loop has two payment legs:

1. a sponsor or institution funds a named language mission through MoMo Collections;
2. accepted speaker rewards accumulate in an auditable ledger and can settle to MoMo at a viable threshold.

Collections is P0 if the event sandbox supports it. South African disbursement remains an external dependency; if it is unavailable, the app uses a clearly labelled demo provider while demonstrating the real state machine and idempotency.

Do not say “money crossed MoMo twice” unless both legs are actually demonstrated. Do not say “instant payout per clip”; say **instant reward credit, transparent MoMo cash-out**.

---

## 6. WHY THIS FITS THE TRACK

The player experience is a social game: a culturally authored challenge, speed and constraint, the tension of whether strangers understood, an earned reveal, Voice Points, streak and tier movement, and a visible reward moment.

The payment and data system strengthens the game, but the entertainment mechanic must still be worth playing without cash on the listener side.

---

## 7. WHY THIS FITS MTN

Use positive, defensible alignment:

> **MTN is expanding MoMo from transactions into daily digital services. AMAZWI gives the Mini App ecosystem a repeatable entertainment habit and could make MTN its first design partner for governed voice-intent data.**

Do not tell MTN that its shelf is empty, that a prior product failed, that MoMo is on a third attempt, that MTN owns no language asset, or that it is already a customer. Those lines are unnecessary and can make the room defensive.

A high-value future campaign is a **MoMo Moments** intent deck: prompts such as buy airtime, send money or check a balance. Two proficient listeners verify the intended action. That output has a direct speech-to-intent use without pretending it is a transcript.

---

## 8. OFFICIAL JUDGING CRITERIA

The public terms list five criteria without weights.

| Criterion | What Team Sonar demonstrates |
|---|---|
| **Innovation & Creativity** | The act of being understood is both the game result and a useful semantic label |
| **Relevance to Fintech Challenges** | Funded missions, transparent reward rules, an immutable ledger and honest MoMo settlement states |
| **Feasibility & Scalability** | Two quality-assured languages, a closed launch cohort, language packs and campaign configuration |
| **Technical Execution** | One cross-device clip, two independent verifiers, deterministic resolution, one reward and one receipt under retries |
| **Presentation & Pitch** | A reliable judge-only golden path, with room play as an optional second beat |

Past MoMo winners reinforce the scope: one local behaviour, one clear verb, and completed value movement. AMAZWI's verb is **speak**.

---

## 9. COMPETITION SCOPE

### P0 — must work

- MoMo Mini App host adapter and clearly labelled browser demo mode
- isiZulu and Setswana language packs
- eight native-authored hero cards per language
- adult gate and versioned, purpose-specific consent
- card, timer, recording, silence/clipping/duration checks and upload
- proficient-verifier playback, free-text answer and blocked-word referee tap
- two-verifier minimum
- conservative per-card accepted-answer matching
- explicit `VOIDED`, `EXPIRED` and `UNVALIDATED` states
- immutable integer-cent reward events and idempotency
- funded mission balance; Collections sandbox call if available
- provider adapter with labelled sandbox/demo/production state
- wallet and Voice Value Receipt
- aggregate, non-identifying Impact Map
- deterministic seed/reset, error copy and fallback recording

### P1 — only after P0 is rehearsable

- room guest mode with MCQ for play and XP only
- one tiered language/place league
- one gold verifier-attention check
- a compact buyer view: eligible seconds, acceptance rate and funds remaining

### Not built

- IRT, Elo, proficiency or difficulty credentials
- ASR fine-tuning, active learning or WER charts
- speaker embeddings, biometric identity or anti-spoof ML
- public raw-audio archive or named public attribution
- story chain or additional game modes
- paid listeners or learner subscriptions
- nationwide matching, feature-phone IVR or twelve-language content
- Redis, Celery, WebSockets, DVC, MLflow, W&B, Grafana or Terraform unless genuinely required by the working thin slice

---

## 10. PRIVACY AND GOVERNANCE

Recordings are private by default. Consent scopes are separate:

1. record and process this round;
2. play privately to assigned verifiers;
3. retain for the stated governed research/model-development purpose;
4. publish audio or named attribution publicly.

Scope 4 is off by default and not built for the competition.

Revocation retires audio from future playback and export. An audit tombstone remains so the ledger and consent history are not rewritten. The team does not promise instant model unlearning.

The public closing visual is an aggregate **Impact Map**, not a playable voice archive.

---

## 11. TEAM SONAR OWNERSHIP

### Sbu — Platform, MoMo and Trust

- FastAPI contract, PostgreSQL schema and state machines
- verification resolver and idempotent reward ledger
- MoMo Collections/disbursement adapters and reconciliation
- consent enforcement, privacy and audit events
- deployment, reliability and technical tests
- isiZulu cards and in-language copy
- technical proof and money/security Q&A

### Lethabo — Product, Experience and Demo

- product scope, React app and frontend state
- recorder experience, design system, wallet/receipt UI and Impact Map
- guest gameplay, error states and accessibility
- demo runbook, fallback video and pitch deck
- Setswana cards and in-language copy
- opening, live game narration, closing and product/culture Q&A

Both can run the demo alone. Lethabo breaks product/experience ties; Sbu breaks money, integrity and deployment-safety ties.

---

## 12. EXTERNAL DEPENDENCIES

Only organisers or MTN can settle these:

1. Which Mini App bridge, heartbeat and CSP rules apply to this event?
2. Is Collections enabled in the event sandbox?
3. Is South African Disbursement available to hackathon teams?
4. What are the minimum amount, currency and bulk B2C fee?
5. What pre-event code/content is permitted?
6. When do submissions close and pitches start?
7. What does the hackathon IP clause's “exclusive” marketing licence cover?

The product must remain demoable with a labelled provider adapter while these are unresolved.

---

## 13. GO / NO-GO

The build is coherent only when both teammates answer these identically:

- What produces `UNDERSTOOD`?
- Who earns cash?
- Is the output a semantic label or a transcript?
- Which MoMo leg is sandbox, simulated or future?
- What happens with fewer than two verifiers?
- What does revocation remove?
- What is the single P0 path?
- What is explicitly not being built?

If the answers differ, stop adding features and reconcile the product.
