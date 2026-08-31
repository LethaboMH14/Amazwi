# AMAZWI — SBU REVIEW AND WINNING-SCOPE DECISIONS
### Independent review of the original submission, research pack, product plan, build plan and pitch

**Reviewed:** 2026-08-31
**Repository state reviewed:** `main` through `9653725`
**Decision status:** **accepted by Sbu on 2026-08-31.** This is now the decision overlay for reconciling the rest of the plan.

---

## 1. EXECUTIVE VERDICT

AMAZWI is a strong hackathon idea with a memorable human moment, genuine MoMo relevance and a credible South African problem. Lethabo's reframe from a paid recording task into a describe-and-guess game is the right strategic move for **Entertainment & Lifestyle**. The repo's research, claims discipline, failure planning and payment-state thinking are far above normal hackathon quality.

At the time of review, the plan was not build-ready. The accepted decisions have since been reconciled into `00_MASTER_PLAN.md`–`07_TRUTH.md`; the application itself is still unbuilt.

Its main problem is no longer lack of thinking. It is that the documents promise **three different products at once**:

1. a party game for language learners;
2. a paid speech-data acquisition system;
3. an ASR corpus and proficiency-credential platform.

Those products need different users, different validation and different evidence. Combining them creates contradictions that a judge can expose with a short question.

The winning version is narrower:

> **AMAZWI is a MoMo voice game: complete a challenge in your language, let two proficient listeners prove they understood you, and earn a transparent reward from a funded language mission.**

For the competition, prove one complete value loop:

> **fund mission → consent → record → two-person verification → reward ledger → MoMo settlement state → Voice Value Receipt**

Everything else is a roadmap.

---

## 2. WHAT LETHABO IMPROVED — KEEP THESE

These changes materially strengthened Sbu's original submission and should survive any further cut:

- **The game is now the interaction, not a leaderboard attached to labour.** Describe-and-guess gives Track 2 a real answer.
- **Two first-language launch languages are named:** isiZulu with Sbu and Setswana with Lethabo. That is more defensible than pretending to quality-assure all official languages.
- **The card target was cut to 30 per language, with eight demo cards first.** Good content is more important than a large deck.
- **Coverage pricing replaced language-rarity pricing.** This avoids paying people according to ethnicity or treating endangered languages as a cheap market input.
- **The plan stopped claiming real sandbox money and live WER improvement.** Those corrections protect Technical Execution.
- **Payment states are taken seriously:** pending, available, submitted and paid are not treated as synonyms.
- **Consent, revocation and payout events are designed as auditable records.** This is a meaningful differentiator if the implementation proves it.
- **The Voice Value Receipt is excellent.** It makes an invisible backend decision visible and connects voice, consent, validation and money in one artefact.
- **The live-play idea can make the room remember the team.** Keep it as an optional expansion of a reliable judge-only demo.
- **The repo credits Swivuriso, African Next Voices and the Esethu Framework.** Partnership is a stronger position than pretending prior work does not exist.

---

## 3. THE FIVE DECISIONS TO FREEZE BEFORE BUILDING

### Decision 1 — name the data honestly

The current game does **not** produce an ASR-ready corpus.

A describe-and-guess clip has a target concept and evidence that listeners understood the intended concept. It does not have a verbatim transcript. A target such as `taxi` is a **semantic or intent label**, not the words the speaker actually said. That means the clip can support speech-to-intent, semantic retrieval, representation learning, language research and later transcription, but it cannot directly supervise ordinary speech-to-text training.

The repo also calls the speech “conversational.” The more accurate term is **elicited spontaneous descriptive speech**. It is freer than read-aloud data, but it is still produced by a game prompt and should not be represented as natural call-centre conversation.

**Freeze this wording:**

> “The competition prototype creates consented, quality-filtered speech with a peer-verified semantic label. Verbatim transcription and ASR training are downstream curation steps, not claims of this prototype.”

**High-value improvement:** add a sponsored “MoMo Moments” deck with intent cards such as *buy airtime*, *send money* or *check a balance*. A verified intent label is directly useful to a future voice interface even without a transcript. That gives MTN a clearer first-use case than generic data licensing.

### Decision 2 — separate player types

The current documents combine two different listeners:

- a **learner/player**, who uses four-option multiple choice because it is accessible and fun;
- a **proficient verifier**, whose free-text answer and rule-referee vote can support a high-confidence label.

They cannot be treated as the same quality signal. The product plan correctly says random MCQ agreement must not validate the corpus, but the demo path is MCQ and the pitch still calls the result validation.

Use three explicit states:

| State | Evidence | Meaning |
|---|---|---|
| `PLAYED` | Any completed guess | Gameplay and XP only |
| `UNDERSTOOD` | Two independent proficient listeners match a native-curated accepted answer | Semantic intent understood |
| `CORPUS_ELIGIBLE` | `UNDERSTOOD` + audio quality pass + active consent + no rule violation | Eligible for governed downstream curation |

Do not say a guess proves the correct language. It proves the listener recovered the intended concept. Language remains contributor-declared until a reliable human or model check exists.

### Decision 3 — simplify who earns

The cleanest competition rule is:

- **speakers earn cash;**
- **listeners earn XP, streak and league status;**
- cash is credited only after two proficient verification events;
- the reward is an honorarium for an accepted contribution, not a wage or an employment solution.

This removes the unresolved paid-listener economics, the R0.50 judgement farm, the contradictory “learners earn nothing / listeners earn money” claims and a second payout path. It also gives meaning to “speaking pays; listening teaches.”

If paid verification is retained after the pilot, price it separately, cap it, and stop saying “nobody reviews anything.” A listener who checks banned words and earns for a judgement is performing verification work, even when the interface is playful.

### Decision 4 — replace the permanent public archive

“Permanent, named, public and revocable” cannot all be true at once.

Raw voice, a name and a place can identify a person. A public archive also needs moderation, publication rights and a separate risk assessment. It is not the ethical answer to extraction merely because it is visible.

For the prototype:

- recordings are **private by default**;
- the contributor can replay their own clip on the private receipt;
- the public screen shows only aggregate, non-identifying contribution dots and counts;
- public audio sharing is a separate, optional consent scope and is not built;
- revocation retires the clip from future playback and export while leaving an audit tombstone, not the audio, in the ledger.

Rename the demo visual from **Archive** to **Voice Map** or **Impact Map**. The emotional payoff remains without publishing personal voice data.

### Decision 5 — choose the one product sentence

Use one sentence everywhere:

> **Play a voice challenge in your language. When two people understand you, your reward is credited through MoMo.**

Do not use these as lead claims:

- youth employment solution;
- ASR model improvement;
- nationwide language archive;
- validated proficiency credential;
- learner subscription;
- “money crosses MoMo twice” unless Collections is actually shown;
- “instant payout per clip” when the provider settlement is batched or simulated.

---

## 4. THE WINNING COMPETITION PRODUCT

### 4.1 Primary user story

> As an adult isiZulu or Setswana speaker, I accept a clear use licence, play one short voice challenge, see that two proficient listeners understood me, receive a transparent reward credit, and get a receipt showing why it was earned and what I consented to.

### 4.2 The one complete loop

1. **A language mission is funded.** Use MoMo Collections if the event sandbox supports it. Otherwise show a clearly labelled seeded campaign balance.
2. **The speaker enters through the Mini App shell** and chooses isiZulu or Setswana.
3. **Consent is captured** for recording, limited peer playback and the stated purpose. No public-audio consent is requested.
4. **The speaker receives one native-authored card**, records a clue and passes simple client-side checks for silence, clipping and duration.
5. **Two proficient listeners are assigned.** They type the concept and answer one referee question about the target/banned words.
6. **The resolver makes a deterministic decision.** Both accepted answers + no two rule flags = `UNDERSTOOD`; quality + consent makes it `CORPUS_ELIGIBLE`.
7. **An immutable reward event is posted.** The balance changes once, even under retries.
8. **The wallet shows the true settlement state.** Sandbox, demo provider and production are visibly distinguished.
9. **The Voice Value Receipt appears.** It includes contribution ID, semantic label, validation evidence, reward rule, consent version and provider reference/state.
10. **The Impact Map increments** with an aggregate contribution, not public raw audio.

### 4.3 Why MoMo is structurally necessary

The strongest version is not “we added a payout button.” It is:

- a sponsor or institution funds a named language mission through Collections;
- accepted contribution rewards are recorded in an auditable wallet ledger;
- users withdraw through MoMo once a sensible threshold is met;
- the receipt connects funding, work accepted, consent and settlement.

Credit the reward immediately in the AMAZWI ledger; do not promise a provider transfer of R2 after every clip. Micro-transfers may have minimum amounts, fees and operational limits. **Instant reward credit and batched MoMo cash-out** is more feasible and more honest.

---

## 5. JUDGING-CRITERIA ALIGNMENT

The official criteria are listed without public weights. This is an internal readiness assessment, not a prediction of scoring.

| Criterion | What is already strong | Current risk | Winning proof |
|---|---|---|---|
| **Innovation & Creativity** | A familiar social game produces useful language signals and a transparent reward | Calling MCQ gameplay “corpus validation” weakens the novelty under scrutiny | A person speaks, strangers recover the concept, and the waveform becomes a receipt in one visible interaction |
| **Relevance to Fintech Challenges** | Small-value rewards, wallet trust, consent and settlement fit MoMo | Outbound reward alone can look bolted on; learner payment is hypothetical | Show a funded mission, immutable reward credit and one real sandbox payment leg, with every simulated leg labelled |
| **Feasibility & Scalability** | Two languages, provider adapter and modular monolith are sensible | Nationwide listener liquidity, public archive and ASR data sales are unproven | Launch as a closed sponsored cohort; scale by language packs and campaigns only after liquidity and quality are measured |
| **Technical Execution** | Audio capture, idempotency, true payout states and deterministic reset are strong | IRT, ML quality models, active learning, offline sync and many services dilute the working core | Demonstrate one cross-device clip, two verifiers, one resolution, one ledger credit and one receipt; show retry safety |
| **Presentation & Pitch** | The voice-to-money transformation and receipt are memorable | A 52-person network demo can fail publicly; aggressive claims about MTN or other datasets can make the room defensive | Judge-only golden path first; room play second if healthy; close on a real receipt and aggregate Voice Map |

### What past MoMo winners teach this plan

The winner research in `01_research/RESEARCH_BRIEF.md` shows a consistent pattern:

- winners solve one local behaviour, not a platform-sized future;
- access innovations win when they remove a real constraint;
- MoMo is part of the completed value movement;
- the product can be repeated as a single verb: cash out, split, save, pay by voice.

AMAZWI's verb should be **speak**:

> **Speak. Be understood. Earn.**

The repo currently adds archive, credentials, learning, active learning, data marketplace, campaigns, leagues and multiple game modes. Those may become a company. They should not become the hackathon submission.

---

## 6. COMPETITION BUILD SCOPE — NO TIMELINE, ONLY PRIORITY

### P0 — must work end to end

- Mini App host adapter plus a browser demo mode that is visibly labelled
- isiZulu and Setswana language packs
- eight excellent demo cards per language; no need to expose the rest
- adult gate and versioned, purpose-specific consent
- one speaker flow: card → timer → recording → basic audio checks → upload
- one proficient-verifier flow: playback → free-text answer → rule-referee tap
- two-verifier minimum; never validate from one answer
- conservative per-card accepted-answer matching
- contribution state machine including `VOIDED`, `EXPIRED` and `UNVALIDATED`
- immutable reward events in integer cents with idempotency
- campaign funding balance, real Collections sandbox call if available
- MoMo provider adapter with a clearly labelled demo implementation
- wallet states and Voice Value Receipt
- aggregate Impact Map/counter
- deterministic seed/reset
- one reliable mobile path, explicit error copy and a recorded fallback demo

### P1 — add only after the P0 loop is rehearsable

- room guest mode using MCQ for fun and XP, explicitly excluded from corpus validation
- one language or place leaderboard
- one gold/honeypot verifier check
- compact buyer view with contribution count, eligible seconds, acceptance rate and funds remaining
- one real sandbox call on the payment leg that the organiser confirms

### Not in the competition build

- IRT, latent ability or difficulty scoring
- a proficiency credential
- ASR fine-tuning or a WER-improvement chart
- active-learning claims or an acquisition model
- speaker embeddings, voice uniqueness or biometric checks
- anti-spoof ML
- public raw-audio archive
- story chain and all additional modes
- paid learner subscriptions
- nationwide asynchronous matching
- Redis, Celery, WebSockets, DVC, MLflow, W&B, Grafana and Terraform unless they are genuinely used by the thin slice
- offline capture/synchronisation beyond a clear retry message
- all twelve languages, IVR or feature-phone entry

If P0 works, the team has a credible product. If P0 does not work, no amount of roadmap UI will recover Technical Execution.

---

## 7. PRODUCT AND VALIDATION CORRECTIONS

### 7.1 Accepted-answer matching

Do not ship blanket noun-class prefix stripping plus Levenshtein distance of two.

That combination can remove meaning-bearing morphology and creates false positives on short words. For the competition deck:

1. lowercase and Unicode-normalise;
2. trim and collapse spaces/hyphens;
3. compare against a native-curated `accepted_answers` list per card;
4. allow a carefully reviewed typo alias only when the word is long enough;
5. log unmatched answers for review instead of pretending the language has been solved.

Eight demo cards per language make exact curation practical and more impressive than a clever but unsafe general matcher.

### 7.2 Referee evidence

The verifier must see the target and banned list only after submitting the guess. Ask:

> “Did the speaker say the answer or one of these blocked words?”

Two independent `yes` votes produce `VOIDED`. A disagreement stays `REVIEW_REQUIRED`; it should not silently pay or enter the eligible set.

A learner who does not understand the language cannot be treated as a rule referee.

### 7.3 Expiry and cold start

Do not promise a nationwide asynchronous marketplace in the pitch. Launch as a **funded cohort** with enough competent listeners for the chosen language.

If a clip expires without two verifiers:

- label it `UNVALIDATED`;
- keep it out of downstream export;
- show the speaker an honest message;
- decide whether any goodwill payment exists outside the competition economics.

The repo currently proposes half payment on expiry but does not include that acquisition cost in its unit economics. Either model it or omit the promise.

---

## 8. TECHNICAL CORRECTIONS

### Keep

- a React/TypeScript client and one FastAPI modular monolith;
- PostgreSQL as the source of truth;
- private object storage or a simple API upload path;
- integer-cent immutable reward events;
- provider reference persisted before a payment call;
- idempotent resolution and payout requests;
- polling/reconciliation after an HTTP `202`;
- deterministic demo data and reset;
- explicit sandbox/demo/production provider labels.

### Correct or simplify

- A PostgreSQL `CHECK` constraint cannot enforce no-self-guessing across another table. Enforce assignment in the service and back it with an appropriate trigger or relational design.
- Derive an available balance only from posted reward and settlement events. Do not sum pending, failed and paid states as though every ledger row has the same sign.
- FastAPI background tasks are not durable jobs. For the prototype, keep processing synchronous where safe or expose a deterministic admin/demo resolver. Do not imply production durability.
- Direct API upload may be simpler than presigned object storage for short clips. Choose the path with fewer failure points.
- Do not load ML into the request path. Duration, silence, clipping and file integrity are sufficient for the prototype.
- Do not call MoMo settlement “instant” until actual product minimums, bulk-disbursement pricing and South African availability are confirmed.
- Treat exact Mini App bridge names, heartbeat timing and API availability as event-spec configuration, not universal platform facts, until confirmed from the organiser's current documentation.

### Minimal state model

```text
DRAFT
  → RECORDED
  → QUALITY_PASSED
  → OPEN
  → UNDERSTOOD | VOIDED | EXPIRED
  → CORPUS_ELIGIBLE | UNVALIDATED
  → REWARD_CREDITED
  → PAYOUT_SUBMITTED
  → PAID | PAYOUT_FAILED
```

Keep contribution state, reward state and provider settlement state separate in the database even if the UI presents one journey.

---

## 9. BUSINESS AND ETHICS CORRECTIONS

### Do not present the current R/hour model as proven

The cost model is a useful scenario, but its headline “validated ASR hour” is not supported by the product output because the clips do not have transcripts. It also depends on an untested acceptance rate, unconfirmed disbursement fee, listener reward policy, expiry policy and demand for the resulting data.

For the pitch, price the first offer as a **sponsored language mission per accepted semantic contribution**, not as an ASR-ready dataset per hour.

The commercial proof required at the hackathon is smaller:

- a mission has a fixed budget;
- the reward rule is published before play;
- every accepted contribution decrements the budget once;
- contributors see the same rule and receipt;
- MTN could fund a domain deck for voice-intent research.

### Avoid hostile or unprovable MTN framing

Remove or soften these lines from the pitch:

- “the shelf is empty”;
- “MoMo South Africa is on its third launch attempt”;
- “Ayoba failed” as an argument made to MTN;
- “MTN owns no language asset”;
- “MTN is its own first customer” as a fact;
- the 2020 active/registered ratio presented as today's activation rate.

Use:

> “MTN is expanding MoMo from transactions into daily digital services. AMAZWI gives the Mini App ecosystem a repeatable entertainment habit and could make MTN its first design partner for governed voice-intent data.”

That aligns with MTN without lecturing the judges about their own company.

### Consent scopes must be separate

At minimum, distinguish:

1. record and process for this round;
2. play privately to assigned verifiers;
3. retain for governed research or model development;
4. publish audio or attribution publicly.

The fourth scope should be off by default and is outside the prototype. “Contributors retain rights” also requires actual licence terms; it cannot be created by pitch language alone.

### The name and cultural balance

Keep **AMAZWI** for the event if the team likes it, but know the museum collision already documented in `07_TRUTH.md`. Do not imply a partnership that does not exist.

Because the launch is equally Setswana and isiZulu, avoid making every mode and navigation label Nguni. Use neutral functional labels in the shell—**Speak**, **Listen**, **Wallet**, **Impact**—with properly translated language-pack copy. Co-equal languages should look co-equal.

---

## 10. PITCH CORRECTIONS

### The reliable demo comes first

The primary demo should use one speaker device and two known proficient-listener devices. It proves the real product. The room-wide QR game is optional after the golden path is healthy; it should never be the only way the central loop resolves.

If room guests use MCQ, say:

> “This audience round is the learner game. It moves the live popularity score, not the governed corpus decision. Two proficient free-text verifiers make that decision.”

### Open with an artefact the team controls

If using a bad-transcription comparison, record the exact clip yourselves, name the model/version and keep the output reproducible. Do not move between isiXhosa evidence and an isiZulu/Setswana product as though the same benchmark applies to every language.

Prefer these claims:

- off-the-shelf performance remains poor on named published benchmarks;
- existing South African corpora are valuable but do not provide a continuous consumer contribution loop;
- this prototype proves acquisition, semantic verification, consent lineage and reward accounting;
- no model was improved during the event.

Avoid:

- “no system on earth”;
- “no working speech recognition for ten languages” without precise model/task qualification;
- “Google skipped us” as an accusation;
- “no existing corpus has consent lineage”;
- one-hour WER claims without the exact study, model, split and domain;
- universal claims that every South African knows or has played the reference game.

### Close on the receipt, not public exposure

The strongest closing visual is the Voice Value Receipt beside the aggregate Voice Map:

> **“This voice stayed under the contributor's control. The value moved visibly. And the country gained one more governed language signal.”**

That is more defensible than saying the clip is permanently public, named and withdrawable at the same time.

---

## 11. TEAM SONAR — CONFIRMED ROLE SPLIT

Sbu explicitly reversed the earlier default. This split is settled and must be used consistently.

### Sbu — Platform, MoMo and Trust Lead

- final say on money, data integrity and deployment safety;
- FastAPI contract, PostgreSQL schema and state transitions;
- verification resolver, idempotent ledger and provider adapters;
- isiZulu card content and copy quality;
- deployment, reconciliation and technical tests;
- explains architecture, MoMo states, security and feasibility on stage.

### Lethabo — Product, Experience and Demo Lead

- final say on product scope and user journey;
- React UI, recorder interaction, design system and receipt presentation;
- Setswana card content and copy quality;
- demo reset/runbook and fallback video;
- stage opening, game narration and close;
- answers product, culture, inclusion and user-experience questions.

### Shared responsibilities

- agree request/response examples before implementation;
- each person can run the full demo alone;
- both know the one-sentence product and the “what was built here” answer;
- both verify the eight hero cards in their own language;
- either can trigger seeded mode without editing production data;
- scope cuts require both people, but Lethabo breaks product ties and Sbu breaks safety/integrity ties.

If speaking strengths favour a different stage split, change only the speaking segments. Do not reverse code/data ownership during the build.

---

## 12. REPOSITORY RECONCILIATION CHECKLIST

These decisions are accepted. Reconciliation status:

1. ✅ `00_MASTER_PLAN.md`: canonical product, scope, payment, privacy and ownership.
2. ✅ `01_PRODUCT.md`: separate learner/verifier paths, MCQ gameplay only, points-only listeners, aggregate Impact Map.
3. ✅ `02_TECH.md`: semantic label separate from transcript, conservative matching, thin architecture and corrected invariants.
4. ✅ `03_BUSINESS.md`: sponsored missions, pilot economics, cash-out threshold and no ASR-ready-hour pricing.
5. ✅ `04_DESIGN.md`: two-verifier copy and aggregate Impact Map.
6. ✅ `05_BUILD.md`: priority gates without a timeline, thin P0 and swapped role ownership.
7. ✅ `06_PITCH.md`: judge-only flow, positive MTN framing and honest semantic-label story.
8. ✅ `07_TRUTH.md`: data-truth claims, private-by-default ethics and softened model absolutes.
9. ✅ `08_REDTEAM.md`: accepted second-pass findings R24–R28.
10. ✅ `README.md`, mockup sources and reciprocal handover updated.

---

## 13. FINAL GO / NO-GO TEST

AMAZWI is ready to build only when both teammates can answer these identically:

1. What exactly makes a contribution `UNDERSTOOD`?
2. Which users earn cash, and why?
3. What exact data object is produced—semantic label, transcript, or both?
4. Which payment leg is real sandbox, which is simulated, and what is merely roadmap?
5. What happens when only one verifier appears?
6. What does consent withdrawal remove?
7. What is the single P0 demo path?
8. Which features are explicitly not being built?

If any answer differs, stop adding features and reconcile the product. If all eight match and the golden path works after a reset, Team Sonar has a credible, memorable and judge-defensible entry.
