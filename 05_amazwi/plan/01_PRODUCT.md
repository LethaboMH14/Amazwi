# AMAZWI — PRODUCT SPECIFICATION
### Game design · every screen · every flow · the gamification model

**Parent:** `00_MASTER_PLAN.md` · **Written:** 2026-08-30

---

## 1. THE CORE LOOP

Everything in AMAZWI is one loop with two seats. Learn this and the rest of the document is detail.

```
        ┌─────────────────────────────────────────────────────────┐
        │                                                         │
        │   ①  SPEAK          ②  LISTEN           ③  AGREE        │
        │                                                         │
        │   You get a word.   Two strangers        Did they get   │
        │   30 seconds to     hear your clip       it? Then it    │
        │   make people       and guess what       was good       │
        │   understand it     you meant — and      speech.        │
        │   in your language. referee the rule.                   │
        │   Without saying                          ↓             │
        │   the banned words.                                     │
        │                                    ④  EVERYONE SCORES   │
        │                                                         │
        │                          speaker earns · guessers earn  │
        │                          league moves · archive grows   │
        └─────────────────────────────────────────────────────────┘
```

### Why this exact mechanic and not another

| Property | How the mechanic delivers it |
|---|---|
| **It is genuinely fun** | It is *30 Seconds* — invented in South Africa in 1998, in a very large number of South African homes. The fun is not a claim; it is a forty-year-old, market-tested result. |
| **It elicits the right speech** | Spontaneous, unscripted, explanatory, fast. This is the category that does not exist in any corpus, because read-aloud is easy to collect and conversation is not. |
| **Validation is free** | A correct guess *proves* the utterance was intelligible, on-topic and in the right language. No moderator decided that. |
| **Fraud is expensive, not impossible** | There is no "approve" button to game, and farming requires colluding with strangers you cannot choose. It is **not** unbreakable — see §1.1, which closes the one hole that matters. |
| **Labels fall out as exhaust** | You get the semantic target (the card word), a distribution of what listeners heard, and a difficulty signal — for free. |
| **It has two seats** | Speakers earn money. Learners gain comprehension. Same loop, opposite motives. |

### 1.1 🔴 THE HOLE, AND THE FIX — read this before building anything

**The game's only rule is unenforceable, and enforcing it would require the exact capability AMAZWI exists to create.**

Nothing checks whether the speaker said the banned word. It *cannot* — there is no working ASR for these languages (`02_TECH.md` §5.1), so there is no keyword spotter. So the dominant speaker strategy is: **say the word, immediately and repeatedly.** All listeners guess correctly. The speaker is paid. The clip enters the corpus marked "validated."

And the second-order damage is worse than the fraud. That strategy produces **degenerate speech — the target word repeated** — the exact opposite of the spontaneous, explanatory speech the entire data thesis rests on. The corpus fills with the worst possible content while every quality metric reads green. Listeners will not report it unprompted: a speaker who says the word hands them a free correct answer.

**The judge question this creates, and it takes eight seconds to ask:**
> *"You've just told us no system on earth transcribes isiZulu. So how does your app know the speaker didn't just say the word?"*

#### The fix — the listener is the referee
One extra tap on the reveal screen, after the answer is shown:

> **"Did they say the word, or any banned word?"**  `[ No ]`  `[ Yes ]`

- **Both listeners say yes → round `VOIDED`.** No speaker reward. `γ_speaker` penalised.
- **Listeners are paid either way**, because they are paid for judging, not for outcomes (§5.1 rule 6) — so reporting costs them nothing.
- **Gold cards make it enforceable.** One assignment in eight is a seeded clip that *does* say the banned word. A listener who fails to flag it is failing an attention check, and their reward stops until they pass one. Without this the report button is decorative.

One boolean on `guess`, one branch in the resolver, one line of UI, plus the honeypot. **~40 minutes at G4.**

#### And it is a better answer than a defence
> *"We can't transcribe it — so we don't. The room referees. Two listeners agreeing that you cheated voids the round. That's the same agreement primitive that validates the clip, pointed at the rule instead."*

Put the limit on the honest-scope slide too: *"banned-word enforcement is peer-reported, not machine-verified — until we have the data to build the verifier, which is the entire point of the product."*

---

> ⚖️ **Legal note, non-negotiable.** *30 Seconds* is a registered trade mark of a South African company (Calco Games). **Game mechanics are not protectable; names, card content and trade dress are.** Never brand any part of AMAZWI "30 Seconds", never copy card content, never imitate the box. Reference it only in the pitch as a cultural touchstone — *"every South African has played a game like this"* — and write all card content yourself. See `07_TRUTH.md`.

---

## 2. GAME MODES

Six designed. **Two built for the competition.** The rest are the roadmap slide.

### 🟢 MODE 1 — UMLOZI · *"the whistle"* — **BUILD THIS**
**Say it, don't say it.**

- Speaker receives a card: one target word + four banned words.
- 30-second timer. Describe it in your language so someone else gets it.
- **Two** listeners, randomly assigned, hear it, answer, and referee the banned-word rule (§1.1).
- **Speaker earns** when listeners understand them, capped by the daily quest (§5.3).
- **Listeners earn a fixed amount for a valid judgement, whether or not they got it right** (§5.1 rule 6).

> **Why two, not three.** Two independent agreements is the ESP Game's own standard, it makes the unit economics literally true (`03_BUSINESS.md` §2), it balances guess supply exactly, it halves time-to-resolution, and it shrinks the cold-start problem by a third. Three costs 21% more per validated hour and buys very little.

> **Why listeners are paid for judging, not for being right.** If you pay listeners for matching each other, the optimal strategy for someone who understood nothing is to type the *most likely* answer — and since the reveal screen shows the answer every round, a pool of ~60 cards is fully learnable in an evening. Output agreement only defends when the guess space is large and unshared. Paying for the judgement removes the thing to converge on. **Attention is enforced by gold cards instead** — unannounced items with known answers; fail two in a row and your reward stops until you pass one.

**Data output:** spontaneous descriptive speech, semantically anchored, with a per-clip comprehension score.
**Why it is first:** it is the entire thesis in one screen.

---

### 🟢 MODE 2 — INGANEKWANE · *"the folktale"* — **BUILD THIS**
**The story chain.**

- A story opens with a seed line. Each player adds **15–20 seconds** and passes it on.
- The finished chain is published to the Archive with every contributor credited.
- Listeners vote for the best turn; the winning turn earns a bonus.

**Data output:** connected narrative speech — the hardest and most valuable kind — plus a shareable cultural artefact.
**Why it is second:** it shares ~90% of Umlozi's code (record → upload → play → score), it delivers the emotional payload, and it is the on-stage "As One" moment. Cheap to build, disproportionate return.

---

### ⚪ MODE 3 — NDIYEVA · *"I hear you"* — roadmap
**The transcription race.** Hear a clip, type what you heard. Two independent players agreeing produces a verified transcript — the single most expensive artefact in speech ML, generated as a competitive typing game.

### ⚪ MODE 4 — IZAGA · *"proverbs"* — roadmap
**Proverb duel.** Say the proverb, explain the meaning; others complete it or pick the meaning. Idiomatic speech plus a living proverb archive. The culture-preservation engine.

### ⚪ MODE 5 — XOXA · *"chat"* — roadmap
**Code-switch mode.** *"Tell a friend about your day."* *"Explain data bundles to your gogo."* Deliberately elicits mixed-language speech — the category that costs monolingual ASR the most and that essentially no corpus contains.

### ⚪ MODE 6 — IMBEWU · *"the seed"* — roadmap, and the moral peak
**The elder archive.** A quest to sit with an elder and record them telling a story, with their own consent, at a higher reward.

The scarcest speech in existence is old, rural, unmixed and idiomatic. It is also the speech that disappears. South Africa has exactly one fluent N|uu speaker left — Ouma Katrina Esau, 92, honoured by the state as a living human treasure, and by press accounts still struggling financially. **That single fact is the entire argument for paying people for their language, and it is true.**

> ⚠️ **Handle with care.** Do not name her, use her image, or imply endorsement without written permission. Cite the situation, not the person. It is context, not a prop. A South African judge will notice the difference instantly.

---

## 3. THE SCORING MODEL — where the real technical depth is

This is the part that separates AMAZWI from a quiz app, and it is worth building because it is both correct and demonstrable.

### 3.1 The problem
When a listener fails to guess, **who failed?** The speaker (unclear), the listener (low proficiency), or the word (too hard)? A naive system blames the speaker and pays them nothing. That is unjust and it corrupts the data.

### 3.2 The model
Treat every guess as an item response. A standard latent-trait formulation:

```
P(correct) = σ( θ_listener  −  β_word  +  γ_speaker )

    θ_listener  listener's proficiency in that language
    β_word      intrinsic difficulty of the card
    γ_speaker   speaker's clarity / expressiveness
    σ(x)        logistic function, 1 / (1 + e^−x)
```

Fit by alternating updates (or online gradient steps) as responses arrive. Three parameters, one equation, and every one of them is a product feature:

| Parameter | What it becomes |
|---|---|
| **γ_speaker** — clarity | The data-quality score. Drives reward multipliers and corpus curation. |
| **θ_listener** — proficiency | **A language proficiency score.** Crowd-calibrated, continuously updated, and — see `03_BUSINESS.md` — a sellable credential. |
| **β_word** — difficulty | Card calibration and adaptive difficulty. New cards start uncalibrated and get seeded against known-ability listeners. |

### 3.3 Why this is a genuinely strong move
- It is the **fair** answer to "who failed", so payment is defensible.
- It converts the learner side from a cost into an **asset**: every learner guess calibrates the corpus.
- **It produces a language proficiency certificate as a by-product.** South Africa's contact-centre sector hires on exactly this and has no objective instrument for African languages.
- It is real, citable psychometrics (Rasch / 2-PL item response theory), not invented mathematics.

### 3.4 Honest limits — say these before a judge does
- Cold start: with no data, all parameters are at their priors. Seed with gold-standard items of known difficulty.
- Identifiability: θ and γ trade off unless anchored. Anchor on gold items and on high-volume listeners.
- **Do not claim the proficiency score is validated** until it has been correlated against an external instrument. In the demo it is *"a proficiency estimate,"* never *"a certified level."*

---

## 4. THE TWO SEATS — one codebase, two roles

The learner side is **not a second product.** It is the same screens with three switches flipped.

| | **SPEAKER** | **LEARNER** |
|---|---|---|
| Primary action | Record a clue | Guess the clue |
| Answer input | — | 4-way multiple choice (default, and the demo path) or free text (advanced) |
| Reward | **Rand**, into MoMo | **XP + proficiency progress** (and optionally a small Rand credit) |
| Motivation | Income, pride, competition | Comprehension, progress, curiosity |
| Money direction | Earns | Pays / subscribes / is sponsored |
| Onboarding question | *"Which languages do you speak?"* | *"Which language do you want to understand?"* |

> 🔴 **Multiple choice must never validate the corpus.** Two beginners guessing at random on a 4-way question agree by chance **6.25%** of the time — on a clip containing no intelligible speech whatsoever. Resolve on a single MCQ listener and it is **25%**. So: **free-text agreement validates a recording; MCQ agreement earns XP only.** One flag on the guess row, and without it the claim that "gibberish earns nothing" is quantitatively false.

**Everyone can be both.** An isiXhosa speaker learning Sesotho earns on one side and learns on the other. That is the norm in South Africa, not the exception — most South Africans are multilingual — and it means the two populations are not two markets to acquire. They are one.

> **This is the answer to "isn't this a digital sweatshop?"** It is not a work app that some people also enjoy. It is a language game that some people also earn from. The learner who pays a subscription and the speaker who earns R4 are in the same match.

---

## 5. THE ECONOMY — points, money, and the wall between them

**Rule zero: Voice Points and Rands are different substances and never convert.**

Points are playful, inflatable, and reset each season. Money is an append-only ledger in integer cents, governed, audited, and never adjusted downward. Mixing them is how reward apps become fraud cases.

### 5.1 The reward formula

```
reward_cents =
      base_task_value
    × coverage_need_multiplier      (capped, e.g. 1.0 – 2.5)
    × difficulty_multiplier         (capped, e.g. 1.0 – 1.5)
    + quality_bonus                 (from γ_speaker, capped)
```

**Rules that must hold in code, not in policy:**
1. The reward is **published before** the task begins.
2. Integer **minor units** only. No floats touch money.
3. All multipliers **capped**; the product of caps is the maximum possible payout and it is asserted in a test.
3b. 🔴 **The coverage multiplier is capped by listener pool size, not by coverage alone — multiplier ≤ 1.0 until a language has ≥ 50 active listeners.** Without this you pay the biggest bonus exactly where collusion is cheapest: a confederate lands among the assigned listeners ~0.3% of the time in a pool of 1,000, and **~43% of the time in a pool of 8.** `02_TECH.md` §3.5.
4. An accepted published reward is **never reduced**.
5. **Exactly one** reward per contribution and per review — enforced by a unique constraint, not by application logic.
6. Listeners are paid a smaller fixed amount for a *valid* judgement, whether or not the speaker was understood.
7. If provider minimums or fees make cent-scale transfers uneconomic, earnings **accumulate in the ledger** and disburse at a transparent threshold.

### 5.2 Coverage-based rewards, not scarcity-based

The earlier draft of this project priced by **language rarity** — Tshivenda and isiNdebele speakers earn most because their languages are small.

**Change this.** Paying someone more because of the ethnicity they were born into is a headline waiting to happen, and it is also economically wrong: what is scarce is not the *language*, it is the *data you do not yet have*.

Price the **gap**, not the group:

> *"This conversational Tshivenda quest carries a coverage bonus because this speaking style is underrepresented in the current campaign."*

Same money reaches roughly the same people. Completely different sentence on the front page of a newspaper. It also self-corrects: once coverage fills, the bonus moves on.

### 5.3 The daily cap — a product rule that came out of the arithmetic

**Modelling the economics surfaced a flaw the original design did not have an answer for.**

A 15-second clip plus reading the card and thinking takes roughly 45 seconds. So an uncapped reward implies:

| Reward | Effective hourly rate | vs minimum wage (R30.23/hr) |
|---|---|---|
| R2.00/clip | R160/hr | **5.3×** |
| R3.00/clip | R240/hr | **7.9×** |

> **Uncapped, this is not a game. It is a farm — and an unaffordable one.** At eight times minimum wage, every sophisticated actor in the country optimises against you inside a week.

**The rule:**
> ### Cash is capped by the daily quest. Past the quest, you play for points, league and the Archive.

**Three plays a day at R2 = R6/day, R216/month including listening rewards — 58% of the SRD grant.** Meaningful money in South Africa. Not a wage. Not farmable.

> ⚠️ **The listening side needs its own cap, and the original design did not have one.** A listen-and-guess takes 20–30 seconds; at R0.50 that is **R60–R90/hour, 2–3× minimum wage** — the same farm, through the other door. **Cap paid judgements at 10 per day.** The loop needs 6/day to balance (3 clips × 2 listeners), so 10 leaves headroom and bounds listening at R5/day.
>
> **Total cash ceiling per user: R11/day.** One counter, one line, and it is the number that makes the whole business modelable.

**Three days of playing buys a loaf of bread** (R6/day; bread ≈ R19.61). ⚠️ *Do not say "three clips buys a loaf" — that is wrong by a factor of 3.3 and the correction is in your own research file.*

This one rule does five jobs:
1. **Bounds cost per user** at ~R216/month — the reason the business is modelable at all.
2. **Bounds fraud upside.** A stolen account is worth R6/day. Not worth industrialising.
3. **Keeps it a game** — the Track 2 argument and the retention argument.
4. **Enforces §6's anti-crowding-out principle structurally.** Past the cap the only reason to keep playing is that you want to — which runs the "is this fun without money?" test continuously, on every user, forever.
5. **Creates honest scarcity**, which is what makes a daily quest worth showing up for.

Full derivation and sensitivity in `03_BUSINESS.md` §2–3.

---

## 6. HOW TO PAY WITHOUT DESTROYING THE THING YOU ARE PAYING FOR

There is a well-established result in economics and psychology — **motivation crowding-out** — that paying people for an activity can *reduce* effort and quality relative to paying nothing, particularly when the payment is small enough to reframe a social act as a cheap transaction. Gneezy and Rustichini's framing is the canonical one: *pay enough, or don't pay at all.*

This is the single largest design risk in AMAZWI, and the current plan walks straight into it: cents per task is precisely the "small payment" regime where quality collapses.

**The structural defences, built into the product:**

1. **The game must be playable, and fun, with the money switch off.** Test this. If nobody plays without payment, the payment is doing all the work and quality will follow the money down.
2. **Pay for outcomes, not activity.** Money attaches to *validated* contributions, never to submissions. Effort without comprehension earns nothing.
3. **Keep the two currencies separated and make points the loud one.** The league, the streak, and the archive are what the interface celebrates. The wallet is honest, correct and quiet.
4. **Never adjust a published rate downward.** Retroactive rate cuts are the fastest way to destroy a contributor community, and it happens in this industry constantly.
5. **Make the learner side genuinely free.** A population that plays for zero money is the proof that the game has intrinsic pull — and it is your control group.
6. **Credit, not just cash.** Named attribution in the Archive is a non-monetary reward that does not crowd out — it is the Wikipedia engine.

> Evidence and citations: `research/F_GAMIFICATION.md`.

### 6.1 The Ayoba lesson — put this on a slide

MTN's previous engagement product, **Ayoba**, reached roughly 35 million monthly active users and was removed from app stores on **20 March 2026**. Press analysis of the failure is consistent: a large share of users were drawn by **free-data incentives rather than utility**, so retention collapsed against WhatsApp.

**That is the exact failure mode of a "get paid to record" app.** Naming it yourself, on stage, is a power move:

> *"MTN has already learned this lesson expensively. Ayoba proved that incentive-driven signups don't retain. So AMAZWI's retention is not the payment. It's the game — and we designed it so you can switch the money off and people keep playing."*

---

## 7. THE GAMIFICATION SET

Ranked by evidence strength. Detail and citations in `research/F_GAMIFICATION.md`.

| # | Mechanic | Design decision |
|---|---|---|
| 1 | **Daily streak** | With **one automatic streak-freeze per week.** The dominant failure of streaks is that a single missed day causes permanent churn — the freeze converts a quit into a return. |
| 2 | **Place leagues** | Weekly, promotion/relegation, by **ward or township**, not just individual. Team competition sustains engagement better than individual leaderboards and it is far more South African. *Khayelitsha vs Soweto. Thohoyandou vs Giyani.* |
| 3 | **Language leagues** | Parallel table by language, so a small language community can be #1 nationally. Fixes the "big languages always win" problem structurally. |
| 4 | **Daily quest — three plays** | Small, closable, completable in under three minutes on a bad connection. |
| 5 | **Coverage call-outs** | *"Sesotho conversational needs 40 more voices this week."* Turns a data need into a rallying cry. This is the "Maximum Velocity" mechanic. |
| 6 | **The Archive** | Permanent, named, credited. The long-term retention engine and the ethical answer in one feature. |
| 7 | **Seasons** | Tied to the South African cultural calendar — **September is Heritage Month, Heritage Day is 24 September.** The hackathon is 2–3 September. Season One should be *Heritage Season*, launching the month it is actually pitched in. |

**Deliberately excluded:** hearts/lives (punishes the poor connection, not the player), loot boxes and any randomised-prize mechanic (gambling-adjacent and a regulatory question in South Africa — see `07_TRUTH.md`), infinite scroll, and streak-loss push notifications that induce anxiety.

---

## 8. SCREEN-BY-SCREEN SPECIFICATION

Mobile-first, single column, inside the MoMo Mini App shell.

✅ **Confirmed from MTN's own Mini App documentation:** the user **arrives already authenticated.** A `START_JOURNEY` event hands your page the logged-in `msisdn` and a session token on load. **Do not build a login screen** — that is the entire point of a mini app, and building one signals you did not read the spec.

⚠️ **Also confirmed, and it constrains this design directly:** the session dies after **60 seconds without a heartbeat**. Every screen below where a user is thinking, reading or recording — which is most of them — depends on that heartbeat running. See `02_TECH.md` §1A.

Assume a constrained viewport, an undocumented CSP, and expensive data.

### 8.1 Onboarding — five screens, under sixty seconds

**① WELCOME**
- Logo, tagline *"Every voice counts. Yours pays."*
- One line: *"Describe the word in your language. If people get it, you get paid."*
- A 6-second silent looping demo of the game
- `[ Start ]`

**② AGE GATE**
- *"You must be 18 or older to play."* → date of birth or explicit confirmation
- Adults-only is a **hard requirement**: voice is personal information, and children's data carries additional restrictions under POPIA. Do not accept minors in the MVP.

**③ IDENTITY**
- *"Continue with MoMo"* — one tap, no forms
- Show what is and is not shared. Never store an identity document.

**④ LANGUAGES** — the screen that sets the seat
- *"Which languages do you speak?"* (multi-select, ordered by home-language share)
- *"Which would you like to understand better?"* (multi-select — **this is the learner switch**)
- Province / community — **coarse only**. Never request precise location.

**⑤ CONSENT** — separate, plain-language toggles, each independently declinable
- Recording and storage
- Other players hearing your recording
- Use for speech-technology research and model training
- Reward terms
- Retention and withdrawal, explained in one sentence
- Store **consent version, purpose, status, timestamp**. Written in the player's own language.

---

### 8.2 The main surfaces

**HOME / TODAY**
Streak · today's quest (3 plays) · published reward · Voice Points · league position (place + language) · wallet strip · `[ PLAY ]` as the single dominant action. Below the fold: the coverage call-out, and the Archive teaser.

**GAME SELECT**
Two live modes with a one-line explanation each. Locked modes visible but greyed with *"coming soon"* — this is where the roadmap becomes visible to a judge inside the product itself.

**UMLOZI · SPEAKER**
1. **Card reveal** — target word large; four banned words listed beneath in red; language chip; published reward; `[ I'm ready ]`
2. **Countdown** — 3 · 2 · 1
3. **Recording** — 30-second ring timer, live waveform, live *too quiet* / *clipping* indicators, `[ Stop ]`
4. **Review** — replay, re-record (limited), `[ Send it ]`. **Upload is blocked until the client-side quality checks pass** — never spend a player's data on a clip that will be rejected.
5. **Sent** — *"Three people are listening now."* Return to home; result arrives later.

**UMLOZI · LISTENER**
1. Clip plays (replay limited to 2)
2. Answer: 4-way multiple choice (default) or free text (advanced)
3. Reveal: the word, whether you got it, what others guessed, XP/reward
4. **The referee tap:** *"Did they say the word, or any banned word?"* `[ No ] [ Yes ]` — §1.1
5. `[ Next ]` — chained, so the listener side is a fast, satisfying run

> 🔴 **Card illustrations appear on the speaker's card ONLY — never in the listener flow, never on the reveal.** If an illustration ever renders on a listener's screen the game is over. And even on the speaker's side it shifts the task from *describe the word* to *describe the picture*, which weakens exactly the linguistic output you are collecting. Consider shipping the demo with text-only cards.

**RESULT (speaker, asynchronous)**
*"2 of 3 people understood you."* Clarity score movement · reward moved to available · points · league movement · `[ See receipt ]`

**WALLET**
Pending → Available → Paid, as three visually distinct states. Transaction history with provider references. Threshold explanation when applicable. **This screen must never lie.** "Request accepted" is not "paid" and must not be displayed as paid.

**VOICE VALUE RECEIPT** — the signature screen
```
Contribution ID · language · mode
Clarity score · how many understood you
Coverage contribution — what gap this filled
Reward, in cents, and its published basis
Voice Points
Consent version and status
MoMo payout status and reference
Archive entry number
```
This one screen simultaneously proves entertainment, payment traceability, data value and consent. It is the last thing shown in the demo.

**THE ARCHIVE**
The emotional core. Browse by language, place, mode. Listen to finished story chains with every contributor credited. Your own contributions, numbered and permanent. *"You are voice #4,182 in the South African Voice Archive."*

**LEAGUES**
Two tabs — Place and Language. Promotion/relegation zones shaded. Your position pinned. Season countdown.

**PROFILE & PRIVACY**
Languages · proficiency estimates · clarity score · active consent version · **revoke future use** with a plain-language explanation of exactly what that does and does not undo · download my contributions.

**IMPACT CONSOLE** *(MTN-facing, second device)*
Campaign budget committed and spent · validated minutes by language and mode · coverage heat map · acceptance rate · active-consent corpus count · payout success rate · cost per validated minute · **next recommended language for budget**. No invented model-improvement numbers.

---

### 8.3 The states everyone forgets — and judges notice
Microphone permission denied · no network mid-record · upload interrupted and resumed · empty league · no clips left to judge · consent revoked · payout failed and returned to available · sandbox unavailable · account rate-limited. Each needs a written, human sentence — not a toast saying "Error".

---

## 9. USE CASES — who actually opens this

| Persona | Seat | Why they open it | What they get |
|---|---|---|---|
| **Thabo, 23, Soweto, unemployed** | Speaker | Three minutes, R6, and he is holding up his ward's ranking | Income, standing |
| **Aisha, 29, Sandton, marketing** | Learner | She has isiZulu-speaking colleagues and cannot follow a meeting | Comprehension that actually transfers |
| **Nomsa, 45, Thohoyandou** | Speaker | Tshivenda has a coverage bonus and her town is climbing | Income, pride, visibility |
| **Pieter, 19, Kaapse Vlakte** | Both | Speaks Kaaps; earns for it; learning isiXhosa | Both sides of the loop |
| **A call-centre trainee, Durban** | Learner | Employer requires conversational isiZulu | A proficiency estimate that means something |
| **Sipho, 31, Alexandra** | Speaker | Records his grandmother's stories in the Archive | Legacy, and the highest reward tier |
| **MTN campaign manager** | Console | Needs 200 hours of banking-domain Sesotho | Targeted acquisition with cost-per-minute visibility |

---

## 10. THE COMPETITION BUILD — the non-negotiable list

Nothing enters this list unless it improves a judging score, keeps the demo alive, or reduces a serious risk.

1. Mini App shell, mobile viewport, MoMo design conventions
2. Adult age gate
3. MoMo/sandbox identity link
4. Versioned, granular consent — **enforced server-side, not merely displayed**
5. Language selection, both seats
6. **Umlozi speaker flow** — card, timer, record, client quality gate, upload
7. **Umlozi listener flow** — playback, answer, reveal
8. Agreement scoring and the clarity/proficiency update
9. Append-only reward ledger in integer cents, idempotent
10. MoMo sandbox disbursement, or a clearly-labelled provider state
11. League update (place + language)
12. **Voice Value Receipt**
13. Impact Console
14. Consent revocation with future-use exclusion
15. Deterministic seed/reset
16. Written, human error states

> **Inganekwane (the story chain) is deliberately NOT on this list.** `05_BUILD.md` §6 cuts it at G6 if the clock demands, and a non-negotiable list with negotiable items on it is not a list. It is the first thing to build once the loop is stable, and the first thing to cut.

**Add only once that loop is stable:** on-device Whisper transcription assist · duplicate-audio fingerprint · coverage-driven card ordering · streak celebration · SMS notification · offline upload queue.

---

## 11. THE FOUR THINGS THAT MAKE THIS UNMISTAKABLY SOUTH AFRICAN

1. **The mechanic is South African.** A describe-it-against-the-clock game invented here in 1998. Not a Silicon Valley loop with local content poured in.
2. **Code-switching is a first-class citizen, not an error.** Every other system treats *"ngicela i-data"* as a failure to be corrected. AMAZWI treats it as the target. Tsotsitaal, Sepitori, Kaaps — these are the speech that global datasets have no category for, and they are how the country actually talks.
3. **Place is the team.** Not countries, not abstract tiers — your ward. South African identity is intensely local and there is no consumer product that reflects it.
4. **The Archive is a public good, not a private dataset.** What gets built is visible, credited and belongs to the people in it. That is the difference between preservation and extraction.

---

## 12. INCLUSION — the design decisions, not the sentiment

- **All twelve official languages** are architecturally supported from day one, including **South African Sign Language**. Ship only the ones you can quality-assure; show the rest as coming, never as done.
- **Afrikaans is in, and it is not a footnote.** Most Afrikaans home-language speakers are Coloured South Africans, and **Kaaps** is a distinct, historically marginalised variety with an active recognition movement. Including Afrikaans *and* naming Kaaps specifically is both linguistically correct and a statement about who this is for. See `research/E_SA_CULTURE.md`.
- **Sign language is not a "later" checkbox.** SASL became an official language in 2023. Video-based quests are the natural extension. Say it is on the roadmap, and mean it.
- **Migrant and heritage languages** — Shona, Chichewa, Portuguese, French, Somali — belong in a community tier. South Africa's linguistic reality is larger than its official list, and being the product that notices is worth more than being the product that is careful.
- **Endangered languages get a protected tier**, not a market rate. N|uu, Nama, ǂKhomani. Their value is not commercial and the pricing must not pretend it is.
- **Low-literacy paths.** Icons, audio instructions in-language, and multiple-choice answering everywhere free text appears. Roughly one in ten South African adults has limited literacy; a text-only game excludes exactly the speakers whose voices are most valuable.
- **Data cost is an inclusion issue.** Aggressive payload minimisation, Opus encoding, client-side gating before upload, and a zero-rating ask to MTN. A product that costs R5 of data to earn R4 is not an income product.
