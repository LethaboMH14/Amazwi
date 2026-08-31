# AMAZWI — RED TEAM
### Adversarial review of `plan/00`–`07` · written 2026-08-31 · ranked most severe first

> Every number below is computed from the plan's own stated inputs, not asserted.
> Each item is a thing that breaks, the file and section it breaks in, and a fix sized
> for the time actually remaining.

---

## THE SINGLE QUESTION YOU CANNOT ANSWER

> **"You've just told us no system on earth transcribes isiZulu. So how does your app know the speaker didn't just say the word?"**

Eight seconds to ask. It attacks the pitch's most honest beat (`06_PITCH.md` §3 at 2:30, `02_TECH.md` §5.1) and turns it into the thing that kills the mechanic. Answer it before it is asked — fix R1.

---

# SEVERITY 1 — STRUCTURAL

## R1 · The game's only rule is unenforceable, and enforcing it requires the product's own output

**Attack.** The speaker says the target word. Immediately, repeatedly. All three listeners guess correctly. The speaker is paid, `γ_speaker` rises, the clip enters the corpus as "validated."

**Why it works.** Nothing checks whether a banned word was spoken. It cannot: `02_TECH.md` §5.1 states plainly there is no working ASR for ten of eleven spoken official languages, and Tier 2 in §5 has no keyword-spotting stage. The referee for the game's single rule is exactly the capability AMAZWI exists to create. That is circular, and a technical judge closes the loop in one question.

Second-order damage is worse than the fraud: the dominant speaker strategy produces **degenerate speech** — the target word repeated — the precise opposite of the "spontaneous, unscripted, explanatory" speech that is the whole data thesis (`01_PRODUCT.md` §1 property table, `00_MASTER_PLAN.md` §1.2). The corpus fills with the worst possible content while every quality metric reads green. Listeners have no incentive to report it: they are paid for *agreeing*, and a speaker who says the word hands them a free correct answer. Speaker and listener interests are perfectly aligned against the data.

**Affected.** `01_PRODUCT.md` §1, §2 Mode 1 · `02_TECH.md` §4, §5.1 · `06_PITCH.md` §3 · `00_MASTER_PLAN.md` §1.2 — the claim "fraud is unprofitable by construction" is false as written.

**Fix — ~40 minutes at G4.** Make the referee the listener. One extra tap on the reveal screen:

> *"Did they say the word, or any banned word?"*  `[ No ]`  `[ Yes ]`

Two of three "Yes" votes → round `VOIDED`, no speaker reward, listeners still paid, `γ_speaker` penalised. One boolean column on `guess`, one branch in the resolver, one line of UI. It converts the hole into a mechanic using the agreement primitive you already trust, and it gives you a better answer than a defence:

> *"We can't transcribe it — so we don't. The room referees. Two listeners agreeing that you cheated voids the round. That is the same agreement primitive that validates the clip, pointed at the rule."*

Put the limit on slide 9 as well: *"banned-word enforcement is peer-reported, not machine-verified, until we have the data to build the verifier — which is the point."*

---

## R2 · The pitch states, twice, that real money moved — and your own research file says it cannot

**Attack.** A MoMo engineer hears *"real money has moved into a judge's MoMo wallet"* and *"Everything that just happened was real. Real recording, real peer validation, real MoMo disbursement."* They know the sandbox does not move money. You are now a team that oversold to the people who built the rail.

**Why it works.** `research/B_MOMO_API.md` §3, verbatim: *"Sandbox is a testing environment and therefore will not process real money."* Worse, §1a/§1b of the same file conclude that the product MTN's own portal links as **"South Africa Disbursement" is not a self-serve REST API** — it is a bulk-payroll batch product behind a signed three-year commercial agreement with African Bank, and *"a hackathon team cannot self-provision this in 48 hours."* SA availability of `disbursement/v1_0/transfer` in the sandbox is recorded there as **NOT CONFIRMED**. Your own documents already disagree with the pitch: `07_TRUTH.md` §7 says *"Disbursement runs in the MoMo sandbox, labelled as such."*

**Affected.** `06_PITCH.md` §2 (the governing decision) and §3 at 0:50 — both must be rewritten · `05_BUILD.md` §2, which treats "get one successful `transfer` end-to-end" as a two-hour Monday checkbox against an API that may not exist for South Africa.

**Fix — 5 minutes tonight.** Delete "real money" from both places. Replace with the line that scores higher:

> *"That is a sandbox disbursement — the sandbox does not move real rands, and we are not going to tell you it did. What is real is the state machine: reference persisted before the call, 202 means submitted not paid, repeat the call and no extra money exists. Point it at production and nothing changes but a header."*

Then move `05_BUILD.md` §2's transfer task to **07:30 Monday, hard 90-minute timebox**, with an explicit branch: if SA disbursement is unreachable, the labelled demo provider becomes the plan of record **on Monday**, not at 00:30 Thursday.

---

## R3 · The sandbox has an undocumented call-volume quota with a multi-day cooldown

**Attack.** You test payouts all Wednesday night. At 03:00 Thursday the sandbox returns `403 {"message": "Out of call volume quota. Quota will be replenished in 2.13:47:06."}`. The cooldown outlasts the event. The payout beat is dead and you learn it six hours before the pitch.

**Why it works.** Confirmed in `research/B_MOMO_API.md` §3 with the verbatim error body — and **no published numeric limit**, so you cannot budget against it. Meanwhile `02_TECH.md` §8 specifies Hypothesis property tests that *"generate random sequences of approvals, retries, duplicate callbacks and payout failures."* Pointed at the sandbox, that is a quota incinerator. `05_BUILD.md` §6 and `06_PITCH.md` §6 both plan for "sandbox is down"; neither plans for "sandbox has locked you out for two days," which has a different mitigation and a higher probability.

**Fix — 20 minutes, a rule not code.**
1. Property tests and all automated tests run against the **demo provider only**, never the sandbox. Add it to `05_BUILD.md` §9 standing rules.
2. A hard manual budget: **30 sandbox calls maximum before the pitch**, counted in a text file on the wall.
3. Provision **two** sandbox API users on Monday; one is held untouched in reserve for the demo.
4. Add to `06_PITCH.md` §6: *"sandbox quota exhausted"* → same move as sandbox down, labelled demo provider.
5. From the same research file: sandbox currency must be **`EUR`** and `payerMessage` rejects `#`. Your wallet says Rands; the provider says EUR. A Rand figure beside a EUR provider reference is exactly what a fintech judge screenshots. Label it `sandbox test transfer · EUR-denominated` on the receipt.

---

## R4 · There is no definition of "correct guess," and it is the load-bearing function in the whole system

**Attack.** *"How do you decide an isiZulu free-text guess is correct?"*

**Why it works.** `02_TECH.md` §3.1 declares `guess.is_correct` as a column. **No document anywhere defines the function that sets it.** For agglutinative Nguni languages this is not a detail — for the plan's own example card, *isithuthuthu*, valid listeners will type `isithuthuthu` / `sithuthuthu` / `izithuthuthu` / `i-motorbike` / `motorbike` / `sthuthuthu`. Exact match fails most of those. Edit distance over noun-class prefixes produces both false negatives and false positives. And you have explicitly excluded the only tools that would help: no ASR, no lemmatiser, MMS-LID licence-barred (`02_TECH.md` §5.2). Every downstream claim — the latent-trait scorer, the reward, the corpus label, the proficiency estimate, the clarity score — is a function of this undefined boolean.

It is also scheduled into **G4 at 21:00**, alongside guess assignment, agreement scoring, the θ/β/γ update, the listener flow and the result screen — the first gate where both lanes must integrate. **G4 is the real bottleneck, not G5.** If G4 slips, everything after it is decoration.

**Affected.** `02_TECH.md` §3.1, §4.1 · `01_PRODUCT.md` §3, §8.2 · `05_BUILD.md` §5 G4.

**Fix — write the function Monday afternoon, on paper, before any code.** Fifteen lines, specified per card and not per language:
- Normalise: lowercase, strip diacritics except where meaning-bearing, strip a whitelisted set of noun-class prefixes for that language, collapse whitespace and hyphens.
- Match against an **`accepted_answers` array stored on the card** — the target plus every native-checked synonym, common code-switched English equivalent, and morphological variant. Three extra minutes per card inside the §2.1 content job you are already doing with a first-language speaker. Nothing else you can build comes close to this for accuracy per hour.
- Levenshtein ≤ 2 against any accepted answer, after normalisation, for typos.
- Everything else is `false`. Ship **multiple choice as the primary listener input for the demo** — deterministic and demo-safe — with free text as the advanced mode.
- Add `accepted_answers TEXT[]` to `card` in `02_TECH.md` §3.1 **tonight**, so Monday's content job captures it rather than requiring a second pass.

---

# SEVERITY 2 — THE ECONOMICS DO NOT CLOSE

## R5 · Two listeners or three? The business case rests on the answer, and the documents give both

**Attack.** *"Your product says three listeners. Your unit economics charges for two. Which is it?"*

**Why it works.** `01_PRODUCT.md` §1 and §2 Mode 1, `02_TECH.md` §10 and `06_PITCH.md` §3 all say **three** listeners. `03_BUSINESS.md` §2.1 computes `5.71 × 2 listeners × R0.50`. Recomputed at three listeners, from the plan's own inputs and its own formulas:

| | 2 listeners (as modelled) | 3 listeners (as designed) |
|---|---|---|
| Listener rewards / validated minute | R5.71 | R8.57 |
| Cost per validated minute | R19.47 | **R23.53** |
| Cost per validated hour | R1,168 | **R1,412** |
| USD @ R16.15 | $72 | **$87** |
| Margin at $100/hr sale | 28% | **13%** |
| Margin at $150/hr sale | 52% | 42% |

The headline sentence in `03_BUSINESS.md` §1 — *"about R1,175 (US$73)"* — is a two-listener number attached to a three-listener product. At the real number the $100/hr price point in §4 earns a 13% margin, which is not a business.

**Two further arithmetic defects in the same section.**

- **§2.1 does not reproduce.** The stated components sum to **R19.47**, not the stated **R19.58**. The total was back-solved from an assumed 70% share (13.71 ÷ 0.70 = 19.58) and the 70% was then presented as a result. The document's own header promises *"every figure below is reproducible from the stated inputs."* It is not. A judge with a calculator finds this in thirty seconds.
- **The loop does not balance at three listeners.** Back out the plan's own R216/month: 63 accepted clips × R2 = R126, leaving R90 of listening = 180 guesses/month = **6.0 guesses per user per day**. Three submissions per user per day × 3 listeners = **9 guesses required**. The model supplies exactly 6 — it balances perfectly at two listeners and is **33% short at three**. One clip in three never resolves. The speaker's published reward sits in `PENDING` indefinitely, on the screen you have promised *"must never lie"* (`01_PRODUCT.md` §8.2).

**Affected.** `03_BUSINESS.md` §1, §2.1, §2.2, §2.3, §2.4 · `01_PRODUCT.md` §1, §2 · `06_PITCH.md` §3.

**Fix — 20 minutes tonight, and it is the cheaper direction.** **Move the product to two listeners.** Say *"two independent strangers"* everywhere. It preserves the output-agreement argument (two independent agreements is the ESP Game's own standard), it makes the economics literally true as written, it balances guess supply exactly, it halves time-to-resolution, and it makes the cold-start problem 33% smaller. Then correct R19.58 → R19.47 and R1,175 → R1,168, and add one line to §2.1: *"totals are the sum of the components; the 70% share is a result, not an input."* That is rigour you can point at.

---

## R6 · The listener reward is uncapped, pays 2–3× minimum wage, and its rule is stated two contradictory ways

**Attack (a) — the contradiction.** `01_PRODUCT.md` §5.1 rule 6: *"Listeners are paid a smaller fixed amount for a valid judgement, **whether or not the speaker was understood**."* `01_PRODUCT.md` §2 Mode 1: *"Listeners earn when their answer matches the independent majority."* `06_PITCH.md` §7: *"a listener earns only when their answer matches an independent majority."* These are different products. Rule 6 is also what `03_BUSINESS.md` §2.1 charges for — it pays listeners on all 5.71 *submitted* clips, including the 30% that are rejected. Your fraud answer on stage and your cost model are not describing the same system.

**Attack (b) — pay-always is a farm.** A listen-and-guess takes roughly 20–30 seconds. At R0.50 that is **R60–R90 per hour, 2.0–3.0× the national minimum wage** — the exact condition `03_BUSINESS.md` §3 declares fatal for the speaker side and then never applies to the listener side. The daily quest caps *plays*, not *guesses*. Nothing in `01_PRODUCT.md` §5.3, §7 or `03_BUSINESS.md` §3 caps listening. The R216/month figure silently assumes six guesses a day; no code enforces six.

**Attack (c) — pay-on-agreement is a Schelling point, not a defence.** If listeners are paid for matching each other, the optimal strategy for a listener who understood nothing is to type the *most likely* answer, not the correct one. With roughly 60 cards per language and a reveal screen that shows the answer after every round (`01_PRODUCT.md` §8.2 step 3), the pool is fully learnable in an evening. Convergence on high-frequency cards is free and requires no collusion at all. Output agreement only defends when the guess space is large and unshared — and you hand every listener the guess space, one card at a time.

**Attack (d) — the beginner path validates noise.** `01_PRODUCT.md` §4 gives learners **4-way multiple choice**. Pure chance, majority of three, is a **15.6% false-accept rate** on a clip containing no intelligible speech at all. At two listeners requiring both, 6.2%. Under `02_TECH.md` §10's "resolve on however many responded," a single MCQ listener gives **25%**. *"Gibberish earns nothing because nobody guesses it"* (`00_MASTER_PLAN.md` §1.2) is quantitatively false.

**Fix — 30 minutes total.**
1. **Pick rule 6.** Pay for a valid judgement regardless of outcome — it matches the cost model, it is fair, and it removes the Schelling-point incentive entirely. Delete the majority-match wording from `01_PRODUCT.md` §2 and `06_PITCH.md` §7 and replace the fraud answer with: *"listeners are paid for judging, not for being right, so there is nothing to converge on. What we check is that they are paying attention — gold cards of known answer, unannounced, and your reward stops if you fail them."*
2. **Cap listening at 10 paid judgements per day.** One counter, one line. Bounds listener cost at R5/day and closes the farm. State it in `01_PRODUCT.md` §5.3 as part of the daily-cap rule — that paragraph currently claims to bound cost per user and does not.
3. **Gold honeypots must be built, not listed.** `07_TRUTH.md` §5 already promises them. One in eight assignments is a card with a known answer; two consecutive failures and the listener earns nothing until they pass one. This is the only defence that survives (c) and (d) and it is roughly thirty lines.
4. **Never count MCQ-only agreement as corpus validation.** Free-text agreement validates; MCQ agreement scores XP. One flag on the guess row.

---

## R7 · Cold start: the mechanic is invisible in the demo and fatal on day one

**Attack.** *"It is Tuesday in Thohoyandou. I record a Tshivenda clip. How long until three people who speak Tshivenda hear it?"*

**Why it works.** Every property of the loop depends on a live pool of same-language listeners and no document models arrival rates. The demo hides this completely: 52 people in one room at one instant is the most favourable matching condition that will ever exist, and it is the only condition you will have tested. Concretely:

- **There is no expiry.** `02_TECH.md` §3.3: `DRAFT → RECORDED → QUALITY_PASSED → OPEN → RESOLVED → REWARDED`. No `EXPIRED`. A clip nobody guesses stays `OPEN` forever and its published reward stays `PENDING` forever — on the wallet screen that must never lie.
- **The stated fallback destroys the thesis.** `02_TECH.md` §10: *"Fewer than three listeners available → resolve on however many responded."* At n=1 there is no agreement, one stranger's guess becomes ground truth, and collusion costs one friend. The output-agreement defence — the core of `00_MASTER_PLAN.md` §1.2 — is switched off by an error handler.
- **The fraud incentive is inverted against the defence.** P(a chosen confederate lands among the three assigned listeners): pool of 1,000 → 0.3%; pool of 50 → 6%; **pool of 8 → 43%.** And `01_PRODUCT.md` §5.1 grants a coverage multiplier of up to **2.5×** precisely for the smallest, thinnest-covered pools. You pay the most where collusion is nearly free. That is a straight line from your own two rules.
- **"Small, frequent, inbound credits every day"** (`03_BUSINESS.md` §6.1) — the entire MoMo-activation argument — requires same-day resolution, which requires liquidity you will not have for months.

**Fix — 45 minutes.**
1. **Add `EXPIRED` to the round state machine** with a 48-hour timeout. On expiry the published reward is **paid anyway**, at half, funded as an acquisition cost, with an honest message: *"not enough Tshivenda listeners yet. We paid you anyway. We will go and find them."* That is a better story than any fraud control and it protects the never-lie promise.
2. **Minimum two guesses to validate, always.** If two are not available within 48 hours the clip pays but is marked `UNVALIDATED` and excluded from corpus export. Never resolve on one.
3. **Cap the coverage multiplier by pool size**, not by coverage alone: multiplier ≤ 1.0 until a language has ≥ 50 active listeners. One line, and it closes the inverted incentive.
4. **Say the cold start out loud on stage.** *"The hard problem here is not the game, it is liquidity — a clip needs listeners who speak that language. That is why we launch two languages and not twelve, and why the first cohort is a place, not a country."* You will be asked or you will not; either way it is better said by you.

---

## R8 · "Three clips buys a loaf of bread" is false by a factor of 3.3 — and your own research says so

**Attack.** Three clips at R2.00 is **R6.00**. A standard loaf is **R19.61** (StatsSA May 2026, `research/G_BUSINESS.md` line 145). R6 is **30.6% of a loaf**. You need **ten** clips.

**Why it works.** It is trivially checkable; it is the sentence you have twice designated as *the* line to say on stage — `03_BUSINESS.md` §7 (*"That is the sentence to use on stage. It is concrete, it is true"*) and `01_PRODUCT.md` §5.3; and your own research file states the correct relation explicitly: *"a per-contribution reward of R2–R5 sits at **10–26% of a loaf of bread**."* The plan contradicts its own evidence file to make a better-sounding sentence. That is the exact failure mode `07_TRUTH.md` exists to prevent, and if a judge catches it in the emotional close, every other number in the deck becomes suspect.

**Fix — 2 minutes.** Use a true one: **"a day's play is a third of a loaf; a week is two."** Or drop bread and use the sourced version: *"R216 a month — 58% of the SRD grant."* Correct it in both files tonight.

---

## R9 · The two-sided market has no second side in the build

**Attack.** *"Show me a learner paying."*

**Why it works.** *"Money crosses MoMo twice"* is the central strategic claim of the entire replan — `00_MASTER_PLAN.md` §1.3 (*"the money now flows in a circle instead of down a hole"*), the diagram at `06_PITCH.md` §3 3:30, and the Relevance-to-Fintech row in `00_MASTER_PLAN.md` §1.4. Now check the build: `01_PRODUCT.md` §10's non-negotiable list has **seventeen items and not one of them collects money from anyone.** `03_BUSINESS.md` §4 explicitly refuses to price the learner subscription and §6 ranks it fifth and *"the most speculative."* Meanwhile `06_PITCH.md` §7 asserts *"half our players are language learners who earn nothing and **pay to be there**"* — a population that does not exist, in a product with no payment-in path, at a price you have correctly declined to invent.

The learner leg carries the Track-2 defence, the sweatshop defence, the Duolingo defence and the fintech-relevance argument. All four rest on an unbuilt, unpriced flow.

**Fix — 90 minutes at G6, and it is worth displacing the story chain for.** Build the **inbound leg only**, as one screen: *"Sponsor a language — R20 funds 10 clips of Tshivenda."* Use MoMo **Collections** `requesttopay`, which `research/B_MOMO_API.md` §5 confirms is one of only four live sandbox products and is better documented than Disbursement. One payment in, credited to a named campaign, spending down live on the Impact Console. Then the diagram is real and the line changes to:

> *"Money crossed MoMo twice just now — in from a sponsor, out to a speaker, and we settled both legs."*

That single screen is worth more than the Archive, the leagues and the story chain combined, because it is the only thing that makes the fintech claim true. If it does not fit, **delete the "pay to be there" claim** from `06_PITCH.md` §7 and say *"learners are free today; the subscription is a hypothesis we have not priced, and we will say so."*

---

# SEVERITY 3 — THE DEMO

## R10 · The room-play cannot complete in 100 seconds, and the failure is public

`06_PITCH.md` §2–3 allocates **0:50–2:30** for 52 strangers to scan a QR, onboard, and guess. But `01_PRODUCT.md` §8.1 specifies onboarding as **five screens** — welcome, age gate, MoMo identity link, language multi-select, and **five independently declinable consent toggles** — budgeted at *"under sixty seconds"* by an optimistic author, for users who have never seen the app, on venue wifi, while being watched.

Failure modes, roughly by probability:

1. **Onboarding does not complete.** Most of the room is on the consent screen when the timer ends. The big-screen counter reads 7, not 52. The emotional peak deflates in public and there is no recovery line written for it.
2. **The hotspot fallback cannot carry the room.** `06_PITCH.md` §6 says *"venue wifi dies → phone hotspot, pre-tested."* An iPhone hotspot supports about 5 clients, Android about 10. That is a fallback for the judge-only demo and for nothing else. It is written as a mitigation and is not one.
3. **You tested N=5, on Tuesday at 16:00** (`05_BUILD.md` §4). N=5 does not test 52 concurrent microphone permissions, 52 presigned-URL generations, database connection-pool limits, or a cold serverless start. The one rehearsal scheduled cannot exercise the thing the pitch is being risked on.
4. **iOS Safari** requires a user gesture per audio context and blocks autoplay. A meaningful share of the room hears nothing and says so out loud.
5. **The demo does not demonstrate the product.** In the script the room hears the judge *speak in the room* and guesses from that. They never listen to a recording. The actual product — a stranger, later, elsewhere, playing back a clip — is never shown. A sharp judge notices, and the hardest real problem (asynchronous matching, R7) stays invisible.
6. **POPIA on stage.** You are recording and collecting the voices of ~52 people in 90 seconds. If consent is skipped for speed you have contradicted your own ethics slide live, in front of the people you just told about versioned granular consent.

**Is the risk worth it?** Yes. The upside is genuine and it is the only thing in the plan that changes what is happening in the room. **Keep it — with the entry cost removed.**

**Fix — 60 minutes at G7; it fixes items 1, 3, 5 and 6 at once.**
- **A guest path.** The QR opens straight into a listener round: one screen, one consent line (*"you are guessing only — we record nothing"*), no age gate, no MoMo link, no multi-select. Guessing collects no personal information, so the consent burden really is near-zero, and saying that out loud is a *stronger* ethics beat than the toggles.
- **Restructure the beat so the room listens to a recording.** The judge records for 30 seconds; the room then plays the clip on their own phones and guesses. That is the actual product, it is more impressive, and it removes the "they just heard him in the room" objection.
- **Seed the room.** Sbu and two briefed friends are in and playing before the QR goes up, so the counter is never zero.
- **Pre-warm everything** at 08:00 Thursday: warm deploy, sized connection pool, one dummy round already resolved.
- **Rehearse the deflation line:** *"Half the room got in — that is a hackathon wifi problem, not a product problem, and here is what the eleven who did just produced."* Then keep moving. The unrehearsed recovery is the failure; the failure itself is survivable.
- **Load-test on Tuesday** with 15 browser tabs plus 5 phones, not 5 friends. Twenty minutes, and it is the only load test you will get.

---

## R11 · You say "30 Seconds" on stage, and your own draft submission text leads with it

`07_TRUTH.md` §4.1 and `05_BUILD.md` §8 both instruct: never use "30 Seconds" as a product descriptor; it is a registered trade mark of Calco Games. Then:

- `06_PITCH.md` §3 at 0:20, spoken aloud: *"**AMAZWI is 30 Seconds** — the game every South African has played…"*
- `00_MASTER_PLAN.md` §2, the designated memory hook: *"AMAZWI is 30 Seconds, in your own language, and it pays."*
- `05_BUILD.md` §8's own draft short summary, three lines above its own warning: *"AMAZWI is **30 Seconds** in your own language."*

Three violations of an instruction the same author wrote. The submission form is the one carrying actual legal exposure, because it is a written commercial document.

**Fix — 10 minutes.** One replacement phrase everywhere: **"the describe-it-without-saying-it game every South African has played."** Rewrite the 231-character summary around it and recount. Rewrite the memory hook: *"AMAZWI is the describe-it game — in your language, and it pays."* Say the real one on stage **once**, unbranded, as an aside: *"you know the game we mean."* The room fills the blank themselves and you have said nothing.

---

## R12 · The close uses an identifiable, vulnerable, non-consenting person as an emotional device — against your own written instruction

`01_PRODUCT.md` §2 Mode 6: *"Do not name her, use her image, or imply endorsement without written permission. Cite the situation, not the person."* Then `06_PITCH.md` §4:30: *"a ninety-two-year-old woman the state calls a living human treasure, **who by every published account still struggles for money**."*

Not naming her is not anonymising her. There is exactly one such person, every South African in the room knows who she is, and you are asserting her financial circumstances — unverified; it is not in `07_TRUTH.md` §2.1's register — in a commercial pitch, for a prize, on video. To a cultural-sector judge that is precisely the extraction the product claims to oppose.

**Fix — 5 minutes.** Keep the fact, drop the person's circumstances:

> *"One of South Africa's languages has a single fluent speaker left. When she stops speaking, it stops existing. No app fixes that. But it does force the question underneath it: what is a language worth, and who gets paid for it?"*

Same force, zero exposure, and every word of it is in `07_TRUTH.md` §2.1 as verified.

---

# SEVERITY 4 — THE BUILD

## R13 · The sleep plan and the gate table are mutually exclusive

`05_BUILD.md` §5.1: one sleeps 23:00–03:00, the other 03:00–07:00. `05_BUILD.md` §5 gate table: **G5 at 00:30** requires PLATFORM (ledger, payouts, idempotency) *and* EXPERIENCE (wallet, pending/available/paid, transaction history). **G6 at 03:00** requires PLATFORM (league, coverage, impact aggregation) *and* EXPERIENCE (leagues, receipt, Archive, story chain). Both gates fall entirely inside somebody's sleep window, so half of each gate's work has nobody assigned to it. §5.1 then forbids the awake person from doing integration work — which is exactly what G5 and G6 are.

**Fix — 15 minutes with a pen tonight.** Re-cut the gates so each is single-lane:
- **G5 (00:30) is PLATFORM-only** — ledger and payout, headless, verified by tests. EXPERIENCE sleeps 23:00–03:00.
- **G6 (03:00) is EXPERIENCE-only** — wallet, receipt, leagues, against endpoints that already exist. PLATFORM sleeps 03:00–07:00.
- Move all cross-lane integration to **G4 (before 23:00)** and **G7 (after 07:00, both awake)**.

That preserves the sleep, which is the correct instinct, and makes the schedule executable.

## R14 · G0 and G7 are the underestimates; G4 is the bottleneck

- **G0 by 11:00.** The event starts at 09:30 and §0 already concedes the first hour goes to registration, briefing and setup. That leaves **about 30 minutes** for repo, FastAPI, health endpoint, Postgres, Alembic migrations, deploy, React shell, tokens, routes and a typed API client — running on **both** laptops. Realistic: 2.5–3 hours. G0 lands at 13:00 and every downstream gate inherits the slip. **Fix:** put the entire G0 scaffold in the generic starter repo on Monday night — `05_BUILD.md` §1.4 already sanctions this and it is genuinely concept-free — so Wednesday's G0 is clone, deploy, health check: forty minutes.
- **G4 (21:00) is the real bottleneck**, not G5. It is the only gate containing a genuinely unsolved problem (R4), the first cross-lane integration, and the mechanic the entire pitch depends on. **Fix:** move G4 to 19:30, cut the latent-trait scorer out of it (θ/β/γ is twenty lines and can land at G6 — a closed loop cannot), and add a kill rule: *"if the loop has not closed by 22:00, listener input becomes multiple-choice only and free text is cut."*
- **G7 (05:30, two and a half hours after twenty hours awake)** carries rate limits, duplicate hashing, consent-on-export, log sanitisation, deterministic seed/reset, every human error state and the mobile viewport pass. That is a full day of work. **Fix:** move `seed/reset` to G1, where the schema is small and the demo depends on it most; and write all error-state *copy* on Tuesday as plain strings in a file. Wiring pre-written strings at 05:30 is possible; writing them is not.
- **Contradiction:** `01_PRODUCT.md` §10 lists Inganekwane (item 13) on the *non-negotiable* list; `05_BUILD.md` §6 kill rules cut it at G6. Resolve tonight by removing it from §10. A non-negotiable list with negotiable items on it is not a list.
- **Missing open question.** `00_MASTER_PLAN.md` §6 asks six things and does not ask **what time submissions close and what time pitches start on Thursday**. G8 assumes 07:00–11:00 is free. If the form closes at 09:00, three gates are wrong. Put it in the same email as §1.2.

## R15 · The card content is correctly identified as the bottleneck and is under-resourced

`05_BUILD.md` §2.1 estimates 120 cards at *"roughly four hours of focused work with a native speaker on the phone."*

- That estimate is for translation. The actual job is **game design in a second language**: choosing a word describable in 30 seconds, then choosing the four banned words that are the most obvious routes to it. Done properly that is 2–3 minutes per card — **4–6 hours** — plus R4's `accepted_answers` array at roughly three more minutes each. Call it **7–9 hours**, against 6 hours scheduled across a Monday that already runs 07:00–21:30 with no slack.
- **The plan never names the native speakers.** Two first-language speakers, for two specific languages, available Monday and Tuesday, for hours, by phone, for free. That is the hardest-to-acquire dependency in the entire plan and it has no owner, no name and no confirmation step. If it fails there is no fallback, and §2.1 correctly says *"a wrong word in a language-preservation app is the single most damaging detail possible."*

**Fix — before the clarification email, first thing today.** Phone both speakers and get a committed two-hour window from each, in writing. Then cut the target to **30 cards per language** (§2.1 already permits it) and spend the saved time on `accepted_answers`. Thirty well-built cards with rich accepted-answer sets beat sixty thin ones, and the demo will use eight.

---

# SEVERITY 5 — CLAIMS, CONTRADICTIONS AND LOOSE ENDS

**R16 · It is not a Mini App.** The QR demo drops strangers into a standalone PWA outside the MoMo shell, while `01_PRODUCT.md` §8 assumes *"the user arrives already authenticated"* inside it. The whole "app #1 on the MoMo shelf" thesis (`00_MASTER_PLAN.md` §3) is then argued from a website. A platform judge asks *"so is this actually a mini app?"*
→ **Fix:** say it first. *"The room is playing the PWA build — same bundle, same API. The Mini App shell is the auth wrapper and we have built to the integration spec. What you are seeing is what would sit on the shelf."* Have the spec open on the second laptop.

**R17 · WAXAL is listed as both confirmed and unverified in the same document.** `07_TRUTH.md` §2.1 and §2.2 call it *"CONFIRMED and your strongest single fact"*; §2.3 lists *"Whether any South African language appears in WAXAL — check yourself"* as unverified. Your opening thirty seconds rests on it.
→ **Fix:** it **is** confirmed. `research/D_SPEECH_AI.md` §1.5 lists WAXAL's full 32-language roster with no SA language, and `research/C_COMPETITIVE.md` line 72 records a confirmed negative across four independently fetched sources. Delete the §2.3 line. One minute.

**R18 · "Up to 70% of call-centre conversations are not in English" is a competitor's marketing claim.** It is load-bearing in `03_BUSINESS.md` §1, §5.1 and §6.3 and in the pitch's reason #4, it originates with Botlhale via TechCabal (`research/G_BUSINESS.md` line 67), and it is absent from `07_TRUTH.md`'s claims register entirely.
→ **Fix:** attribute it aloud every time — *"Botlhale, who sell into that sector, put it at up to 70%."* Attribution makes it stronger, not weaker, and it survives the judge who knows the source. Add it to the register.

**R19 · ECAPA-TDNN/VoxCeleb has the licence problem one layer down.** `02_TECH.md` §5.2 rightly excludes MMS and SeamlessM4T as CC-BY-NC, then §5 Tier 2 ships an ECAPA-TDNN VoxCeleb model as Apache-2.0. The *weights* are Apache; **VoxCeleb itself is CC BY-NC-SA 4.0**, and the commercial status of a model trained on it is unsettled. Having made licence purity a pitch point, this is the one a careful judge finds.
→ **Fix:** drop speaker-uniqueness from the competition build — it is not on the demo path — or footnote it: *"weights are Apache-2.0, the training corpus is non-commercial; we would retrain on licensed data before shipping."*

**R20 · `03_BUSINESS.md` §2.4's scale table has no demand side.** 100,000 users produce 26,250 validated hours a month; at $100/hr that is $2.6m of inventory *per month* against a market for South African speech data that has never absorbed anything close. The same table also implies **R308 all-in cost per user per month**, contradicting §3's claim that the daily cap *"bounds the cost per user at R216/month."*
→ **Fix:** relabel the column **"cost to run,"** add *"demand at this scale is unproven; the 1,000-user row is the one we would underwrite,"* and correct the cap claim to *"bounds **contributor earnings** at R216/month; all-in cost per active user is about R308."*

**R21 · Three likely Q&A entries are missing** from `06_PITCH.md` §7: *"How do you score a free-text guess in isiZulu?"* (R4); *"Is your targeting active learning, and does it beat random?"* — `02_TECH.md` §5.3 has the correct, humble answer and it is buried in a tech doc; and *"Is this actually a mini app?"* (R16).
→ **Fix:** add all three and rehearse them. §5.3's line — *"the selection policy is in place; whether it beats random selection is an open question we have not powered a study to answer"* — is one of the strongest things in the plan and it currently never reaches the room.

**R22 · Event length is stated as both 24 and 26 hours inside one pitch.** `06_PITCH.md` §3 says *"twenty-six hours"* at 2:30 and *"in twenty-four hours"* in §7; `00_MASTER_PLAN.md` §5 says *"plus 24 hours"*; `05_BUILD.md` says 26.5.
→ **Fix:** pick **26 hours**. Trivial, but inconsistency inside one pitch reads as recitation rather than knowledge.

**R23 · Card illustrations leak the answer.** `04_DESIGN.md` specifies illustrations for concrete nouns — taxi, kettle, spaza. If one ever renders on the listener's screen the game is over; and even on the speaker's card it shifts the task from *describe the word* to *describe the picture*, which weakens the linguistic output.
→ **Fix:** speaker card only, never in the listener flow or the reveal. Write it as an explicit rule in `01_PRODUCT.md` §8.2.

---

# WHAT IS GENUINELY SOLID — stated once, then moved past

- **The ledger design.** Append-only, integer cents, derived balances, unique index on `(kind, round_id, user_id)`, `X-Reference-Id` persisted before the provider call, property-tested for conservation. `02_TECH.md` §3.2, §7.4, §8. Better than most production fintech, and the right thing to put on stage.
- **The claims register.** `07_TRUTH.md` §2.2's "do not say these" list — WAXAL's 11,000 hours, "MTN has no AI product," load shedding, "nobody has thought of using a game" — is disciplined, correctly sourced, and would have saved a lesser team from three public corrections.
- **The honesty beat at 2:30** (`06_PITCH.md` §3): *"we have not improved anyone's word error rate today."* Correct, rare, and it will win Technical Execution. Do not soften it.
- **Refusing to price the learner subscription** (`03_BUSINESS.md` §4). The right call, and the reasoning given for it is the right reasoning.
- **Coverage pricing over language-rarity pricing** (`01_PRODUCT.md` §5.2). A genuine save, correctly diagnosed.
- **The design budget.** `04_DESIGN.md` — 200 KB enforced in CI, no Three.js dependency, no image-generated South African people, orthographic correctness down to the click letters. Internally consistent throughout, and the CI size badge is a claim provable in ten seconds.
- **The Tier-0 client-side quality gate** (`02_TECH.md` §5). Correct engineering and a genuine ethical argument about the contributor's data cost. Say it on stage.

---

# THE ORDER TO FIX THINGS IN

**Tonight (about 2 hours, all editing, no code).** R2 (delete "real money") · R8 (bread) · R11 ("30 Seconds") · R12 (the close) · R5 (two listeners, everywhere) · R6.1 (pick rule 6) · R17 · R22 · R14's non-negotiable-list contradiction.

**Monday, first thing.** R15 (phone the native speakers and get committed windows — the longest-lead dependency in the plan) · R2's 90-minute timebox on SA disbursement · R3 (the sandbox call budget, written on the wall) · R4 (write the correctness function on paper; add `accepted_answers` to the card schema before the content job starts).

**Tuesday.** R10 (guest path, restructured room-play beat, load test at 20 clients not 5) · R13 (re-cut the gates single-lane) · R21 (three Q&A answers, rehearsed).

**At the event.** R1 (the peer-referee boolean at G4, forty minutes — the highest-value forty minutes in the entire build) · R7 (`EXPIRED` state and the two-guess minimum) · R9 (the sponsor screen, if G6 permits).
