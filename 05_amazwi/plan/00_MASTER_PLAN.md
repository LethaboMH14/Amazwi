# AMAZWI — MASTER PLAN
### Team Sonar · Track 2, Entertainment & Lifestyle · MoMo Mini App Hackathon 2026

**Owner:** Lethabo · **Teammate:** Sbu · **Written:** 2026-08-30 · **Event:** 2–3 September 2026, The Forum, Bryanston

> **Read this file first.** Everything else in `05_amazwi/plan/` is a subordinate specification.
> Research evidence lives in `05_amazwi/research/`. Prior project history lives in `../MASTER_CONTEXT.md`.

---

## 0. THE 90-SECOND VERSION

You have a good plan. It has one structural flaw, and fixing it makes the product better on every judging criterion at once.

**The flaw:** AMAZWI as currently specified is *paid data labelling wearing a game costume*. Your own planning document admits this in its risk table. In Track 2 — **Entertainment & Lifestyle** — a judge who notices this has a fatal question and you have no structural answer, only a framing answer.

**The fix is not to describe it better. It is to change what it is.**

Three moves, in order of importance:

| # | The move | What it fixes |
|---|---|---|
| **1** | **Make the validation the game.** Stop asking people to "review recordings." Have them play a guessing game where *the guess IS the label*. Quality enforcement becomes intrinsic to the mechanic instead of bolted on. | Track 2 fit · fraud · data quality · fun |
| **2** | **Add the second population: learners.** People learning a South African language play the *same game* from the other side. They pay or subscribe; speakers earn. | Business model · inclusivity · "digital sweatshop" objection · Track 2 fit |
| **3** | **Anchor it on a game every South African has already played.** *30 Seconds* — describe the thing without saying the word, against a timer — was invented in South Africa and published in 1998. It is a fixture in South African homes. It is also, by accident, the most efficient natural-speech elicitation mechanic ever designed. | Instant comprehension · cultural authenticity · the memory hook |

**The new one-sentence product:**

> **AMAZWI is the describe-it-without-saying-the-word game, played in your own language against the whole country — where speaking pays you, and listening teaches you.**

A judge understands that sentence in full before you finish saying it. That is the bar, and the current version does not clear it.

---

## 1. WHAT CHANGED AND WHY

### 1.1 The problem with "a game where speaking your language pays"

Read the sentence honestly. The subject is *earning*. The verb is *pays*. It is an income product. Income products are excellent — they are just **Track 1**, and they invite the single most damaging question a judge can ask:

> *"So this is Mechanical Turk with a leaderboard?"*

Your existing answer is a framing answer: *lead with the game, never say "data annotation."* That works until someone looks at the actual loop, which is: receive prompt → record → someone reviews it → get paid. That is a task queue. A leaderboard on a task queue is still a task queue.

### 1.2 The turn

The insight comes from **Games With A Purpose** — Luis von Ahn's line of work that produced the ESP Game and reCAPTCHA. The principle:

> Do not build a task and add fun. Build a game people would play anyway, and let the labels fall out as exhaust.

reCAPTCHA digitised millions of books not because people wanted to digitise books, but because they wanted to get past the box. The ESP Game labelled images because two strangers trying to guess the same word is genuinely fun.

**Applied to speech:** the reason "validation" feels like work is that we designed it as work. *Accept / Reject / Flag* is a moderation console.

Now replace it:

> **Player A** gets the word **"ISITHUTHUTHU"** (motorbike) and four banned words. She has 30 seconds to make people understand it **in isiZulu** without saying any of them.
>
> **Players B, C, D** — strangers, somewhere in South Africa — hear the clip and type what they think the word is.
>
> If they get it, everyone scores. If nobody gets it, nobody scores.

Look at what that single mechanic does:

- **It is fun.** It is a party game. This is not an assertion — it is the best-selling South African board game.
- **It elicits spontaneous, unscripted, natural speech** — the precise category that does not exist in any dataset, because read-aloud corpora are easy and conversation is hard.
- **It validates semantically, not acoustically.** A correct guess proves the utterance was intelligible, on-topic and in the right language. No reviewer had to decide that.
- **It makes fraud expensive.** There is no "accept" button to game, and farming the speaker side means colluding with strangers you cannot choose. ⚠️ **It is not self-enforcing** — the one rule the mechanic cannot check by itself is whether the speaker just said the word, and the fix is peer refereeing plus gold honeypots. `01_PRODUCT.md` §1.1. Do not claim "unprofitable by construction" on stage; it is false and a technical judge will find it in one question.
- **The guesses are free labels.** You get a semantic target and a distribution of what listeners heard.
- **Nobody validates anything.** They play.

That is the aha. Everything downstream gets easier.

### 1.3 The second turn: two populations, opposite motivations, one loop

Ask who plays this game.

**Population A — the speaker.** Speaks isiZulu natively. Wants income, pride, competition. This is your existing user.

**Population B — the learner.** Wants to *understand* isiZulu. A Sandton twenty-something whose parents never taught them. A call-centre trainee. A nurse in Limpopo posted to a Tshivenda-speaking district. A German expat. An isiXhosa speaker who wants Sesotho.

**Population B playing the guessing side of the game is doing validation.** They are not doing it for money. They are doing it because guessing what a native speaker just described *is how you learn a language* — comprehensible input, delivered by a real human, at speed, with immediate feedback.

This is the whole thing. Two populations with completely opposite motivations, producing exactly what the other one needs, inside one loop:

```
    SPEAKERS                                    LEARNERS
    (supply speech)                             (supply comprehension labels)
         │                                            │
         │  record a 30-second clue                   │  guess what it was
         ▼                                            ▼
    ┌──────────────────────────────────────────────────────┐
    │                    THE AMAZWI LOOP                    │
    │   agreement between strangers = validated data        │
    └──────────────────────────────────────────────────────┘
         │                                            │
         ▼                                            ▼
    earns MoMo                                  learns the language
    (paid out)                                  (pays / subscribes)
```

**The money now flows in a circle instead of down a hole.** It is not "MTN funds a data-collection campaign." It is a marketplace where MTN owns the rail, takes the spread, and keeps the corpus as exhaust. Every rand crosses MoMo twice.

### 1.4 What this fixes, criterion by criterion

| Official criterion | Before | After |
|---|---|---|
| **Innovation & Creativity** | A voice recorder with a leaderboard | A two-sided language market where a party game *is* the validation mechanism — never built at consumer scale, for African languages, on a mobile-money rail |
| **Relevance to Fintech** | MTN pays users (a cost centre) | Learners and sponsors pay in, speakers earn out, MoMo settles both legs (a rail with a spread) |
| **Feasibility & Scalability** | Needs sponsors to exist before it works | Self-funding at the margin; the learner side monetises on day one |
| **Technical Execution** | Quality control bolted on | Quality is a property of the mechanic; the ML is real and demonstrable |
| **Presentation & Pitch** | "We pay you for voice data" | "It's 30 Seconds, in your language, against the country" — the room understands instantly |

And critically: **it is now unambiguously Entertainment & Lifestyle.** It is a social game and a culture app. The earning is a *feature*, not the category.

---

## 2. THE PRODUCT IN ONE PAGE

### Name
**AMAZWI** — *the voices* (isiZulu / isiXhosa). Keep it. It is plural and collective, which is now literally what the product is.

### Tagline
> **Every voice counts. Yours pays.**

Alternates, ranked: *"Speak. Guess. Earn."* · *"The country is listening."* · *"Play with your voice."*

### The memory hook — the sentence judges repeat in deliberation
> **"AMAZWI is the describe-it game — in your language, and it pays."**

⚠️ **Never write "30 Seconds" as a product descriptor** — it is a registered trade mark, and the submission form is a written commercial document. Say it aloud **once**, unbranded, as an aside: *"you know the game we mean."* The room fills the blank themselves and you have said nothing. `07_TRUTH.md` §4.1

### The five pillars

**1 · THE GAME (Umlozi — "the whistle")**
The core loop. Describe-it-don't-say-it, 30 seconds, in your language. Strangers guess. Agreement pays both sides. Four other modes rotate in (§ `01_PRODUCT.md`).

**2 · THE LEAGUE**
Language leagues and place leagues. Khayelitsha vs Soweto. Thohoyandou vs Giyani. Weekly promotion and relegation. Non-cash points, strictly separated from money.

**3 · THE WALLET**
Published reward before you play. Pending → available → paid. Real MoMo disbursement. A wallet screen that never lies about state.

**4 · THE ARCHIVE**
Every validated contribution is deposited into a named, permanent, credited national voice archive. You can see yours. You can hear the story your community built. This is the emotional core and the answer to "am I being harvested?"

**5 · THE ENGINE (Impact Console)**
The MTN-facing view: coverage by language, validated minutes, acceptance rates, consent-active corpus, rewards committed and paid, and the next language the budget should go to.

---

## 3. THE THESIS FOR MTN

Judges are not scoring your app. They are unconsciously asking one question:

> *Could this be app #1 on the MoMo shelf in Johannesburg in six months?*

MTN signed **Ant International in June 2026** to rebuild MoMo as a super app with a mini app platform. They have bought the shelf. **The shelf is empty.** They are not running a charity hackathon; they are recruiting supply. So the winning entry does not look like a science project — it looks like a **launch partner**.

### The four statements for the "Why MTN" slide

**1 · It is a daily lifestyle loop, which is exactly what the Mini App platform is short of.**
MTN's own results attribute growth to high-frequency everyday use cases. A language game with streaks and leagues is a daily-open product. Bill payment is a monthly-open product.

**2 · It makes MoMo structurally necessary, not decorative.**
Cent-scale payouts to tens of millions of wallets are impossible on card rails — the interchange alone exceeds the payment. Two-sided settlement between learners and speakers requires a wallet on both ends. Remove MoMo and there is no product. That is the difference between using MoMo and *needing* it.

**3 · It builds MTN the one asset it does not have and cannot buy.**
MTN has committed publicly to AI and has no consumer AI product and no proprietary African-language asset. Google's WAXAL programme funded East and West Africa. Existing South African corpora are valuable but static, read-aloud, and thin on conversational and code-switched speech. AMAZWI is a *continuous acquisition layer* for the speech that is missing, with per-user consent lineage — which no existing corpus has.

**4 · MTN is its own first customer.**
This is the line that closes it. MTN South Africa runs customer service in a country where English is the fifth home language. MTN's own IVR and MoMo support do not work in isiXhosa. **The first buyer of AMAZWI's output is standing in the room.** Every other data play has to go find a customer. This one starts inside the building.

### Theme alignment — *Maximum Velocity, As One*
- **Maximum Velocity:** targeted acquisition. The system asks for the speech it most needs next, not random samples.
- **As One:** speakers, learners, language communities, MTN and African developers in a single value loop — and on stage, literally: the whole room plays at once (§ `06_PITCH.md`).

---

## 4. WHAT WE ARE DELIBERATELY NOT BUILDING

Scope discipline is the difference between a demo and a story about a demo. **Not in the competition build:**

- Whisper large-v3 or W2V-BERT fine-tuning on the day *(pre-trained results may be shown, clearly labelled and dated)*
- Speaker biometric authentication *(voice is the interface, never the lock)*
- Celery, Redis, Kafka, DVC, MLflow, W&B *(name them on the roadmap slide; do not run them)*
- A full feature-phone IVR path
- All twelve languages *(ship the ones you can actually quality-assure)*
- Cross-market deployment
- A raw-audio marketplace *(governed model/API access instead — see `03_BUSINESS.md`)*
- Complex collusion detection *(the mechanic already makes collusion expensive)*

**The rule:** every feature must improve a judging score, keep the demo alive, or reduce a serious ethical or financial risk. If it does none of those, it does not get built.

---

## 5. THE HONEST PROBLEMS, STATED UP FRONT

Stating these yourself is worth more than surviving them under questioning.

| Problem | Status | Where it is handled |
|---|---|---|
| **The T&Cs prohibit pre-existing code, and you intend to pre-build** | 🔴 Unresolved and material | `05_BUILD.md` §1 — includes the exact email to send today and a compliant fallback |
| **"30 Seconds" is a registered trade mark of a South African company** | 🟡 Manageable | Mechanics are not protectable; the name and card content are. Never brand it *30 Seconds*; reference it only as a cultural touchstone. `07_TRUTH.md` |
| **Two people, two days, plus 26 hours** | 🟡 The real constraint | Scope is cut to a single demonstrable loop. `05_BUILD.md` |
| **Learners are a second product; second products kill hackathon entries** | 🟡 Design risk | Build the *speaker* loop fully; the learner side is the same screen with the reward hidden. One codebase, two roles. `01_PRODUCT.md` §4 |
| **Paying for contributions can destroy intrinsic motivation** | 🟡 Real, evidenced | Payment structure designed against the crowding-out literature. `01_PRODUCT.md` §6 |
| **This collects voice data from people who need money** | 🔴 The ethical core | Adults only, versioned consent, published rates, revocable, credited. `07_TRUTH.md` |
| **Which MoMo APIs are actually enabled in the SA hackathon sandbox** | 🔴 Unknown | Provider adapters so the product survives any answer. `02_TECH.md` |
| **African Next Voices / Swivuriso is a much closer competitor than the earlier docs assumed** | 🔴 Must be handled on stage | Gates-funded, explicitly pays contributors, covers the same seven SA languages. The move is to **build on it and credit it**, not to claim it doesn't exist. `07_TRUTH.md` §3 |
| **Duolingo already tried and killed crowdsourcing inside a learning app** | 🟡 The sharpest precedent objection | Immersion and Incubator both retired. Our answer must be that guessing *is* the lesson, not a tax on it. `07_TRUTH.md` §3 |

---

## 6. OPEN QUESTIONS — CHASE THESE BEFORE WEDNESDAY

1. **Email the organisers today** about pre-built code. Draft in `05_BUILD.md` §1.
2. **Which MoMo APIs are enabled for the event sandbox in South Africa?** Specifically: is *Disbursement* live, and are *Identify* and *Get Consent* available? Ask on the MoMo developer community now.
3. **Minimum disbursement amount and currency in the SA environment.** Determines whether cent-scale payouts accumulate to a threshold.
4. **Is judging per-track or overall?** Still never asked.
5. **Do you get day-of credentials, or must you arrive with your own sandbox account?**
6. **Native-speaker sign-off** on every word of in-game copy before it goes on screen.

---

## 7. FILE MAP

```
05_amazwi/
├── plan/
│   ├── 00_MASTER_PLAN.md   ← you are here
│   ├── 01_PRODUCT.md       game design, every screen, every flow, gamification
│   ├── 02_TECH.md          architecture, AI engineering, data pipeline, security
│   ├── 03_BUSINESS.md      revenue, pricing, unit economics, the buyers
│   ├── 04_DESIGN.md        visual system, motion, 3D, sound, mockup pipeline
│   ├── 05_BUILD.md         pre-build plan + the 24-hour run
│   ├── 06_PITCH.md         stage choreography, slides, demo script, Q&A
│   └── 07_TRUTH.md         verification, claims audit, red team, ethics
└── research/
    ├── A_MTN_CORPORATE.md  ├── E_SA_CULTURE.md
    ├── B_MOMO_API.md       ├── F_GAMIFICATION.md
    ├── C_COMPETITIVE.md    └── G_BUSINESS.md
    └── D_SPEECH_AI.md
```
