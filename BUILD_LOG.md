# BUILD LOG
Newest entries at the top. One entry per working session.

---

## 2026-08-15 — Session 3: Moonshot reset
**Days to hackathon: ~18**

### The trigger
Lethabo's verdict on the 33 concepts: *"these are somewhat generic... I want out of this world stand out."* Specifically called out as missing: resilience when the phone is lost or stolen, no smartphone, no data, no network, load shedding, South African language, and any use of 2026 technology — AI agents, autonomy, forecasting, computer vision, ML engineering.

**That verdict is correct.** Every one of the 33 is structurally *a screen that moves money*, and every one dies when the phone is stolen, the data runs out, or the user doesn't read English.

### Done
- Four parallel research sweeps: SA/African language AI · offline payment technology · SA 2026 hard statistics · agentic AI, voice AI and applied ML. ~150 sources. All logged in `INFO_LOG.md` Session 3 with confidence markings.
- New file: **`02_ideas/MOONSHOTS.md`** — sits *above* `IDEAS_BOARD.md`, does not replace it.
- One flagship (**UMOYA**) plus five alternative moonshots, scored.
- Full failure-scenario table: every objection has a documented answer.

### Seven findings that reset the brief
1. **The SA language barrier just became crossable, and the window is open now.** Google Cloud STT gets isiXhosa wrong **56.71%** of the time on real conversational speech (human: 9.6%); foundation models score **>100% WER zero-shot** on all six Southern Bantu languages. **But the Swivuriso corpus released 3,016 hours across 7 SA languages under CC BY 4.0** and fine-tuning took Setswana from 223% → 13% WER. **Google's Feb 2026 WAXAL push covers 27 African languages and zero South African ones.** Nobody has productised this.
2. **Theft is now a financial crime and it is vertical.** SABRIC 2025: **R2.4bn digital banking crime (+29.2%)** vs **R630,000 from physical bank robberies** — roughly 3,800:1. Banking app fraud is **88.6% of all cases**. **Express kidnapping — abduct someone to force transfers — is up 264%, running at ~53/day**, with ~80% of Gauteng kidnappings tied to armed robbery.
3. **The phone is the least reliable object in a South African's life.** 16% of connections are feature phones; **MTN SA sold 29% 2G devices in 2023/24**; the poor pay **3.5× more per GB**. *Correction: neither MTN nor Vodacom has announced a 2G/3G sunset date — MTN plans to retain a 2G layer, and 2G will outlast 3G.*
4. **Voice biometrics is a trap.** Cloning bypasses speaker verification **82.7%** of the time on 10–30 minutes of scraped audio. Several teams will pitch "log in with your voice" and lose to one question.
5. **Offline payments are buildable — Android HCE, no secure element, no network — but double-spend can only be bounded, never prevented.** The Fed published the canonical framework in Dec 2025. MTN already ships hardware NFC offline via VeryPay in Uganda at pilot scale.
6. **MTN killed Ayoba on 20 March 2026.** 35m MAU, lost on retention. The judges have just lived through a super-app failure caused by the absence of a reason to open the thing. MTN's 2026 AI posture is data centres and a Microsoft licensing deal — **no shipped consumer AI product.**
7. **⚠️ LOAD SHEDDING ENDED 16 MAY 2025** — 441 days clear as at 4 Aug 2026. **Do not claim it.** *Load reduction* has not ended: Eskom still cuts overloaded township feeders 05:00–09:00 and 17:00–22:00, unannounced. Claim that instead, and cite it.

### The core inversion
> Every fintech in Africa builds **for the phone**. Put the money intelligence in the **network** instead, and the phone becomes optional. **MTN is the only organisation in South Africa that can do this** — you have to own the network to live inside it.

### The flagship: UMOYA
An AI money agent living on MTN's network, reachable five ways — **voice call, USSD, mini app, SMS, offline NFC tap** — with one identity and one balance. Works on a R149 Nokia, in isiZulu, with no data, with no network, and survives the phone being taken at gunpoint.

Five capabilities: **Speak** (Swivuriso-tuned ASR + code-switching) · **Survive** (duress PIN with decoy balance, silent alert, graph-based recovery) · **Act** (Get Consent mapped onto AP2 mandate structure) · **Foresee** (usage-periodicity forecasting pointed at the *user*, not at a lender) · **Endure** (HCE signed tokens, capped and time-boxed).

Scales across 16 markets by swapping the language model — Nigeria, Uganda and Ghana are all covered by WAXAL.

### Decisions taken (Session 3b)
- ✅ **UMOYA is locked in its entirety as the primary entry. Track 1 — Everyday Essentials.** Every demo scene is a Track 1 scene: prepaid electricity, data, bills, family transfers. Track 3 would have been a reach, and reaching is worse than choosing.
- ✅ **Name resolved: UMOYA, tagline "even if."** *Umoya / moya* is a shared Bantu root running through **both** Nguni (isiZulu, isiXhosa, siSwati, isiNdebele = 45.2%) **and** Sotho-Tswana (Sesotho, Setswana, Sepedi = 26.1%) — **~71% of South Africans hear their own word.** NOMA rejected: it is isiZulu-specific (isiXhosa uses *okanye* / *nokuba*), so it inherits exactly the exclusion problem Lethabo flagged. ⚠️ Sotho-Tswana forms need native-speaker sign-off before going on a slide.
- ✅ **Team strategy: three members, three tracks, one thesis.** Two sibling entries designed to Umoya's depth → `02_ideas/THE_THREE_ENTRIES.md`
  - **AMAZWI** (Track 2) — the game where young South Africans are paid in MoMo, cents at a time, for their language. Google's Feb 2026 WAXAL release covered 27 African languages and **zero** South African ones; MTN has bet publicly on AI with no African-language data asset, and has had no youth product since Ayoba died in March. Active-learning acquisition loop, consent via Get Consent, uniqueness via Identify. **Feeds Umoya's voice engine — entry #2 is entry #1's supply chain.**
  - **HAMBA** (Track 3) — from *hamba kahle*, "go well." Pay for your journey, escrow releases on arrival, and **the network watches the trip by cell-tower handover** — no app, no GPS, no data. Express kidnapping up 264%, ~53/day, 44% tied to hijackings. **The purest only-MTN idea in the project: nobody without the radio network can build it.**

### ⚠️ NEW BLOCKING RISK
The T&Cs describe teams of ≤4 **or** individuals, one track per submission. **Three people registering individually under one team name is ambiguous** and could be read as one team submitting three entries. **Ask the organisers in writing this week.** If disallowed, fall back to Umoya alone and the other two become the "where this goes next" slide.

### Next session
1. **Send the organisers all three questions in one email:** (a) may three teammates each submit in a different track under a shared team name? (b) is judging per-track or overall? (c) the pre-building clarification, open since Session 1.
2. Prototype-test an AI voice agent over a real GSM call. **No published study covers this.** Know by day three.
3. Ask the MoMo dev community immediately whether *any* tower or SIM signal is exposed, even simulated — Hamba and Umoya both depend on the answer.
4. Native-speaker sign-off on the *moya* claim.
5. `South Africa-Umoya` team name + three 250-char summaries.
6. MoMo sandbox credentials + the gated PWA Mini App design spec.
7. **Agree the day-10 kill rule now:** three entries at 60% loses to one at 95%.

---

## 2026-08-15 — Session 2: Wide ideation
**Days to hackathon: ~18**

### Plan change (important)
Lethabo confirmed: **team assembled**, and the intention is to **build from registration through to 2 September**, using demo day for polish, mentor feedback, UI and the presentation.

**This raises the ambition ceiling substantially.** Stop optimising for "buildable in 24 hours." Optimise for *"nobody else in the room could build this in a day — and we already have."* The 24-hour teams will all ship a single-screen payment demo.

### ⚠️ OPEN RISK — resolve this week
The 2026 T&Cs state all work must be **created during the hackathon**; pre-existing projects prohibited **unless organiser-approved**. But the registration form requests a **GitHub/repo URL** and a **detailed project description** — which implies pre-work is expected.

**Action:** get written clarification from the organisers (email or MoMo Dev Community post). Keep the reply. Regardless of the answer: honest commit history, and a README stating what existed at registration vs what was built on the day.

### Done
- Generated **33 concepts** across all three tracks → `02_ideas/IDEAS_BOARD.md`
- Scored all 33 against the official criteria plus three of our own (launch-partner, weekly-open, only-MTN)
- Additional research: SA e-hailing cash data, gig economy sizing, ticketing, gaming, youth economy

### New research findings
- **Over 80% of South African ride-hailing trips are paid in cash** (Bolt, Apr 2026) — vs 85%+ cashless in Nigeria. Cash = 56% of all SA consumer transactions by volume.
- SA gig economy: **1.8–2m participants, $5.03bn**, ride-hailing 29% of it. 70% use it to supplement other income; most cannot prove what they earn.
- SA esports/gaming on a path to **$12.9bn by 2032**.

### Recommendation reached
**Primary: SETTLE + CHANGE as a single Track 3 entry.** Both convert cash-in-hand into wallet balance at the moment of a transport transaction — the point where SA's cash economy renews itself daily. Settle is the beachhead (verified 80% cash problem, no taxi-association politics); Change is the vision (coins, not fares, as the wedge into the minibus economy). Together they're a thesis, not a feature.

Backups: **GIFT** (Track 2, whitest space, MTN is the merchant), **SHAYA** (best live demo), **SHIELD** (strongest moat), **NKOSI** (most resonant).

### Next session
1. Lock track + concept
2. User journeys (passenger + driver)
3. Screen-by-screen API mapping
4. 250-char summary + detailed description for registration
5. Repo + MoMo sandbox credentials
6. Organiser answer on pre-building

---


---

## 2026-08-15 — Session 1: Intelligence gathering
**With:** Claude (Cowork) · **Duration:** research sprint · **Days to hackathon: ~18**

### Done
- Established project folder structure and doc system (`MASTER_CONTEXT`, `BUILD_LOG`, `INFO_LOG`, `01_research`, `02_ideas`, `03_build`, `04_assets`).
- Full research sweep across ~25 primary sources. Compiled:
  - `01_research/RESEARCH_BRIEF.md` — hackathon mechanics, lineage, every past winner, MoMo scale & strategy, competitive landscape, SA market reality, 12-gap analysis, 6 wild concepts + 1 "skyrocket".
  - `01_research/MOMO_API_AND_MINIAPP.md` — nine API families, auth mechanics, endpoints, async model, mini app = PWA, pre-event checklist.
  - `INFO_LOG.md` — every source and figure.

### Key findings that changed the strategy
1. **MTN signed with Ant International (Alipay group) in June 2026** to build the MoMo super app + mini app platform, launching Nigeria Q3 2026. This hackathon is **supply-side recruitment for a platform launching now.** Build like a launch partner, not a science project.
2. **70%+ of African mobile money accounts are dormant.** MTN SA has *deliberately stopped* chasing registrations and is chasing "stickiness." The winning idea creates a **weekly reason to open MoMo**.
3. **Every past winner was a lending or savings play — and 2026 has no lending track.** The judges have been deliberately redirected toward lifestyle, commerce and mobility.
4. **Mini apps are PWAs.** Web stack, buildable in 24h — which means the stack is not a differentiator. Idea + polish + pitch are.
5. **Three APIs are effectively unused by the market**: `Interact` (Channel as a Service — get into the MoMo USSD menu), `Get Consent` (PIN-signed mandate primitive), `Identify` (frictionless KYC). Differentiation lives there.
6. **M-PESA already has 221 mini apps.** MTN has a documentation page. MTN knows.
7. **Access-layer innovation wins this competition** — Rova Pay won Nigeria for removing the internet requirement; EchoKash placed for removing the screen.

### Decisions
- Docs live in this folder and are the single source of truth across chats.
- No code before the event (T&Cs require all work built during the hackathon). We prepare **knowledge, credentials, architecture and pitch** — not commits.

### Next session
1. Full ideation across all three tracks → `02_ideas/IDEAS_BOARD.md`
2. Score against the rubric in `RESEARCH_BRIEF.md` §F3
3. Converge on one primary + one backup
4. Draft the 250-character summary and the detailed description for the registration form
5. Register a MoMo developer account and pull the gated Mini App PWA spec
