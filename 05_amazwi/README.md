# AMAZWI — Team Sonar · Track 2 · MoMo Mini App Hackathon 2026

**Event:** Wed 2 Sept 09:30 → Thu 3 Sept 12:00 (26.5 hours) · The Forum, Bryanston
**Prep remaining:** Monday 31 Aug + Tuesday 1 Sept
**Team:** Lethabo + Sbu · **Track:** Entertainment & Lifestyle

---

## START HERE

Read in this order. `00_MASTER_PLAN.md` is the spine; everything else is subordinate detail.

| | File | What it is |
|---|---|---|
| **1** | [00_MASTER_PLAN.md](plan/00_MASTER_PLAN.md) | **The decision.** What changed and why, the product, the thesis for MTN, what we are not building |
| 2 | [01_PRODUCT.md](plan/01_PRODUCT.md) | Game design, the scoring model, every screen, gamification, the daily cap, inclusion |
| 3 | [02_TECH.md](plan/02_TECH.md) | Architecture, data model, AI engineering, the data pipeline, security by design |
| 4 | [03_BUSINESS.md](plan/03_BUSINESS.md) | Unit economics, pricing, the five buyers, how MTN makes money |
| 5 | [04_DESIGN.md](plan/04_DESIGN.md) | Visual system, motion, sound, 3D, the mockup pipeline |
| 6 | [05_BUILD.md](plan/05_BUILD.md) | **Most urgent.** The two prep days, the 26.5-hour gate schedule, packing list |
| 7 | [06_PITCH.md](plan/06_PITCH.md) | Stage choreography, script, slides, judge Q&A, failure plan |
| 8 | [07_TRUTH.md](plan/07_TRUTH.md) | **Read before pitching.** Claims register, competitor handling, legal, ethics |
| 9 | [08_REDTEAM.md](plan/08_REDTEAM.md) | Adversarial review — what breaks and how |
| 10 | [09_MOCKUP_LIBRARY.md](plan/09_MOCKUP_LIBRARY.md) | Twelve visual directions mapped screen-by-screen, **plus six corrections the existing AMAZWI concept board needs** |

**Evidence** lives in [`research/`](research/) — A_MTN_CORPORATE · **B_MOMO_API** · C_COMPETITIVE · D_SPEECH_AI · E_SA_CULTURE · G_BUSINESS.
*(F_GAMIFICATION was not completed — see "Gaps" below.)*
[`B_MOMO_API.md`](research/B_MOMO_API.md) contains **the hackathon T&Cs quoted verbatim** — judging criteria, the pre-existing-code rule, the IP clause and team size. Read §7 of it before Wednesday.

---

## 📋 FOR SBU — WHAT TO CHECK, AND THE SIX DECISIONS THAT NEED BOTH OF US

**Status: the planning is complete and internally consistent. Nothing has been built.** Read the master plan, then the two documents for your lane, then bring answers to these six.

### Decisions we cannot start without

| # | Decision | Default if we don't decide | Where |
|---|---|---|---|
| **1** | **Who is PLATFORM and who is EXPERIENCE?** The source plan assigns Lethabo → backend/MoMo/trust, Sbu → frontend/product/demo. **Confirm it and never revisit it.** | As written | [05_BUILD.md §3](plan/05_BUILD.md) |
| **2** | **Which two languages?** Two, not five. Only ones we can genuinely quality-assure. | — | [05_BUILD.md §2](plan/05_BUILD.md) |
| **3** | **Do we keep the name AMAZWI?** It collides with a national museum. My call: keep it and own it — but decide today or not at all | Keep + own it | [07_TRUTH.md §1](plan/07_TRUTH.md) |
| **4** | **Do we build the sponsor payment screen?** It's the only thing that makes "money crosses MoMo twice" true — four of our defences rest on it | Build it; cut the story chain | [06_PITCH.md §7a](plan/06_PITCH.md) |
| **5** | **Do we pre-build?** Depends on the organiser's answer to the email | Generic public starter only | [05_BUILD.md §1](plan/05_BUILD.md) |
| **6** | **The kill rules** — agree them Tuesday, before anyone is emotionally invested | As written | [05_BUILD.md §6](plan/05_BUILD.md) |

### Where I'd most like your disagreement
- **The whole reframe** — turning validation into a guessing game, and adding learners as a second population. It's a big change from what we submitted. [00_MASTER_PLAN.md §1](plan/00_MASTER_PLAN.md)
- **The 26-hour gate schedule.** It's aggressive. If you think a gate is wrong, say so now, not Wednesday. [05_BUILD.md §5](plan/05_BUILD.md)
- **The live room-play.** It's the highest-risk, highest-reward moment in the pitch. If you're not confident, we do the judge-only demo. [06_PITCH.md §3](plan/06_PITCH.md)
- **The mockup corrections.** Your concept board is good; six things on it now contradict the plan. [09_MOCKUP_LIBRARY.md §1](plan/09_MOCKUP_LIBRARY.md)

### What is NOT done
- **Nothing is built.** No code, no repo, no cards written.
- **`F_GAMIFICATION` research never completed** — mechanics are designed against known literature but citations aren't assembled. **No retention statistic goes on a slide.**
- **Two questions only the organisers can answer**, both in the Monday email: the pre-built-code rule, and what time pitches start Thursday.
- **One question only MTN can answer:** the actual bulk disbursement fee. It decides whether R2 rewards are economical at all.

---

## THE PRODUCT IN ONE SENTENCE

> **AMAZWI is 30 Seconds played in your own language, against the whole country — where speaking pays you, and listening teaches you.**

Describe the word without saying the four banned words. Strangers across South Africa guess. If they understand you, everyone scores and MoMo pays. Learners play the guessing side to learn. What comes out is the South African conversational speech data that does not exist.

---

## DO THESE TODAY (Monday 31 August)

- [ ] 🔴 **06:45 — PHONE THE TWO NATIVE SPEAKERS. BEFORE ANYTHING ELSE.** Get a committed two-hour window from each, in writing. This is the longest-lead dependency in the whole plan and it had no name attached to it. If you can only get one, ship one language. [05_BUILD.md §2.0](plan/05_BUILD.md)
- [ ] **Send the organiser email** about pre-built code — draft in [05_BUILD.md §1.2](plan/05_BUILD.md). Before 09:00. **Add the two questions in §1.6** — especially *what time do pitches start on Thursday*, because three gates assume the morning is free.
- [ ] **MoMo developer account** → subscription keys for Collections **and Disbursements** → provision sandbox API user → **complete one successful `transfer` end to end.**
- [ ] **Ask the MoMo community the one financial question that decides the model:** what is the actual **bulk B2C disbursement fee** in South Africa? (Not the 2% consumer rate.) This determines whether R2 micro-rewards are economical at all.
- [ ] **Decide the two demo languages.** Two. Not five.
- [ ] **Start the card content** — ~60 cards per language, every one checked by a first-language speaker. This is the bottleneck. [05_BUILD.md §2.1](plan/05_BUILD.md)
- [ ] **Decide the name question** — AMAZWI collides with a national museum. Keep it and own it, or switch. [07_TRUTH.md §1](plan/07_TRUTH.md). Decide today or not at all.
- [ ] **Read [02_TECH.md §1A](plan/02_TECH.md) — the MoMo WebView host contract.** The mini app session dies after **60 seconds without a heartbeat**, and our core interaction is a user who is busy but not tapping for over a minute. Without it the demo dies mid-recording, on stage. Fifteen lines of code. Build it at G0.
- [ ] Confirm the PLATFORM / EXPERIENCE role split and do not revisit it.
- [ ] Record the sound assets. Two people, a phone, a quiet room, forty minutes.

---

## THE FIVE FACTS THAT CARRY THE PITCH

1. **There is no working speech recognition for ten of South Africa's eleven spoken official languages.** Whisper scores 146% WER on Southern Bantu, 223% on Setswana. Above 100% means it invents more than it gets right.
2. **Google's WAXAL dataset contains zero South African languages.** They funded East and West Africa and skipped us.
3. **One hour of in-domain data takes isiZulu from ~146% to ~25% WER.** When the baseline is broken, the first hour is worth more than the next thousand.
4. **MoMo South Africa has ~13m registered users and does not report active ones.** In the 2020 relaunch, ~8% of registered were active. Activation is MTN SA's live problem, and this is a daily-open product.
5. **Ayoba had 35m MAU and died in March 2026** because free-data signups don't retain. That is the exact failure mode of a "get paid to record" app — which is why the game has to work with the money switched off.

---

## 🔴 THE RED TEAM FOUND A HOLE IN THE CORE MECHANIC — FIXED, BUT KNOW IT

**"You've just told us no system on earth transcribes isiZulu. So how does your app know the speaker didn't just say the word?"**

Nothing checked banned words — and it *can't*, because that needs the ASR the product exists to create. The dominant strategy was to say the word: it pays reliably, and listeners get a free correct guess so they'd never report it. Worse than the fraud, it fills the corpus with the target word repeated — the exact opposite of the spontaneous speech the whole thesis rests on, with every quality metric reading green.

**Fixed** by making the listener the referee (one tap on the reveal, both agreeing voids the round) plus gold honeypots that make reporting enforceable. [01_PRODUCT.md §1.1](plan/01_PRODUCT.md). Read it before you build, and have the answer ready before it's asked.

**Four other things the red team caught, all now corrected:**
- **Three listeners → two.** At three the margin at $100/hr fell to 12% and guess supply ran 33% short, so a third of clips would never resolve. Two balances the loop exactly. [03_BUSINESS.md §2.1](plan/03_BUSINESS.md)
- **The pitch claimed real money moved.** MTN's own sandbox docs say it doesn't process real money — said to MoMo engineers, that's the credibility kill. [06_PITCH.md §2](plan/06_PITCH.md)
- **`is_correct` had no definition** — the load-bearing function in the whole system. Now specified, and it needs `accepted_answers` captured in today's card job. [02_TECH.md §3.4](plan/02_TECH.md)
- **The sandbox has an undocumented quota with a ~2-day cooldown.** Automated tests must never touch it. [05_BUILD.md §2.2](plan/05_BUILD.md)

**All 23 findings are now folded into the plan.** The ones that changed the most:

| | What was wrong | Where it now lives |
|---|---|---|
| **R7** | **Cold start.** No `EXPIRED` state — a Tshivenda clip with no listeners stayed `OPEN` and its reward `PENDING` forever, on the screen that must never lie. And the coverage multiplier paid **up to 2.5×** into exactly the small pools where a confederate lands among the listeners **43%** of the time | [02_TECH.md §3.5](plan/02_TECH.md) — 48h expiry, pay half anyway, two-guess minimum, multiplier capped by pool size |
| **R9** | **The inbound leg doesn't exist.** "Money crosses MoMo twice" carries four separate defences, and the build had 17 items and no way to collect money from anyone | [06_PITCH.md §7a](plan/06_PITCH.md) — build the sponsor screen, or change the sentence |
| **R10** | **The room-play couldn't complete.** 5-screen onboarding in 100 seconds; a hotspot carries ~5 devices; and the room never actually heard a *recording* | [06_PITCH.md §3](plan/06_PITCH.md) — guest path, room listens to the clip, seeded, rehearsed deflation line |
| **R13/R14** | **The sleep plan and gate table were mutually exclusive.** G5 and G6 needed both people while one was asleep. G0 had ~30 real minutes for 3 hours of work | [05_BUILD.md §5](plan/05_BUILD.md) — gates re-cut single-lane overnight, G0 into the starter repo |
| **R15** | **The longest-lead dependency had no name on it** — two native speakers, for hours, Monday and Tuesday, unconfirmed | [05_BUILD.md §2.0](plan/05_BUILD.md) — phone them at 06:45, cut to 30 cards |
| **R12** | The close described an identifiable, elderly, non-consenting person's finances — against my own instruction three documents earlier | [06_PITCH.md](plan/06_PITCH.md) — corrected |
| **R16–R23** | Not-a-mini-app · WAXAL listed as both confirmed and unverified · the 70% figure is a vendor's claim · ECAPA's corpus is non-commercial even though its weights aren't · scale table had no demand side · 24 vs 26 hours · card art leaks the answer | folded across all files |

Full detail in [08_REDTEAM.md](plan/08_REDTEAM.md), including its own fix-ordering by day.

---

## THE THREE THINGS MOST LIKELY TO LOSE THIS

1. **"Isn't this just paid data labelling?"** — answered structurally, not rhetorically: nobody reviews anything, there is no approve button, and half the players earn nothing and are there to learn. [07_TRUTH.md §3](plan/07_TRUTH.md)
2. **African Next Voices / Swivuriso already does much of this** — Gates-funded, pays contributors, same seven languages. **Build on it and credit it.** Do not pretend it doesn't exist. [07_TRUTH.md §3.1](plan/07_TRUTH.md)
3. **"What did you build today?"** — one agreed answer, identical from both of you, delivered without defensiveness. [05_BUILD.md §1.5](plan/05_BUILD.md)

---

## GAPS — what is not covered and what to do about it

- **`F_GAMIFICATION.md` was not completed** (session limits). The mechanic set in [01_PRODUCT.md §7](plan/01_PRODUCT.md) is designed against the known literature (motivation crowding-out, streak failure modes, output-agreement games) but **the citations are not assembled. Do not put a specific retention statistic on a slide** — describe the mechanics, not measured lifts.
- **The T&Cs say "48 hours"; the invitation says 26.5.** Ask at check-in which governs — it changes the gate schedule. [05_BUILD.md §1.1](plan/05_BUILD.md)
- **The IP clause grants MTN an "exclusive" licence over "demos and products" for marketing purposes.** Probably harmless, genuinely unusual. Ask what it covers.
- **One legal question is unresolved:** whether a skill-based reward game touches the SA Lotteries Act or National Gambling Act. The design avoids all chance-based mechanics, which should keep it clear, but get a view before any real-money launch. [07_TRUTH.md §4.3](plan/07_TRUTH.md)
- **The unit economics are a plausibility model, not a forecast.** The two assumptions that move it most are the 70% acceptance rate and the MoMo disbursement fee. Say so.

---

## RELATIONSHIP TO THE EARLIER PLANNING

This supersedes the AMAZWI sections of `../02_ideas/THE_THREE_ENTRIES.md` and `../03_build/SUBMISSION_PACK_FITTED.md`, which described a different product — a prompted-recording app with rarity-based pricing and active learning as a centrepiece. Three things changed on evidence:

| Was | Now | Why |
|---|---|---|
| Prompted recording + reviewer queue | **Guessing game; agreement is the validation** | Track 2 fit, fraud, and quality all improve at once |
| **Rarity pricing** — rarer language earns more | **Coverage pricing** — the data gap earns more | Paying by ethnicity is a headline waiting to happen, and it is economically wrong |
| Active learning as the technical centrepiece | **Mechanism built, claim withdrawn** | The literature shows uncertainty sampling can underperform random for ASR, and it is not demonstrable in 26 hours |
| MMS / SeamlessM4T / InkubaLM in the stack | **Removed** | All CC-BY-NC. They cannot ship in a commercial product |

The earlier research (`../01_research/`, `../INFO_LOG.md`, `../01_research/VERIFICATION_STATUS.md`) remains valid and should still be read — particularly the corrections about load shedding, 2G sunset dates, and voice biometrics.
