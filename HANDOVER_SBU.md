# HANDOVER → SBU

> **Sbu response incorporated 2026-08-31.** The role split was reversed and the product decisions were accepted/reconciled. Read [`HANDOVER_LETHABO.md`](HANDOVER_LETHABO.md) and [`05_amazwi/plan/00_MASTER_PLAN.md`](05_amazwi/plan/00_MASTER_PLAN.md) before acting on older instructions below. This file remains Lethabo's incoming context and historical reasoning; where it conflicts with the canonical plan, the canonical plan wins.

**From:** Lethabo · **Date:** Monday 31 August 2026
**Event:** Wednesday 2 Sept 09:30 → Thursday 3 Sept 12:00 · The Forum, Bryanston
**Repo:** https://github.com/LethaboMH14/Amazwi

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

## THE SIX DECISIONS THAT NEED BOTH OF US

Full detail in the README. In short:

1. **Role split — reversed and confirmed.** Sbu owns PLATFORM (backend, MoMo, ledger, trust, deployment, isiZulu). Lethabo owns EXPERIENCE (frontend, product, demo, Setswana).
2. ~~Which two languages~~ — **settled: isiZulu + Setswana.** The competition does not build or pitch two ASR models; the advantage is first-language content ownership.
3. **Keep the name AMAZWI?** It collides with the Amazwi South African Museum of Literature — a real national institution. My call: keep it and own it. Decide today or not at all.
4. **Build the sponsor payment screen?** It is the only thing that makes the central fintech claim true.
5. **Pre-build?** Depends on the organiser's answer. The rule is quoted verbatim in `05_BUILD.md` §1.1.
6. **The kill rules.** Agree them Tuesday, before anyone is emotionally invested.

---

## TODAY, IN ORDER

- [ ] **Card content — 30 isiZulu cards.** I do 30 Setswana in parallel. Target word, four banned words, `accepted_answers`, three distractors, plus a few gold honeypots. **Build the eight demo cards first and to a higher standard.** This is game design in your own language, not translation — budget 2–3 min per card. `05_BUILD.md` §2.0.1
- [ ] **Organiser email** — the pre-built-code rule, what the "exclusive" IP licence covers, and **what time pitches start Thursday** (three gates assume the morning is free). Draft in `05_BUILD.md` §1.2 and §1.6.
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
