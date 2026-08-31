# AMAZWI — TECHNICAL ARCHITECTURE
### System design · AI engineering · data pipeline · database · security by design · automation

**Parent:** `00_MASTER_PLAN.md` · **Written:** 2026-08-31

> Model-specific figures marked ⟨D⟩ are to be reconciled against `research/D_SPEECH_AI.md`. Do not put a ⟨D⟩ number on a slide until it is confirmed there.

---

## 1. ARCHITECTURAL PRINCIPLES

Six decisions, each of which removes an entire category of failure:

1. **A modular monolith, not services.** Two people, 26 hours. Service boundaries cost more than they return below about five engineers. Modules inside one FastAPI app, with clean seams you could split later.
2. **No queue broker.** No Celery, no Redis, no Kafka. FastAPI background tasks and a `pending_jobs` table. Polling, not WebSockets. Every one of those tools is a thing that can be down at 04:00.
3. **Provider adapters for everything MoMo.** `IdentityProvider`, `ConsentProvider`, `PaymentProvider`, `NotificationProvider` — each with a sandbox implementation and a clearly-labelled demo implementation behind identical interfaces. **The product survives any answer to "which APIs are enabled?"**
4. **The ML lane is offline and never in the request path.** No user action ever blocks on a model. Everything AI is either sub-50ms on-device, or asynchronous.
5. **Audio never touches the API server's filesystem.** Presigned upload straight to private object storage. The API handles metadata and state.
6. **Money is an append-only ledger of integers.** Balances are derived, never stored. This is the single most important decision in the system.

---

## 1A. ⚠️ THE MINI APP HOST CONTRACT — read this before writing any frontend code

MTN's community documentation for the MoMo PWA Mini App is **public** and contains a constraint that will silently destroy this specific product if you miss it.

### What the host gives you
A mini app runs as a web page inside a **React Native WebView** in the MoMo app — MTN's docs call it a **"MicroSite"**, not an Ant/Alipay mini-program runtime. **The user arrives already authenticated.** On load you receive a `START_JOURNEY` event carrying the logged-in `msisdn` and a `micrositeToken`:

```js
window.addEventListener('MoMoWebViewEvent', (payload) => {
  const { event, msisdn } = payload.detail;
  if (event === 'START_JOURNEY') {
    const token = window.micrositeToken;
    startYourApplication(token, msisdn);
  }
});
```

There is no SDK package. The entire bridge is that `CustomEvent` plus `window.ReactNativeWebView.postMessage(JSON.stringify({...}))`. Event vocabulary: `START_JOURNEY` (received) · `IS_STILL_ACTIVE` · `AWAITING_FOR_APPROVAL` · `APPROVED` · `REJECTED` · `DONE` · `ERROR`.

### 🔴 The constraint that matters — a 60-second inactivity timeout

> **"The micrositeToken is valid for 10 minutes."**
> **"If no activity (no heartbeats) occurs within 10 minutes, the session ends and the user must restart."**
> **"Actual timeout is 60 seconds, providing a 10-second buffer. Recommended sending interval: every 45–50 seconds."**
> **"At 9 minutes, restart the journey to obtain a new valid token."**

**Only `IS_STILL_ACTIVE` resets the timer.** `AWAITING_FOR_APPROVAL`, `APPROVED` and `REJECTED` do not.

```js
function sendHeartbeat() {
  window.ReactNativeWebView.postMessage(JSON.stringify({
    event: 'IS_STILL_ACTIVE', micrositeToken: window.micrositeToken
  }));
}
const heartbeatInterval = setInterval(sendHeartbeat, 50000);
```

**Why this is existential for AMAZWI specifically.** Our core interaction is: read a card, think, record for 30 seconds, review, submit. That is a user who is *busy but not tapping* for a minute or more at a time. **Without the heartbeat the session dies mid-recording**, and it will die on stage, in front of judges, during the one moment that matters.

**Build the heartbeat at G0, not later.** It is fifteen lines and it is the difference between a demo and an incident. Add the 9-minute token refresh at the same time.

### What is NOT documented — ask the mentors on day one
- **Design standards and any CSP allowlist.** The programme page promises them; no reachable page renders them. Building against an unknown CSP is a real risk if you load external fonts or assets. *(This is a further argument for the self-hosted, 200 KB, zero-external-request design in `04_DESIGN.md`.)*
- **The review/approval process.** Not documented for the Mini App programme. The sibling Interact product uses a manual Partner Portal review with revision cycles — so a hackathon prototype almost certainly will **not** clear real MTN review inside the event. **Plan to demo in a simulator or a plain mobile browser**, and say so.

---

## 2. SYSTEM DIAGRAM

```
┌──────────────────────────────────────────────────────────────┐
│  MoMo Mini App — React 18 + TypeScript + Vite (PWA)          │
│                                                              │
│  Speaker · Listener · Wallet · Receipt · League · Archive    │
│  Impact Console                                              │
│                                                              │
│  Web Audio API (AnalyserNode)   IndexedDB outbox queue       │
│  ├ live waveform                ├ survives refresh           │
│  └ TIER-0 quality gate          └ retries upload             │
└─────────────────────────┬────────────────────────────────────┘
                          │ HTTPS / JSON · typed client from OpenAPI
┌─────────────────────────▼────────────────────────────────────┐
│  FastAPI modular monolith                                    │
│                                                              │
│   sessions & consent   │  card engine (coverage-ranked)      │
│   submission lifecycle │  guess assignment + agreement       │
│   latent-trait scorer  │  reward ledger + payout orchestration│
│   league / archive     │  impact aggregation                 │
│   audit                │  admin: seed / reset                │
└────────┬──────────────────────────────┬──────────────────────┘
         │                              │
┌────────▼─────────┐          ┌─────────▼──────────┐
│  PostgreSQL 16   │          │  Private object     │
│  state, ledger,  │          │  storage — audio    │
│  consent, audit  │          │  presigned URLs only│
└──────────────────┘          └────────────────────┘
         │
┌────────▼─────────────────────────────────────────────────────┐
│  PROVIDER ADAPTERS   Identity │ Consent │ Pay │ Notify        │
│  each: sandbox impl · labelled demo impl · identical states   │
└──────────────────────────────────────────────────────────────┘
         │
┌────────▼─────────────────────────────────────────────────────┐
│  ML LANE — offline, Kaggle, never in the request path         │
│  corpus export → clean → fine-tune → evaluate → report        │
└──────────────────────────────────────────────────────────────┘
```

### Repository
```
/apps/web          React PWA
/apps/api          FastAPI
/packages/contracts  OpenAPI + generated TS types
/ml                pipeline notebooks + eval harness
/infra             docker-compose, deploy config
/demo              seed data, reset script, fallback video
```

**Contract ownership:** PLATFORM owns the OpenAPI document. EXPERIENCE consumes generated types. **Neither invents a field independently** — this is the rule that prevents 04:00 integration failure.

---

## 3. THE DATA MODEL

### 3.1 Core entities
```sql
user                id · momo_subject_ref · adult_confirmed_at · status · created_at
language            code · name · endonym · active
user_language       user_id · language_code · role(SPEAKS|LEARNING) · theta
consent_version     id · version · purpose · body_text · effective_from
consent             id · user_id · consent_version_id · status · granted_at · revoked_at
card                id · language_code · target_word · banned_words[]
                    · accepted_answers[]  ← REQUIRED, see §3.4
                    · distractors[]       ← the 3 wrong MCQ options
                    · is_gold · gold_expected_flag
                    · beta · topic · status
round               id · card_id · speaker_id · language_code
                    · published_reward_cents · state · created_at
recording           id · round_id · storage_key · duration_ms · rms_dbfs · peak_dbfs
                    · clip_ratio · silence_ratio · sha256 · state
guess               id · round_id · listener_id · answer_text · is_correct
                    · input_mode(MCQ|FREE_TEXT)   ← only FREE_TEXT validates corpus
                    · said_banned_word BOOLEAN    ← the referee tap, §1.1 of 01_PRODUCT
                    · latency_ms · created_at
ledger_entry        id · user_id · kind · amount_cents · round_id · guess_id
                    · idempotency_key · created_at
payout              id · user_id · amount_cents · x_reference_id · state
                    · provider_ref · created_at · resolved_at
audit_event         id · actor · action · subject_type · subject_id · payload · created_at
```

### 3.2 The constraints that are the actual product

These are not hygiene. Each one is a failure mode a judge will probe.

```sql
-- Money is integers. Never float, never numeric-in-application.
amount_cents BIGINT NOT NULL

-- Exactly one reward per contribution per person. Enforced by the
-- database, not by application logic, because application logic
-- loses races and databases do not.
CREATE UNIQUE INDEX ON ledger_entry (kind, round_id, user_id);

-- One decision per assignment.
CREATE UNIQUE INDEX ON guess (round_id, listener_id);

-- No self-guessing. Enforced at assignment AND asserted here.
ALTER TABLE guess ADD CONSTRAINT no_self_guess CHECK (...);

-- Idempotent payout: the X-Reference-Id is generated and PERSISTED
-- BEFORE the provider call, so a crash mid-call cannot double-pay.
CREATE UNIQUE INDEX ON payout (x_reference_id);

-- Exact-duplicate audio cannot be submitted twice.
CREATE UNIQUE INDEX ON recording (sha256);
```

**Balances are derived:**
```sql
SELECT COALESCE(SUM(amount_cents), 0) FROM ledger_entry WHERE user_id = $1;
```
Never a `balance` column. A stored balance is a bug waiting for a race condition, and "show me how you compute the balance" is exactly the question a fintech judge asks.

### 3.4 🔴 `is_correct` — the load-bearing function nobody had defined

Every downstream number — the reward, the clarity score, the proficiency estimate, the corpus label — is a function of one boolean, and it had no definition. For agglutinative Nguni languages this is not a detail. For the card *isithuthuthu* (motorbike), honest listeners will type: `isithuthuthu` · `sithuthuthu` · `izithuthuthu` · `sthuthuthu` · `motorbike` · `i-motorbike`. Exact match rejects most of those. Edit distance over noun-class prefixes produces false positives *and* false negatives. And every tool that would help is unavailable — no ASR, no lemmatiser, MMS-LID licence-barred.

**Specify it per card, not per language. Fifteen lines:**
```
1. Normalise: lowercase; strip a whitelisted set of noun-class prefixes for that
   language (i-, isi-, izi-, ama-, ubu-, se-, le-, ma-); collapse whitespace,
   hyphens and apostrophes. Preserve meaning-bearing diacritics.
2. Match against card.accepted_answers[] — the target plus every native-checked
   synonym, morphological variant, and common code-switched English equivalent.
3. Levenshtein <= 2 against any accepted answer, post-normalisation, for typos.
4. Everything else is false.
```

⚠️ **`accepted_answers[]` is captured during Monday's card-content job.** Three extra minutes per card, with the first-language speaker already on the phone. **Add the column tonight** or that job needs a second pass you do not have time for. Nothing else you can build buys this much accuracy per hour.

**For the demo, ship MCQ as the primary listener input** — deterministic, fast, and it cannot fail on stage. Free text is the advanced mode, and it is the only mode that validates the corpus (`01_PRODUCT.md` §4).

### 3.3 State machines

```
ROUND     DRAFT → RECORDED → QUALITY_PASSED → OPEN → RESOLVED → REWARDED
                          ↘ QUALITY_FAILED      │  ↘ VOIDED   (both listeners
                                                │              reported a banned
                                                │              word: no speaker
                                                │              reward, listeners
                                                │              still paid)
                                                ↘ EXPIRED  (48h, fewer than two
                                                            guesses: pay half
                                                            anyway, mark
                                                            UNVALIDATED, exclude
                                                            from corpus export)

LEDGER    PENDING → AVAILABLE → PAYOUT_PENDING → PAID
                        ↑                    ↘ PAYOUT_FAILED
                        └────────────────────────┘

PAYOUT    CREATED → SUBMITTED → PENDING → SUCCEEDED
                                       ↘ FAILED
```

**The rule that matters:** a provider returning `202 Accepted` means *submitted*, not *paid*. `PAYOUT_PENDING` is not `PAID`. The UI must never conflate them, and a failed payout returns the money to `AVAILABLE` — it does not vanish.

### 3.5 🔴 `EXPIRED` — the state that keeps the wallet honest at low liquidity

**Without it, the whole loop has a silent failure mode.** A Tshivenda clip recorded on a Tuesday in Thohoyandou sits `OPEN` forever if no Tshivenda speaker is online, and its published reward sits `PENDING` forever — on the screen you have promised must never lie. That is not an edge case at launch; **it is the normal case**, and the demo hides it completely because 52 people in one room at one instant is the most favourable matching condition that will ever exist.

**Three rules:**
1. **48-hour timeout → `EXPIRED`.** The published reward is **paid anyway, at half**, funded as an acquisition cost, with an honest message:
   > *"Not enough Tshivenda listeners yet. We paid you anyway. We're going to go and find them."*
2. **Minimum two guesses to validate, always.** If two never arrive, the clip pays but is marked `UNVALIDATED` and **excluded from corpus export.** Never resolve on one — a single listener is not agreement, and it makes collusion cost exactly one friend.
3. **Cap the coverage multiplier by pool size, not by coverage alone.** Multiplier ≤ 1.0 until a language has ≥ 50 active listeners.

That third rule closes an incentive the earlier design had backwards. The probability that a chosen confederate lands among a clip's assigned listeners is ~0.3% in a pool of 1,000, ~6% in a pool of 50, and **~43% in a pool of 8** — while the coverage multiplier paid *up to 2.5×* precisely for the thinnest pools. **You were paying the most exactly where collusion was nearly free.** One line fixes it.

> Paying an expired clip anyway is a better story than any fraud control: *"we'd rather pay someone for speech we can't yet validate than leave a promise unpaid on their screen."*

---

## 4. THE SCORING ENGINE

### 4.1 It is Elo, for how clearly you speak

The model from `01_PRODUCT.md` §3 — a latent-trait formulation where every guess updates three parameters:

```
p = σ(θ_listener − β_card + γ_speaker)

on observing outcome y ∈ {0,1}:
    err      = y − p
    θ_l  +=  k_l · err        listener got better/worse than expected
    γ_s  +=  k_s · err        speaker was clearer/less clear than expected
    β_c  -=  k_c · err        card was easier/harder than expected
```

Learning rates decay with observation count — exactly Elo's K-factor — so early estimates move fast and settle. Clamp every parameter to a sane range. Three floats per row, one update per guess, no training job, no GPU. It runs in the request handler in microseconds.

**Why this is worth the twenty lines it costs:**
- It answers *"who failed?"* fairly, so payment is defensible.
- It converts the learner side from a cost into a calibration asset.
- It produces a **language proficiency estimate** as a by-product — see `03_BUSINESS.md`.
- It is standard psychometrics (Rasch / 2-PL item response theory), not invented mathematics, and you can name it.
- **You can explain it in one sentence:** *"It's Elo, but for how clearly you speak."*

### 4.2 🔴 THE CONVERGENCE CONSTRAINT — write this down before someone "improves" it

The Elo approach is well established in adaptive learning, **but it has a documented failure mode that we sit one design decision away from:**

> **"In scenarios where items are selected adaptively based on the current ratings and the item difficulties are updated alongside the student abilities, the variance of the ratings across items and students artificially increases over time and as a result the ratings do not converge."**
> — *Keeping Elo alive: Evaluating and improving measurement properties of learning systems based on Elo ratings* · `research/F_GAMIFICATION.md` §6

**In plain terms: if you both (a) choose which card to serve based on its estimated difficulty and (b) keep updating that difficulty, the estimates diverge instead of settling.**

**We are safe only by accident.** Our card selection is driven by **coverage need** — which language and speaking style is under-represented — which is independent of the player's ability. That is not the failure condition. But it is one plausible "improvement" away from being one.

**The four rules:**
1. 🔴 **Never select cards by estimated difficulty while difficulty is still being updated.** If adaptive difficulty is ever added, **freeze β first.**
2. **Anchor β on gold cards and freeze it there.** Gold cards have known difficulty and must not float.
3. **Decay K with observation count.** Fixed K forces a trade-off — large K tracks change but is volatile, small K is stable but slow. Dynamic-K approaches are published.
4. **Cold start is a studied problem** with published mitigations; seed with gold items of known difficulty.

> **The line for a technical judge:** *"It's Elo, with difficulty anchored on gold items and a decaying K — because the literature shows that if you adaptively select on difficulty while also updating it, the ratings don't converge."* That demonstrates we read past the first result.

### 4.3 Cold start and honesty
With no data every parameter sits at its prior. θ and γ are not separately identifiable without anchors — anchor on gold cards and high-volume listeners.

**Never call the proficiency number a certified level in the demo.** It is *an estimate*, until it has been correlated against an external instrument.

---

## 5. AI ENGINEERING — five tiers

The organising principle: **push work to where it is cheapest and least likely to fail.** Nothing user-facing waits on a model.

### TIER 0 · On device, no model at all — the highest-value tier
Pure Web Audio API. Runs *before upload*, costs nothing, and saves the contributor's data:

| Check | Method | Reject when |
|---|---|---|
| Duration | timer | < 3s or > 35s |
| Loudness | RMS → dBFS over frames | mean < −45 dBFS ("speak up") |
| Clipping | \|sample\| ≥ 0.99 ratio | > 1% of samples |
| Silence | frame energy below floor | > 70% of the clip |
| Dead mic | all-zero buffer | any |

> **This tier is a design statement, not an optimisation.** In a country where a gigabyte costs what it costs, uploading a clip you already know is unusable is taking money from the contributor. Say that on stage.

### TIER 1 · On device, tiny model
**Silero VAD v5, ONNX, ~2 MB, MIT** — speech present, and where. Trims leading and trailing silence client-side, cutting upload size materially. Lazy-loaded, cached by the service worker.
> **Not browser Whisper.** In-browser ASR is a large download for a result no user needs before upload, in languages no model transcribes anyway. Skip it.

### TIER 2 · Server, fast
| Job | Model | Licence |
|---|---|---|
| Exact duplicate | SHA-256 of normalised audio, unique index | — |
| Near duplicate / replay | Landmark spectral fingerprint | MIT |
| Speaker **uniqueness** (never auth) | ECAPA-TDNN VoxCeleb | ⚠️ weights Apache-2.0, **corpus is not** — see below |
| Spoof / TTS risk score | **AASIST-L**, 85k params | MIT |
| Language ID | ⚠️ **Train your own** — see below | — |

⚠️ **Anti-spoofing degrades from ~0.83% to ~25% EER out of domain**, and phone audio is exactly the codec-compressed narrowband condition that degrades it most. **It is a risk score routed to human review. It never auto-rejects.** Fraud defence must be behavioural and fingerprint-first, model-second.

⚠️ **The ECAPA licence problem is one layer down, and it is the one a careful judge finds** — precisely because you made licence purity a pitch point. The **weights** are Apache-2.0; **VoxCeleb itself is CC BY-NC-SA 4.0**, and the commercial status of a model trained on it is unsettled.
> **Cleanest fix: drop speaker-uniqueness from the competition build entirely** — it is not on the demo path. If you keep it, footnote it honestly: *"weights are Apache-2.0, the training corpus is non-commercial; we'd retrain on licensed data before shipping."* Having audited MMS and SeamlessM4T for exactly this and missed it one level down is worse than not raising licences at all.

⚠️ **Language ID is a genuine gap.** MMS-LID is **CC-BY-NC** and cannot ship commercially. VoxLingua107-ECAPA (Apache-2.0) covers Afrikaans but has **no Nguni or Sotho-Tswana languages at all**. A small classifier trained on Swivuriso + NCHLT is the only viable path.

### TIER 3 · Server, asynchronous
Quality/MOS via **DNSMOS P.835 (MIT)** — ⚠️ **not NISQA, whose weights are CC-BY-NC-SA despite an MIT repo badge.** Transcription assist for Afrikaans only (see below). Forced alignment for read-prompt modes.

### TIER 4 · Offline, Kaggle
Corpus export → clean → fine-tune → evaluate. **Never on the demo path.** Full 60-GPU-hour budget in `research/D_SPEECH_AI.md`.

### 5.1 THE FINDING THAT SHAPES THE WHOLE PITCH

**There is no working off-the-shelf ASR for ten of South Africa's eleven spoken official languages.** Not weak — non-functional. Whisper large-v3-turbo scores **146.30% WER zero-shot on Southern Bantu languages and 223% on Setswana.** (Error rates exceed 100% because insertions count.) Only Afrikaans has a usable baseline.

This is better news than it sounds, because it makes the honest claim the strong one:

> **"We validate that a submission is real, audible, unique, human-sounding speech of adequate quality — before a cent is paid for it. We do not claim to transcribe it, because no system on earth transcribes isiZulu reliably today. That is the gap we are collecting the data to close."**

That survives a technical judge. A faked transcription demo does not.

**And the number that justifies the entire product:** roughly **one hour** of in-domain data takes isiZulu from ~146% WER to about **23–28%**; fifty hours reaches about **8%**. *(NCHLT-based, arXiv 2512.10968.)* One hour of speech is worth an enormous amount when the baseline is broken — which is exactly the argument for paying people to produce it.

### 5.2 Model stack for fine-tuning (Track B)
Architecture split, and it is measured, not preference — about 3–4 WER points each way:
- **Nguni** (isiZulu, isiXhosa, siSwati, isiNdebele) → **w2v-bert-2.0**, 600M, MIT + LoRA
- **Sotho-Tswana and Afrikaans** → **whisper-large-v3-turbo**, 809M, MIT + LoRA

⚠️ **Excluded on licence grounds for a commercial pitch:** MMS-1B-all, MMS-LID, SeamlessM4T (all CC-BY-NC-4.0), NISQA weights (CC-BY-NC-SA-4.0). Fine for internal research; **none may ship in a product.** The earlier submission drafts named some of these — correct that.
⚠️ **The T4 has no bf16.** Copying Swivuriso's published training config verbatim will fail on Kaggle. Budget a one-hour timing calibration run before anything else.

### 5.3 Active learning — the honest correction
The earlier plan made active learning a centrepiece. **The literature does not support that, and a judge who knows the field will.** Uncertainty-based selection can *underperform random sampling* for ASR, because uncertainty correlates poorly with WER and tends to select from small clusters, reducing diversity. Hybrid uncertainty-plus-diversity does better.

**It is not honestly demonstrable in a hackathon.** Proving strategy X beats random at equal budget needs multiple runs, multiple seeds, and a test set large enough for statistical power. You will not have it.

> ✅ **Build the mechanism, demo the queue, and say:** *"the selection policy is in place; whether it beats random selection is an open question we haven't powered a study to answer."* That is more impressive to a good judge than an unfalsifiable claim.

### 5.4 The one honesty rule
**Word error rate only moves after a real training run against a fixed test set with a named model version.** In 26 hours you can show acquisition, validation, coverage and consent. Any external benchmark shown must be labelled external, with source and date. And before claiming any improvement, three gates: **Mann-Whitney p<0.05 · bootstrap 95% CI excluding zero · Cliff's delta reported.** If any gate fails, the answer is "no significant difference" — and reporting that null result is more credible than a wall of wins.

---

## 6. THE DATA PIPELINE — how raw speech becomes ML-ready

Six stages. This is the answer to *"how do you clean and prepare it?"*

**STAGE 1 · CLIENT, pre-upload**
Opus @ 16 kHz mono. Tier-0 gates. VAD trim. **Nothing that will be rejected is ever uploaded.**

**STAGE 2 · INGEST**
Presigned PUT direct to private storage under a random, unguessable key. SHA-256 computed and deduplicated. Size and content-type validated. Metadata row created. Audit event written.

**STAGE 3 · AUTOMATED QA (async)**
Resample to 16 kHz. **Loudness-normalise to −23 LUFS (EBU R128)** — store as a *derived* artefact and **keep the original**. Estimate SNR. Predict quality ⟨D⟩. Run language ID and spoof detection. Attach all scores.

> ⚠️ **Do not denoise for the training corpus.** Denoising introduces artefacts and removes exactly the acoustic conditions a South African ASR model needs to be robust to — taxi ranks, wind, cheap microphones. Denoise only for playback if a listener needs it. This is a mistake most teams make and it is worth saying out loud.

**STAGE 4 · VALIDATION**
Agreement from independent guesses. Clarity score updated. Gold-standard honeypots checked. Outliers flagged.

**STAGE 5 · CURATION**
Consent status re-checked **at curation time, not just at collection time**. Quality threshold applied. Coverage tags assigned (language, style, region band, topic).

**Split assignment — and this is where most speech projects quietly ruin themselves:**
> **Splits must be speaker-disjoint.** If the same speaker appears in train and test, your WER is fiction and it will be flattering fiction. Assign every speaker to exactly one of train/dev/test, permanently, at first contribution.

**STAGE 6 · EXPORT**
Parquet / HuggingFace `datasets` format, plus a manifest carrying **consent lineage per row** — consent version, status, timestamp. Revoked contributions are filtered at export. That manifest is what makes the corpus licensable rather than merely academic, and it is the thing no existing African speech corpus has.

---

## 7. SECURITY BY DESIGN

Not a checklist appended at the end — a set of decisions that constrain the architecture.

### 7.1 Identity and personal information
- **No identity document is ever stored.** Identity comes from MoMo; you keep an opaque subject reference.
- **The MoMo reference lives in a different table from the recordings**, joined only where needed. Voice and identity are separable by design.
- **Adults only.** Voice recordings are personal information under POPIA; children's data carries additional restrictions. The age gate is a legal control, not UX.
- **No precise location.** Province or ward band only. Precise location plus voice plus a wallet reference is a re-identification kit.

### 7.2 The biometric line — the most important security decision
> **Voice is the interface. It is never the lock.**

Speaker embeddings may be used for **uniqueness** (one human, one account). They must **never** be used for authentication. Two reasons, both defensible on stage:
1. Voice cloning defeats speaker verification at high rates on modest amounts of scraped audio.
2. Under POPIA, biometric processing for identification is *special personal information* with a materially higher compliance burden. Choosing not to do it is the correct engineering decision and the correct legal one.

### 7.3 Audio access
Private buckets. No public URLs, ever. Listeners receive a **short-lived presigned URL scoped to the round they were assigned** — never a bucket path, never a permanent link. Encryption at rest and TLS 1.3 in transit.

### 7.4 Money integrity
Secrets server-side only — the PWA never sees a MoMo key. `X-Reference-Id` generated and persisted **before** the provider call. Webhooks verified and **idempotent**, because callbacks are delivered more than once and a naive handler pays twice. Polling *and* callback, reconciled to the same payout row. Rate limits per user, per device, per IP. Campaign budget checked before any reward is committed.

### 7.5 Consent as an enforced control
Consent is checked at three points, not one: **before a round starts**, **before a recording is served to a listener**, and **before corpus export**. Revocation blocks new contributions and excludes existing recordings from future exports and training runs.

Say the hard part plainly: **you cannot un-train a model that has already seen the data.** Handle it with a declared retirement and retraining policy. Anyone promising instant unlearning is misleading you, and a judge who knows this will respect you for saying so.

### 7.6 Logs and audit
Structured JSON. **Never log MSISDNs, tokens, or subject references.** An audit event for every submission, guess, reward, payout, consent change and revocation — actor, action, subject, timestamp.

---

## 8. AUTOMATION

| What | How | Why it earns its keep |
|---|---|---|
| CI on every push | GitHub Actions: lint, typecheck, tests | Catches the 04:00 mistake at 04:01 |
| **Ledger property tests** | Hypothesis: generate random sequences of approvals, retries, duplicate callbacks and payout failures; **assert money is conserved and never duplicated** | This is the single highest-value test in the project and it is the answer to "how do I know your ledger is right?" |
| Contract types | Generate TS types from OpenAPI in CI | Makes field drift impossible |
| **Seed / reset** | One command, deterministic | The demo must run twice in a row with no manual DB edits |
| Bundle size gate | Fail CI above 200 KB | Turns the design principle into an enforced constraint |
| Migrations | Alembic, forward-only | No hand-edited schemas at 05:00 |

---

## 9. THE STACK

**Ship with this. Nothing else.**

| Layer | Choice | Why |
|---|---|---|
| Frontend | React 18 + TypeScript + Vite | Fast, known, small |
| PWA | Hand-written service worker | Workbox is more than you need |
| Audio | Web Audio API + MediaRecorder → Opus | Native, zero dependency |
| Offline | IndexedDB outbox | Survives refresh and bad signal |
| Backend | Python 3.12 + FastAPI + Pydantic | OpenAPI for free |
| DB | PostgreSQL 16 | Constraints are the product |
| Storage | S3-compatible, private | Presigned URLs |
| Async | FastAPI background tasks + `pending_jobs` | No broker to fail |
| Deploy | Cloudflare Pages / Vercel + a container | Instant redeploys |
| Callbacks | Cloudflare Tunnel | Stable during the event |

**On the roadmap slide, not in the build:** Celery · Redis · Kafka · TimescaleDB · MLflow · DVC · W&B · Terraform · Kubernetes.

> Naming tools you did not run is the fastest way to lose Technical Execution. A judge who asks *"show me the Celery worker"* and finds none has stopped believing everything else. **The list of technologies in the submission form should match what is actually running**, with future work explicitly labelled as future.

---

## 10. WHAT COULD BREAK, AND THE ANSWER

| Failure | Mitigation |
|---|---|
| iOS Safari audio quirks | Test on a real iPhone Monday. Android is primary; know the iOS behaviour before the room finds it. |
| Mic permission denied | A written, human recovery screen with per-browser instructions. |
| Conference wifi kills the webhook | Poll as well as callback. Both reconcile to the same payout row. |
| Sandbox down | Labelled demo provider, identical state machine. |
| Callback delivered twice | Idempotent handler keyed on `X-Reference-Id`. Property-tested. |
| Fewer than two listeners available | ⚠️ **Never resolve on one.** A single multiple-choice listener guessing at random accepts a meaningless clip **25%** of the time. Hold the round `OPEN` and show the speaker an honest *"still waiting for a second listener"*; in demo mode seed a synthetic listener, clearly labelled on screen. |
| Someone submits a 30-second silence | Tier 0 rejects it before upload. |
| Someone uploads TTS | Spoof flag → held for review, not auto-rejected. |
| Two users record identical audio | SHA-256 unique index rejects the second. |
