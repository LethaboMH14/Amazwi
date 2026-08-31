# HANDOVER → SBU

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

1. **The validation IS the game.** Nobody reviews anything. A speaker describes a word against a 30-second timer without saying four banned words; two randomly-assigned strangers guess. **Agreement between independent strangers is the validation.**
2. **Learners are the second population.** They play the guessing side, earn nothing, and are there because guessing what a native speaker just described *is* how you learn a language. Money flows in a circle instead of down a hole.
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
| 🔴 **`F_GAMIFICATION` was never completed** | The only missing research file. Needed: **motivation crowding-out** (Deci & Ryan; Gneezy & Rustichini *"Pay Enough or Don't Pay At All"*) — the evidence that small payments can *destroy* quality, which is the single biggest risk in our design. Plus Duolingo's published retention results, gold-standard/honeypot literature, output-agreement games (ESP Game, peer prediction), and **whether a skill-based reward game triggers the SA Lotteries or National Gambling Act.** Write it to `05_amazwi/research/F_GAMIFICATION.md` in the same format as the others |
| **MoMo Mini App design standards + CSP** | Promised by MTN's programme page, not rendered anywhere public. Dig into the portal. Building against an unknown CSP is a real risk |
| **Whether SA sandbox disbursement actually exists** | `B_MOMO_API.md` §1a suggests "South Africa Disbursement" is a bulk-payroll product behind a commercial agreement, **not a self-serve API**. If so, our payout demo is the labelled demo provider and we should know that today |
| **The bulk B2C disbursement fee** | Not the 2% consumer rate. **This one number decides whether R2 rewards are economical at all.** Only MTN can answer it |
| **Native-speaker sign-off** | Every word of in-game copy, every card. Non-negotiable |

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
5. The Archive — the closing image

**Three critiques of our existing board you should know:**
- 🔴 **The tone is wrong.** It reads as a documentary about language loss. **This is a party game.** Nothing on that board is *fun* — no laughter, no rivalry, no speed, no near-misses. Reverence belongs in the Archive; the game needs to feel like a Friday night.
- 🔴 **The imagery is AI-generated and reads as such** — the face paint is a pan-African pastiche tied to no actual culture. Fine on a concept board. **Never in-product, and never on a slide as if it were documentary.** Photograph each other instead; it will be more convincing.
- **It shows 3 listeners; we moved to 2**, and it has the speaker rating their own round instead of the listener refereeing the banned-word rule. Six corrections in `09_MOCKUP_LIBRARY.md` §②.

**And the three gaps across all thirteen references:** none of them is funny, none is specifically South African *(Ndebele geometry, Kaaps, a taxi rank, a Joburg skyline — never generic "Africa")*, and none shows a failure state. **Those three gaps are where the design can actually win.**

---

## THE SIX DECISIONS THAT NEED BOTH OF US

Full detail in the README. In short:

1. **Role split** — the plan assigns me PLATFORM (backend, MoMo, trust), you EXPERIENCE (frontend, product, demo). Confirm and never revisit.
2. **Which two languages.** Two, not five.
3. **Keep the name AMAZWI?** It collides with the Amazwi South African Museum of Literature — a real national institution. My call: keep it and own it. Decide today or not at all.
4. **Build the sponsor payment screen?** It is the only thing that makes the central fintech claim true.
5. **Pre-build?** Depends on the organiser's answer. The rule is quoted verbatim in `05_BUILD.md` §1.1.
6. **The kill rules.** Agree them Tuesday, before anyone is emotionally invested.

---

## TODAY, IN ORDER

- [ ] 🔴 **Phone the two native speakers.** Committed two-hour window from each, in writing. **This is the longest-lead dependency in the whole plan and it has no name on it.** No fallback if it fails.
- [ ] **Organiser email** — the pre-built-code rule, what the "exclusive" IP licence covers, and **what time pitches start Thursday** (three gates assume the morning is free). Draft in `05_BUILD.md` §1.2 and §1.6.
- [ ] **MoMo: 90-minute hard timebox.** Two sandbox API users, one held in reserve. If SA disbursement is unreachable at 09:00, the labelled demo provider becomes the plan of record **today**, not at 00:30 Thursday.
- [ ] **Sandbox call budget on the wall — 30 calls.** The quota is undocumented and its cooldown is ~2 days, which outlasts the event. **No automated test ever touches it.**
- [ ] **Write the `is_correct` function on paper** before the card job starts. `02_TECH.md` §3.4.
- [ ] Card content. Design tokens. Sound assets.

---

## THE FIVE FACTS THAT CARRY THE PITCH

1. **There is no working speech recognition for ten of our eleven spoken official languages.** Whisper scores 146% WER on Southern Bantu, 223% on Setswana. Above 100% means it invents more than it gets right.
2. **Google's WAXAL dataset contains zero South African languages.** They funded East and West Africa and skipped us.
3. **One hour of in-domain data takes isiZulu from ~146% to ~25% WER.** When the baseline is broken, the first hour is worth more than the next thousand.
4. **MoMo SA has ~13m registered users and does not report active ones.** In the 2020 relaunch, ~8% of registered were active. Activation is MTN SA's live problem; we are a daily-open product.
5. **Ayoba had 35m MAU and died in March 2026** because free-data signups don't retain. That is the exact failure mode of a "get paid to record" app — which is why the game has to work with the money switched off.

---

## THE ONE THING I WOULD NOT COMPROMISE ON

**The honesty.** The strongest paragraph in the whole pitch is the one where we say what we did *not* do:

> *"We have not improved anyone's word error rate today. You can't do that in twenty-six hours, and anyone who tells you otherwise is showing you a slide, not a training run."*

Every judge in that room has been oversold to eleven times before we walk on. **Precision is the differentiator.** If you find something in these documents that overclaims, cut it — even if it sounds good. Especially if it sounds good.
