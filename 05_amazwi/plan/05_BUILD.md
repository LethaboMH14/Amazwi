# AMAZWI — BUILD PLAN
### The two prep days · the 26.5-hour run · who does what

**Parent:** `00_MASTER_PLAN.md` · **Written:** 2026-08-31, 02:53 SAST

---

## 0. THE CLOCK

```
NOW              Monday 31 August 2026, 02:53
PREP             Monday 31 Aug + Tuesday 1 Sept        ~2 days
EVENT STARTS     Wednesday 2 September, 09:30
EVENT ENDS       Thursday 3 September, 12:00
EVENT LENGTH     26.5 hours, in person, overnight, on site
```

Registration opens earlier than 09:30. Briefing, mentor time and setup will eat the first hour. **Assume ~21 hours of real build time, minus sleep.** Plan the sleep. A team that codes through the night and pitches destroyed loses to a team that shipped less and can speak.

---

## 1. THE PRE-BUILD QUESTION — deal with this first, today

### 1.1 The rule, verbatim — no longer ambiguous

The terms are public at [momodevelopercommunity.mtn.com](https://momodevelopercommunity.mtn.com/p/momo_hackathon_2026_terms_and_conditions) and say this, word for word:

> **"3. Hackathon Rules**
> Participants will have 48 hours to ideate, build, and present a prototype/solution.
> **All submissions must be original and created during the hackathon. Pre-existing projects are not allowed unless approved by organizers.**
> **Use of open-source libraries and APIs is permitted, provided licenses are respected.**
> Teams must present their solutions within the allocated time."

**Read those two sentences together.** Pre-existing *projects* are prohibited. Open-source *libraries* are permitted. The line between them is whether the thing is generic and publicly available to anyone, or is your entry with a head start.

**That is exactly why §1.4's approach is the defensible one** — a genuinely generic, publicly published starter that contains no AMAZWI concept is a library. A private half-built AMAZWI is a pre-existing project. **But you should still get it in writing**, because "approved by organizers" is the only clause that removes all doubt.

⚠️ **Two other things the terms say that matter:**
- They state **"48 hours"**. Your invitation says Wed 09:30 → Thu 12:00, which is **26.5**. Ask at check-in which governs; it changes the gate schedule in §5.
- The IP clause says participants *"retain ownership"* but grants MTN a **"royalty free, sub-licensable and exclusive license to use the project descriptions, demos and products for marketing and promotional purposes."** The word **"exclusive"** over "products" — not just descriptions and media — is unusual even scoped to marketing. **Ask what it covers.** It probably does not bite, but you should know before you sign, not after.

### 1.2 Send this today
Send it to the address the invitation came from, and to the MoMo developer community, before 09:00.

> **Subject: Hackathon 2026 — clarification on preparatory work and starter code**
>
> Good day,
>
> We are Team Sonar, confirmed participants in the MoMo 24-Hour Mini App Hackathon on 2–3 September. We would like to be certain we comply with the terms and would appreciate written clarification on three points:
>
> 1. The terms state that submissions must be created during the hackathon. Does this permit the use of **generic, publicly available starter/boilerplate code** (project scaffolding, a MoMo API client, CI configuration) that is not specific to our concept, in the same way third-party open-source libraries are permitted?
> 2. Is preparatory **non-code** work — research, product design, written content, pitch material, and provisioning MoMo sandbox credentials — permitted before the event?
> 3. The registration form requests a repository URL. Should this repository be **empty at the time of submission**, or does the organiser expect it to contain the work produced during the event?
>
> We would rather over-comply than assume. We are happy to work within whatever the answer is.
>
> Kind regards,
> Team Sonar

### 1.3 What is unambiguously safe to do now, regardless of the answer

These are **not code** and no reasonable reading of the rules prohibits them. This is where most of your advantage actually lives:

- ✅ All research, strategy and product design *(done — `05_amazwi/`)*
- ✅ **The card content** — every target word and its banned words, in isiZulu and Setswana, written by us as first-language speakers. The single biggest content job and the most likely bottleneck. See §2.0.
- ✅ Every slide, the pitch script, the rehearsal
- ✅ MoMo developer account, sandbox credentials, and one successful end-to-end sandbox transaction
- ✅ Reading the Mini App PWA integration spec and design standards
- ✅ Provisioning deployment targets and a callback tunnel
- ✅ Recording your own sound design assets
- ✅ Generating card illustrations
- ✅ Practising the stack on something unrelated

### 1.4 The code question — the defensible position
If the answer is yes, or if no answer arrives: publish a **generic, public, open-source starter repository under your own name, dated before the event, that is not AMAZWI.** Something anyone could use — `momo-miniapp-starter`: a React PWA shell, a FastAPI service, a MoMo provider adapter with sandbox and demo implementations, and CI. It contains no AMAZWI concept, no game, no cards, no branding.

That is boilerplate, in the same category as any library you would install, and it is publicly verifiable as generic. Then **the AMAZWI repository's first commit happens at the venue**, and its history is clean and honest.

If the answer is a flat no: you lose perhaps three hours of scaffolding and nothing else. The design, content, credentials, sound and slides — the majority of the advantage — are unaffected.

### 1.6 Two more questions for the same email
1. **What time do submissions close, and what time do pitches start on Thursday?** The gate schedule in §5 assumes 08:30–11:30 is free for rehearsal. **If the form closes at 09:00, three gates are wrong** — and you will find out on the morning, which is the worst possible time.
2. **What does the "exclusive" licence in the IP clause actually cover?** (§1.1.)

### 1.5 The answer you must both have ready
A judge may ask what you built during the event. **Agree the exact sentence now and make sure both of you say the same one.** For example:

> *"Everything you're looking at was written here. We arrived with our research, our design, our game content, and a generic open-source starter we published publicly last week — the same way we arrived with React."*

Say it without defensiveness. An inconsistency between the two of you is far more damaging than the underlying fact.

---

## 2. MONDAY 31 AUGUST — content and credentials day

The theme of today is: **the things that cannot be done at 3am on Thursday.**

| Block | PLATFORM role | EXPERIENCE role |
|---|---|---|
| **06:45** ✅ | ~~Phone the native speakers~~ — **resolved, they are us.** Languages settled: **isiZulu (Sbu) + Setswana (Lethabo)**. See §2.0 for why this pair is the strongest available. | |
| **07:00** | Send the clarification email (§1.2) — **and add the two questions in §1.6** | — |
| **07:30–09:00** | 🔴 **HARD 90-MINUTE TIMEBOX.** MoMo developer account, subscription keys, provision **two** sandbox API users (one held in reserve, untouched, for the demo). Attempt one `transfer` end-to-end. **If SA disbursement is unreachable at 09:00, the labelled demo provider becomes the plan of record — decided Monday, not at 00:30 Thursday.** See §2.2. | **CARD CONTENT — the bottleneck.** 30 isiZulu cards. §2.0.1 |
| **10:00–13:00** | Join the developer community. Download the Mini App PWA integration spec + design standards. Read the sandbox Q&A threads. Write down every gotcha. | **CARD CONTENT — the bottleneck.** 30 Setswana cards; Sbu does 30 isiZulu in parallel. §2.0.1 |
| **13:00–15:00** | Draft the OpenAPI contract and the data model on paper. No code. Agree every request/response shape with EXPERIENCE. | Design tokens in a single file (`tokens.css`, per `04_DESIGN.md` §2). Colour, type, spacing, motion, three themes. |
| **15:00–17:00** | Provision Vercel/Cloudflare + a callback tunnel. Test the tunnel receives a POST. | Screen sketches for the five hero screens. Not Figma — paper or code. |
| **17:00–18:30** | *(joint)* Walk the whole user journey out loud, screen by screen, until you both describe the identical product. **This is Gate 1 and it is the most valuable hour of the week.** | |
| **18:30–20:00** | *(joint)* Record the sound design assets. Two people, a phone, a quiet room. `04_DESIGN.md` §4. | |
| **20:00–21:30** | Generic starter repo, if pursuing §1.4 | Card illustrations, batch-generated with a locked style prompt |

### 2.2 🔴 The sandbox will lock you out — budget it like fuel

MTN's sandbox has an **undocumented call-volume quota** with a multi-day cooldown. The error body, verbatim from the research file:

> `403 {"message": "Out of call volume quota. Quota will be replenished in 2.13:47:06."}`

**Two days.** That outlasts the event. Exhaust it at 03:00 Thursday and the payout beat is dead six hours before you pitch — and no numeric limit is published, so you cannot budget against it by calculation. Only by discipline:

1. **Automated tests never touch the sandbox.** The Hypothesis property tests in `02_TECH.md` §8 generate hundreds of retries and duplicate callbacks — pointed at the sandbox that is a quota incinerator. **They run against the demo provider, always.** This is now a standing rule (§9).
2. **Hard manual budget: 30 sandbox calls before the pitch.** Counted on a sheet of paper stuck to the wall. When it is gone, it is gone.
3. **Two sandbox API users**, provisioned Monday. The second is never used until the demo.
4. **`06_PITCH.md` §6 needs a new row:** *"sandbox quota exhausted"* — same move as sandbox down, labelled demo provider, said out loud.
5. ⚠️ **Sandbox currency is `EUR`, and `payerMessage` rejects `#`.** Your wallet shows rands. A rand figure beside a EUR provider reference is exactly what a fintech judge photographs. **Label the receipt `sandbox test transfer · EUR-denominated`** and mention it before they spot it.

Also from the same research: MTN's portal-linked **"South Africa Disbursement" appears to be a bulk-payroll product behind a commercial agreement, not a self-serve REST API.** SA availability of `disbursement/v1_0/transfer` in the sandbox is **NOT CONFIRMED**. Hence the timebox above.

### 2.0 ✅ RESOLVED — THE LANGUAGES ARE OURS

An earlier version of this plan flagged *"two first-language speakers, unconfirmed, needed for hours"* as the hardest-to-acquire dependency in the project, with no owner and no fallback.

**It has an owner. Lethabo is a first-language Setswana speaker; Sbu is a first-language isiZulu speaker.**

That removes the largest external risk in the plan and settles decision #2. **The two demo languages are isiZulu and Setswana**, and this is not a compromise — it is the strongest available pair:

| Reason | Detail |
|---|---|
| **One from each major family** | Nguni (isiZulu, isiXhosa, siSwati, isiNdebele ≈ 45% of home-language speakers) and Sotho-Tswana (Sepedi, Setswana, Sesotho ≈ 26%). Together ≈ 71% — so the architecture is demonstrated across both families rather than tuned to one |
| **It forces the two-model story** | The architecture split is *measured*, not preference: **w2v-bert-2.0 wins on Nguni, whisper-large-v3-turbo wins on Sotho-Tswana**, by 3–4 WER points each way (`D_SPEECH_AI.md` §1.2). One language from each means you **demonstrate both paths** instead of asserting one |
| **Setswana carries the best published result anywhere** | Swivuriso took Setswana from **223% → 13% WER** on fine-tuning. The most dramatic citable number in African ASR, and it is our language |
| **isiZulu carries the headline** | Largest home language at 24.4%, and the source of the **~146% → ~25% WER on one hour of data** figure that the whole pitch rests on |
| **Both are in Swivuriso** | The seed corpus (CC BY 4.0) covers both, so Track B fine-tuning has a real base on day one |

> **The pitch line:** *"We each brought our own language, and they're from different families — which is why our stack has two models instead of one."*

### 2.0.1 The risk that replaces it

The dependency is no longer *"will strangers show up?"* It is now **"do we have the hours?"** — a much better problem, but still a real one.

The four-hour estimate in §2.1 was for *translation*. The actual job is **game design in your own language**: choosing a word describable in 30 seconds, then the four banned words that are the most obvious routes to it. That is 2–3 minutes per card, plus ~3 more for `accepted_answers`. **120 cards is 7–9 hours** against a Monday already running 07:00–21:30.

**So: 30 cards per language, not 60.** Thirty well-built cards with rich accepted-answer sets beat sixty thin ones, **and the demo will use eight.** Build the eight demo cards first and to a higher standard than the rest.

**Two advantages you now have that a hired speaker could never give you:**
- You can write cards **while building**, in gaps, instead of scheduling someone else's time.
- You can **QA each other's language in the room** at 3am when something reads wrong — which is exactly when it will.

### 2.1 The card content — do not underestimate this
For each demo language you need **≈60 playable cards**: a target word plus four banned words, chosen so the word is describable in 30 seconds without them.

🔴 **Each card needs five fields, not two. Capture all five in one pass — a second pass does not exist.**
```
target_word        the answer
banned_words[]     the four most obvious ways to say it
accepted_answers[] EVERY correct variant: morphological forms, noun-class
                   prefixes, synonyms, the code-switched English equivalent.
                   For "isithuthuthu": isithuthuthu, sithuthuthu, izithuthuthu,
                   sthuthuthu, motorbike, i-motorbike
distractors[]      three plausible wrong options for multiple choice
is_gold            a few cards seeded to DO say the banned word — the honeypots
                   that make peer refereeing enforceable
```
**`accepted_answers` is three extra minutes per card with the first-language speaker already on the phone, and it is the single highest-value use of their time.** Without it, `is_correct` cannot be computed and every downstream number — reward, clarity, proficiency, corpus label — has no definition. See `02_TECH.md` §3.4.

**Rules for good cards:**
- Concrete and everyday beats abstract. *Taxi, kettle, gogo, spaza, blanket, rain, wedding, soccer.*
- The banned words must be the four **most obvious** ways to say it — that is what forces interesting speech.
- Culturally native, not translated from an English list. A card list translated from English produces English-shaped speech and defeats the purpose.
- Mixed difficulty, tagged, so difficulty calibration has a range to work with.
- **Every card written by its first-language speaker, and cross-checked by the other.** You are the speakers (§2.0) — but still read each other's aloud. A wrong word in a language-preservation app is the single most damaging detail possible.

**120 cards is roughly four hours of focused work with a native speaker on the phone.** Start it today. If you only get 30 per language, that is enough for the demo — but get them right.

---

## 3. ROLES

The plan document that seeded this work assigns **Lethabo → Platform, MoMo and Trust** and **Sbu → Product, Experience and Demo**. This plan uses role labels so it holds either way. **Confirm the assignment today and do not revisit it.**

| | **PLATFORM** | **EXPERIENCE** |
|---|---|---|
| Owns | FastAPI service · OpenAPI contract · Postgres schema and migrations · submission state machine · audio storage · guess assignment and agreement scoring · reward ledger · MoMo adapters · idempotency and reconciliation · consent enforcement · audit events · deployment | React Mini App · design system · the game screens · recorder and client quality gates · wallet and receipt UI · leagues · Archive · Impact Console presentation · demo narrative and pitch |
| Final say on | Money, data integrity, deployment safety | Scope and user experience |
| Never touches | Frontend state model | MoMo secrets · server-side payout state · migrations |

**Two rules that prevent the classic two-person collapse:**
1. **No feature starts without an agreed request/response example.** Write the JSON first, both agree, then build. This is the only defence against integration hell at 4am.
2. **Never edit the same file at the same time.** With two people this is entirely avoidable and entirely fatal when ignored.

---

## 4. TUESDAY 1 SEPTEMBER — rehearsal and readiness

| Block | Both |
|---|---|
| **09:00–12:00** | Finish card content. Every card native-checked. |
| **12:00–14:00** | Build the slide deck skeleton (`06_PITCH.md` §4). Placeholders where real screenshots will go. |
| **14:00–16:00** | **Rehearse the pitch three times, out loud, standing up, timed.** Not reading it — performing it. The opening 20 seconds and the closing 30 seconds should be memorised word for word. |
| **16:00–17:00** | 🔴 **LOAD-TEST the room-play at 20 clients, not 5.** Fifteen browser tabs plus five real phones, simultaneously, through the guest path. Five friends does not test 52 concurrent microphone permissions, 52 presigned-URL generations, connection-pool limits or a cold serverless start — and this is the only load test you will get. Also: **test on a real iPhone** (Safari needs a user gesture per audio context). |
| **17:00–17:30** | Write **every error-state string** into one file, as plain copy. Wiring pre-written strings at 07:00 Thursday is possible; writing them then is not. |
| **17:00–18:00** | **Pack.** See §7. |
| **18:00–19:00** | Agree the day-10-style kill rules (§6). Write them down. |
| **21:00** | **Sleep.** Both of you. A full night. This is a build instruction, not a courtesy — you are about to lose a night and you cannot bank sleep on Wednesday. |

---

## 5. THE 26.5-HOUR RUN

Every gate leaves the app **integrated and demoable**. There is no "frontend phase" and no integration phase at the end. If the clock runs out at any gate, you still have something to show.

> 🔴 **The gates are cut single-lane after 23:00.** An earlier version had G5 and G6 requiring both people while one of them was asleep — the sleep plan and the gate table were mutually exclusive. **All cross-lane integration now happens before 23:00 (G4) or after 07:00 (G7).** The overnight gates are each one person's work, verifiable alone.

| Gate | By | PLATFORM | EXPERIENCE | Exit condition |
|---|---|---|---|---|
| **G0** | **10:30** Wed | Clone the starter, deploy, health check, migrations | Clone, tokens, routes, **⚠️ the MoMo WebView heartbeat** | **The same repo runs on both laptops and is deployed** |
| **G1** | **12:30** | Seeded endpoints, **deterministic seed/reset** | All screens connected, loading/empty/error states | **Click welcome → receipt with no dead ends, and reset works** |
| **G2** | **14:30** | Identity adapter, consent persisted and **enforced server-side** | Age gate, language setup, consent UX, **the guest path** (§5.2) | **A user without consent cannot start a round** |
| **G3** | **17:00** | Submission IDs, private audio storage, quality metrics persisted | Mic permission, card, 30s timer, record, waveform, client quality gate, upload | **A recording made on one device plays on another after a refresh** |
| **G4** 🔴 | **19:30** | Guess assignment (no self-guessing), `is_correct` per §3.4, agreement resolution, **the banned-word referee + VOIDED**, **EXPIRED + two-guess minimum** | Listener flow, MCQ answer, **the "did they say it?" tap**, reveal, result screen | **A judge's clip is understood by a second device and the loop closes** |
| **↕ integration** | **19:30–23:00** | **Both awake. The only cross-lane window before morning.** Close the loop, fix the seams, seed realistic data. | | **The core game works end to end** |
| **G5** | **02:00** Thu | **PLATFORM ONLY, headless, verified by tests:** append-only ledger, integer cents, one reward per contribution, payout adapter, idempotency | *EXPERIENCE SLEEPS 23:00–03:00* | **Repeat approval and repeat payout create no extra money** |
| **G6** | **06:30** | *PLATFORM SLEEPS 03:00–07:00* | **EXPERIENCE ONLY, against endpoints that already exist:** wallet states, Voice Value Receipt, leagues, Archive | **Receipt and wallet render correctly from real data** |
| **G7** | **07:00–08:30** | **Both awake.** Rate limits, duplicate hash, consent on export, sanitised logs | Wire the **pre-written** error strings, mobile viewport, pre-warm | **Reset and run the full demo twice in a row with no manual DB edits** |
| **🔒 FREEZE** | **08:30** | **No new features. None.** Bugs that break the demo only. | | |
| **G8** | **08:30–11:30** | Rehearse the full pitch **four times**, once with something deliberately broken. Take the real screenshots. Finish the deck. Record the 90-second fallback video. | | **Both of you can run the entire demo alone** |

### 5.0 Four schedule corrections that make this achievable

- **G0 was impossible.** The event starts 09:30 and the first hour goes to registration and briefing — that left ~30 minutes for repo, FastAPI, Postgres, migrations, deploy, React shell, tokens and a typed client, on *both* laptops. Realistically 2.5–3 hours, and every gate downstream inherits the slip. **Fix: the entire G0 scaffold goes into the generic starter repo on Monday night** (§1.4 already sanctions it, and it is genuinely concept-free). Wednesday's G0 becomes clone, deploy, health check — forty minutes.
- **G4 moved earlier and got lighter.** It is the only gate containing a genuinely unsolved problem, the first cross-lane integration, and the mechanic the whole pitch rests on. **Cut the latent-trait scorer out of it** — θ/β/γ is twenty lines and can land at G6; a closed loop cannot. **Kill rule: if the loop has not closed by 22:00, listener input is multiple-choice only and free text is cut.**
- **Seed/reset moved to G1**, where the schema is small and the demo depends on it most. Writing it at 05:30 after twenty hours awake is how it ends up non-deterministic.
- **Error-state copy is written Tuesday**, as plain strings in a file. **Wiring pre-written strings at 07:00 is possible; writing them is not.**

> 🔴 **G4 is the real bottleneck, not G5.** It is the first gate where both lanes must integrate, and it carries the undefined-until-now `is_correct` function, the referee mechanic, the scoring update and the entire listener UI. **If G4 slips, everything after it is decoration.** Protect it: have `accepted_answers` in the seed data before Wednesday, and ship MCQ first — free text can arrive later or not at all.

### 5.1 Sleep
**Staggered, not skipped.** EXPERIENCE sleeps **23:00–03:00**; PLATFORM sleeps **03:00–07:00**. Four hours each.

**The gate table above is now built around this**, not in conflict with it: G5 is PLATFORM-only and headless, G6 is EXPERIENCE-only against endpoints that already exist. Neither requires the sleeping person. That is why the integration window is 19:30–23:00 while you are both awake and still functional.

### 5.2 The 03:00 rule
At 03:00, whatever is not working gets **cut, not fixed**. Write the list at 03:00 and cut it at 03:05. The single most common way hackathon teams lose is spending the last four hours on a feature nobody would have missed, and arriving unable to speak.

---

## 6. KILL RULES — agree these Tuesday, before anyone is emotionally invested

| If by… | …this is not working | Then |
|---|---|---|
| G3 (18:00) | Browser audio recording | **Stop.** Fall back to file upload of a pre-recorded clip and continue. Without audio there is no product — this is the one true blocker, so find out early. |
| G5 (00:30) | MoMo sandbox disbursement | Switch to the labelled demo provider. Say so on stage. Do not burn the night on someone else's sandbox. |
| G6 (03:00) | Story chain / Archive | Cut it. Umlozi alone is the whole thesis. |
| G7 (05:30) | Impact Console | Reduce to a single static screenshot on a slide. |
| Any time | The live room-play | Fall back to the judge-only demo. Rehearse both. |

---

## 7. THE PACKING LIST

Hardware failure is a more common cause of hackathon death than bad code.

**Essential**
- Both laptops + **both chargers**
- **Three phones minimum** — speaker, listener, spare. At least one Android.
- Phone chargers, a multi-plug extension lead, a 3-way adapter *(venue plugs are always scarce; this is the highest-return item on the list)*
- Mobile hotspot with data loaded on both networks
- USB-C ↔ HDMI adapter **and** a spare *(the projector will not have what you have)*
- Headphones for testing audio without disturbing the room

**The demo survival kit**
- The **90-second fallback video** on both laptops' local drives *and* on a phone
- The deck as a **PDF** on both laptops, not only in the cloud
- A printed one-pager with the architecture diagram, for the mentor conversations
- A pre-generated QR code as a PNG, in case live generation fails

**Human**
- Warm layer *(air conditioning overnight)*, toothbrush, deodorant, any medication
- Real food you like. Snacks that are not sugar.
- **A water bottle.** Dehydration at 4am is why people write bad code at 5am.

---

## 8. THE SUBMISSION FORM — draft it Tuesday, not Thursday

The form has hard character limits: **250 characters** for the short summary, **4000** for the detailed description and technologies. Draft them Tuesday and paste them Wednesday.

**Short summary — a starting draft (238 characters):**
> AMAZWI is the describe-it-without-saying-the-word game, played in your own language. If strangers across South Africa understand you, MoMo pays you. Learners guess to learn. What comes out is the SA speech data that has never existed.

Rewrite it in your own voice — but hold the shape: **the game, the money, the two sides, the output.** Recount characters after every edit.

⚠️ **Do not write "30 Seconds" anywhere in the submitted form** — it is a registered trade mark of a South African company, and using a competitor's mark as your own product descriptor in a submitted document is the one version of this that is genuinely risky.
✅ **Saying it out loud on stage as a comparison is fine** — *"it's the game every South African has played"* — that is ordinary nominative reference. The rule is: **spoken comparison yes, written product descriptor no.**

---

## 9. THE STANDING RULES

0. 🔴 **No automated test ever calls the MoMo sandbox.** Property tests, load tests, retries — all against the demo provider. The sandbox quota is finite, undocumented, and its cooldown outlasts the event. §2.2.
1. **Integrated at every gate.** Never more than 90 minutes from a demoable state.
2. **Small commits, descriptive messages, trunk-based.** No long-lived branches with two people.
3. **The demo runs from a deterministic seed/reset.** If it needs a manual database edit, it is broken.
4. **Both laptops run everything.** Test this at G0, not at 07:00 Thursday.
5. **Every claim in the pitch is checked against the running product** before you walk on stage.
6. **When in doubt, cut.** A smaller thing that works beats a larger thing that nearly works, every single time, and judges can tell the difference from across the room.
