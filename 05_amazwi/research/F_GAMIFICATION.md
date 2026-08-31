# F — GAMIFICATION, INCENTIVES AND THE LAW
### Evidence base for the AMAZWI game layer

**Compiled:** 2026-08-31 · **For:** `plan/01_PRODUCT.md` §5–§7, `plan/02_TECH.md` §4, `plan/07_TRUTH.md` §4.3

> **Source grading used throughout.**
> `[PRIMARY]` peer-reviewed, or the originating source · `[SECONDARY]` reputable reporting of a primary result · `[VENDOR]` marketing or blog content, treat with caution · `[UNVERIFIED]` could not be traced to a primary source — **do not put on a slide**

> ⚠️ **This file contains three findings that contradict the plan as written.** They are flagged 🔴 and listed again at the end.

---

## 1. MOTIVATION CROWDING-OUT — the single biggest risk in our design

### The core result
**Gneezy, U. & Rustichini, A. (2000), "Pay Enough or Don't Pay At All", *Quarterly Journal of Economics* 115(3): 791–810.** `[PRIMARY]`
https://rady.ucsd.edu/_files/faculty-research/uri-gneezy/pay-enough.pdf

The finding, stated precisely:

> The effect of monetary compensation on performance is **not monotonic**. When money was offered, a larger amount yielded higher performance — **but offering money did not always produce an improvement. Subjects offered small monetary incentives performed more poorly than those offered no compensation at all.**

**Read that against our design.** AMAZWI pays **R2.00 per validated clip.** That is squarely in the "small payment" regime where the literature says performance can fall *below* the unpaid baseline. This is not a hypothetical risk — it is the exact experimental condition.

Related: the effect fits best for individuals with **low pre-existing motivation** `[SECONDARY]` — which describes a user who opens the app because a friend said it pays, rather than because they wanted to play.

### Why this does not sink the design
Three structural features already in the plan work against crowding-out, and the reason each works is worth knowing:

1. **A dual population.** Learners play the guessing side for zero money. If the game only functions when paid, we will see it immediately — the learner cohort is a permanent, free control group. **This is the most valuable property of the two-sided design and it was not originally justified this way.**
2. **Payment attaches to outcomes, not activity.** Money follows *validated* contributions. Effort without comprehension earns nothing, so the payment is a signal of quality rather than a wage for time.
3. **The daily cap.** Past three plays, the only reason to continue is that you want to. The cap runs the "is this fun without money?" test continuously, on every user, forever.

### The design rule the literature actually supports
> **Either pay enough that the payment is the point, or pay little enough that it reads as a token of recognition rather than a wage — and never sit in the middle without a non-monetary reason to play.**

AMAZWI sits deliberately at the token end, and therefore **the non-monetary layer is not decoration. It is load-bearing.** The league, the streak, the Archive credit and the laugh when nobody guesses your clue are what stop the small payment from doing damage.

**⚠️ Falsifiable prediction to test on Tuesday:** run the game with five friends, with the money switched off. If they play three rounds and stop, the reward is doing all the work and quality will follow the money down.

---

## 2. DUOLINGO — what is actually published

⚠️ **Source-quality warning.** Duolingo publishes very little peer-reviewed material on retention mechanics. Most circulating numbers trace to a single essay by **Jorge Mazal, former Duolingo CPO**, on Lenny's Newsletter, and to conference talks — reputable first-hand accounts, but not controlled published experiments. **Attribute them; do not present them as independent research.**

| Claim | Grade | Note |
|---|---|---|
| **Leagues increased lesson completion by ~25%** | `[SECONDARY]` | Widely repeated from Duolingo-sourced accounts |
| Leagues increased both session starts and finishes in internal experiments before rollout | `[SECONDARY]` | |
| **600+ experiments run on the Streak feature alone**, purpose: improve DAU | `[SECONDARY]` | Jackson Shuttleworth, Group PM Retention |
| Gamification work grew **DAU ~4.5× over four years** | `[SECONDARY]` | Multi-causal; do not attribute to one mechanic |
| An **eight-word explanation** of what a streak is produced **10,000+ additional DAU** | `[SECONDARY]` | The cheapest lesson here: *explain the mechanic* |
| **Streak freezes exist specifically to minimise anxiety** | `[SECONDARY]` | Directly supports our design |

Sources: [Lenny's Newsletter — Jorge Mazal](https://www.lennysnewsletter.com/p/how-duolingo-reignited-user-growth) · [Behind the product: Duolingo streaks](https://www.getrecall.ai/summary/lennys-podcast/behind-the-product-duolingo-streaks-or-jackson-shuttleworth-group-pm-retention-team) · [Deconstructor of Fun](https://www.deconstructoroffun.com/blog/2025/4/14/duolingo-how-the-15b-app-uses-gaming-principles-to-supercharge-dau-growth)

**What we take:** leagues are the strongest single mechanic on the evidence available; **explain the streak in the interface in one short sentence**; ship the freeze from day one.
**⚠️ Do not put "25%" or "4.5×" on a slide as though it were ours or independently verified.**

---

## 3. STREAKS — and the failure mode that matters more than the benefit

**How they work.** Loss aversion — losing feels roughly twice as bad as an equivalent gain feels good — combined with sunk-cost psychology and the **goal-gradient effect** (effort rises as a goal nears). `[SECONDARY]`

### 🔴 The failure mode
> **A 2020 CHI study reportedly found streak anxiety was the top reason users abandoned habit apps, and users tracking via rigid streaks were 63% more likely to quit entirely after missing a single day.** `[UNVERIFIED]`

⚠️ **The 63% figure is repeated across secondary sources and I could not trace it to the underlying CHI paper. Do not cite the number.** Cite the direction, which is well supported: **Duolingo itself sees higher churn after a streak break** `[SECONDARY]`, and the mechanism is the *"what-the-hell effect"* — one missed day becoming total abandonment.

**Phillippa Lally (UCL)** on habit formation: **missing a single day has no measurable effect on long-term habit formation.** `[SECONDARY]` The damage is entirely psychological, which means it is entirely a design problem.

### The design consequence
**A rigid streak is a churn mechanic wearing a retention costume.** The literature's answer is a **graceful recovery path rather than a harsh reset**, and framing breaks as normal.

✅ **Our design is already right:** one automatic streak-freeze per week. **Strengthen it:**
- Never send a loss-inducing notification (*"your streak is about to die!"*). Send a positive one.
- On a break, show **"you've played 14 of the last 20 days"** — progress, not failure.
- Make the freeze **automatic and visible**, not a purchasable item.

---

## 4. OUTPUT-AGREEMENT GAMES — the mechanic we are actually building

**von Ahn, L. & Dabbish, L. (2004), the ESP Game.** `[PRIMARY]`
An output-agreement system **accepts a label only when two independent players agree, with no communication between them.**

That is exactly AMAZWI's validation rule, and it is worth knowing that our two-listener choice — arrived at through unit economics — lands on **the ESP Game's own standard**, not an approximation of it.

### The two anti-collusion devices, and we already have both
The ESP Game defends against collusion with:
1. **Taboo words** — certain words are forbidden as answers `[PRIMARY]`
2. **Random pairing per item**, so players never face the same partner repeatedly `[PRIMARY]`

> **Our banned words are the ESP Game's taboo-word device.** We adopted them for difficulty and speech quality; they are *also* the canonical anti-collusion mechanism in this class of game. That is a genuinely strong thing to be able to say, and it was not in the plan.

**Further reading:** [A game-theoretic analysis of the ESP game](https://dl.acm.org/doi/abs/10.1145/2399187.2399190), ACM Trans. Economics & Computation · [When majority voting fails](https://arxiv.org/pdf/1204.3516), arXiv 1204.3516 · [A Survey of Incentives and Mechanism Design for Human Computation](https://arxiv.org/pdf/1602.03277)

### Peer prediction — the more advanced option, and why we should not use it
**Bayesian Truth Serum (Prelec, 2004)** scores an answer by how much *more frequent* it is in the population than respondents themselves predicted; truthful in Bayesian Nash equilibrium, with no ground truth needed. `[PRIMARY]`

⚠️ **BTS is incentive-compatible only above a minimum number of agents, and that number depends on the prior — so it is unknown to the mechanism.** `[PRIMARY]` **Robust BTS (RBTS)** fixes this, giving strict incentive compatibility for every **n ≥ 3** without knowing the prior. `[PRIMARY]` — [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/8261)

**Verdict for AMAZWI: do not build it.** It requires eliciting a *prediction of others' answers* as well as an answer — a second question per round, which doubles friction in a 30-second game. Output agreement plus gold cards is the right cost/benefit. **But knowing RBTS exists, and being able to say why we chose not to use it, is a strong answer to a technical judge.**

---

## 5. QUALITY CONTROL IN PAID CROWDSOURCING

**Dawid–Skene** applies expectation-maximisation to estimate true labels by modelling each annotator's error rate, and is widely described as the reference method for label aggregation. `[PRIMARY]`
Majority voting is the baseline and **fails in noisy environments** `[PRIMARY]` — see [When majority voting fails](https://arxiv.org/pdf/1204.3516) and [Error Rate Bounds and Iterative Weighted Majority Voting](https://arxiv.org/pdf/1411.4086).

**Gold-standard items** are the consistent recommendation across the speech-annotation literature: insert verifiable items with known answers randomly into each task set, selected by experts, and use them to detect and remove spammers. `[PRIMARY]` — e.g. [SOMOS: Samsung Open MOS Dataset](https://arxiv.org/pdf/2204.03040), which does exactly this for speech ratings.

**Agreement metrics:** chance-corrected measures — **Fleiss' κ** and **Krippendorff's α** — are standard; raw agreement overstates reliability. `[PRIMARY]`
⚠️ **No universal α threshold for speech tasks was found.** Do not quote "α > 0.8" as a standard. Report the number you actually get.

Also: [Data quality in crowdsourcing and spamming behavior detection](https://link.springer.com/article/10.3758/s13428-025-02757-5), *Behavior Research Methods*, 2025. `[PRIMARY]`

**What we take:** gold cards are **not optional** — they are the single most-supported quality mechanism in this literature, and they are what makes our banned-word referee tap enforceable rather than decorative. Dawid–Skene-style listener reliability weighting is the right *later* upgrade; simple agreement plus gold cards is correct for the competition build.

---

## 6. 🔴 ELO / IRT — a finding that directly contradicts our architecture

The **Elo rating system** updates learner ability and item difficulty simultaneously after each response, requires no computationally intensive calculation, and is well established in adaptive educational systems. `[PRIMARY]` — [Applications of the Elo rating system in adaptive educational systems](https://www.sciencedirect.com/science/article/abs/pii/S036013151630080X), *Computers & Education*

That validates the approach in `02_TECH.md` §4.1. **But:**

> 🔴 **"In scenarios where items are selected adaptively based on the current ratings and the item difficulties are updated alongside the student abilities, the variance of the ratings across items and students artificially increases over time and as a result the ratings do not converge."** `[PRIMARY]`
> — [Keeping Elo alive: Evaluating and improving measurement properties of learning systems based on Elo ratings](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12784335/)

**In plain terms: if you both (a) choose which card to serve based on its estimated difficulty and (b) keep updating that difficulty, the estimates diverge instead of settling.**

### What this means for us — and the fix is cheap
We are **partly safe by accident**: our card selection is driven by **coverage need** (which language and speaking style is underrepresented), which is independent of the player's ability. That is not the failure condition.

**But the fix must be written down before someone "improves" it:**
1. 🔴 **Never select cards by estimated difficulty while difficulty is still being updated.** If adaptive difficulty is ever added, freeze β first.
2. **Anchor β on gold cards and freeze it there.** Gold cards have known difficulty and must not float.
3. **Use a decaying K** (Elo's learning rate). Fixed K forces a trade-off — large K tracks change but is volatile, small K is stable but slow. A **dynamic K** approach is published. `[PRIMARY]` — [Balancing stability and flexibility](https://link.springer.com/article/10.1007/s11257-025-09439-z), *UMUAI*
4. **Cold start** is a known, studied problem with published mitigations. `[PRIMARY]` — [An explanatory IRT method for alleviating the cold-start problem](https://link.springer.com/article/10.3758/s13428-018-1166-9), *Behavior Research Methods*

**The honest line for a judge:** *"It's Elo, with difficulty anchored on gold items and a decaying K — because the literature shows that if you adaptively select on difficulty while also updating it, the ratings don't converge."* That sentence demonstrates we read past the first result.

---

## 7. 🔴 TEAM vs INDIVIDUAL LEADERBOARDS — weaker evidence than the plan assumed

`01_PRODUCT.md` §7 asserts team competition "sustains engagement better than individual leaderboards." **The evidence is mixed, and the risk runs the wrong way for us.**

**In favour** `[SECONDARY]` — team-based competition is reported to outperform individual ranking; shared goals resonate more than individual point accumulation; team leaderboards enhance social relatedness and reduce intra-team friction.

**Against** `[PRIMARY]` — [As it unfolds: Exploring the impact of team-based gamification](https://www.sciencedirect.com/science/article/pii/S1041608024001584), *Learning and Instruction*, 2024:

> **The losing team demonstrated lower performance, confidence and engagement, while the winning team was merely comparable to the non-gamified control.**

Read that carefully: **the winners gained nothing measurable and the losers were harmed.** The same literature finds team gamification *may* have a detrimental effect overall, and that individual differences moderate everything — including the counter-intuitive result that people *more* positively disposed to gamification experienced a *larger* negative impact. `[PRIMARY]`

Also: [The use of leaderboards in education: a systematic review](https://onlinelibrary.wiley.com/doi/10.1111/jcal.13077), *J. Computer Assisted Learning*, 2024. `[PRIMARY]`

### 🔴 Why this matters specifically for AMAZWI
**Khayelitsha vs Soweto has a losing side every week** — and our whole thesis is that small, under-represented communities matter. A mechanic that systematically demoralises whoever loses is pointed directly at the users we most need to keep.

**The fixes, all cheap:**
1. **Tiered promotion/relegation, never one national table.** Most players sit mid-tier and can plausibly win their tier. This is Duolingo's actual design and it is why it works.
2. **Never render a "you lost" state.** Show movement against your own past week.
3. **Keep the language league.** A small language community can be **#1 nationally** in its own table — a structural fix for "big languages always win," and the plan already had this right.
4. **Celebrate the winner without ranking the bottom.** Show the top of your tier and your own position; do not show a national last place.

---

## 8. SOUTH AFRICA — cash vs airtime, and what a reward is worth

**Airtime as currency.** Across African markets airtime functions almost as a parallel currency and is frequently the *preferred* reward. `[VENDOR]`

> **But for South Africa specifically:** it reportedly "makes little difference whether cash or airtime is offered, as people spend substantial money on airtime anyway." `[VENDOR]` — [SagaPoll](https://sagapoll.com/airtime-surveys-in-africa/), [Reloadly](https://www.reloadly.com/blog/afrisight-airtime-rewards/)

⚠️ **Both sources are incentive-delivery vendors.** Directionally useful, commercially motivated. **Do not cite as research** — but it is enough to support the design decision: **cash into MoMo is fine for South Africa**, and it carries the additional strategic benefit of driving wallet activity, which airtime does not.

**Incentive size vs response rate.** `[PRIMARY]` A randomised controlled trial of promised and lottery airtime incentives for IVR surveys in Bangladesh and Uganda ([ScienceDirect](https://www.sciencedirect.com/org/science/article/pii/S1438887122003387) · [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9127645/)); and a Kenya experiment found that **increasing the incentive amount did not boost response rates** at around US$1 of airtime. `[SECONDARY]`

**Implication, and it is a good one for us:** paying *more* is not the lever. Above a threshold of respect, more money buys little additional participation — which is consistent with §1 and means **the R2.00 figure should be defended on fairness and unit economics, not on its motivating power.**

---

## 9. 🔴 THE SOUTH AFRICAN LEGAL POSITION — corrected

`07_TRUTH.md` §4.3 says a skill-based reward game "should sit outside" the National Gambling Act and Lotteries Act. **That framing is wrong in an important way.**

### The correct statute
**Promotional competitions have been governed by the Consumer Protection Act 68 of 2008, section 36 — not the Lotteries Act — since April 2011.** `[PRIMARY]`
Read with **regulation 11 of the CPA Regulations, GNR.293 of 1 April 2011.** The National Lotteries Commission still monitors compliance.
Sources: [NLC — Promotional competitions](https://www.nlcsa.org.za/promotional-competitions/) · [Cliffe Dekker Hofmeyr](https://www.cliffedekkerhofmeyr.com/en/news/publications/2020/corporate/corporate-and-commercial-alert-22-january-Rules-of-the-game-Keep-the-consumer-protection-act-in-mind-when-facilitating-promotional-competitions.html) · [Regulation of Promotional Competitions in SA](https://www.icla.up.ac.za/images/about/staff/van_heerden/Strachan_Regulation_2016.pdf) (Univ. of Pretoria)

### The definition, and the two-limb test
> A promotional competition is *"any competition, game, scheme, arrangement, system, plan or device for **distributing prizes by lot or chance**"* **if** (a) it is conducted in the ordinary course of business **for the purpose of promoting** a producer, distributor, supplier, or the sale of goods or services; **and** (b) any prize exceeds the prescribed threshold.

**The threshold is R1.00** — so effectively every competition is caught. `[PRIMARY]`
**"Prize"** is broad: reward, gift, free good or service, price reduction, concession. `[PRIMARY]`
**No consideration** may be required from the participant beyond reasonable transmission cost — **capped at R1.50** for electronic entry. `[PRIMARY]`

⚠️ **And the trap:** SA legal commentary repeatedly warns that the definition catches competitions **regardless of whether skill is required** — you cannot escape s36 merely by bolting on a skill element. `[SECONDARY]`

### Where AMAZWI actually sits
**Not legal advice. This is the analysis to take to a lawyer, not a substitute for one.**

| Element | Assessment |
|---|---|
| **Per-contribution payments (R2.00)** | **Very likely outside s36.** This is *consideration for a service rendered* — you recorded something and it was validated — not a prize distributed by lot or chance to promote goods. Different legal character entirely, closer to payment for work |
| **Leaderboards and leagues** | 🔴 **The real exposure.** If any **prize** attaches (and "prize" includes a free good, service or concession, above R1), and it promotes the business, s36 is arguably engaged |
| **Any randomised mechanic** | **Squarely in.** Spin-wheels, loot boxes, prize draws — already excluded from the design |

### The design rules that follow — all of which we were already doing, now for a better reason
1. **Leagues award non-cash points and status only. No prizes, ever.** This is why `01_PRODUCT.md` §5's wall between points and money exists — and it now has a *legal* justification, not just a product one.
2. **No chance-based mechanics anywhere.**
3. **Never require payment to participate.** Entry is free; the CPA's R1.50 transmission cap is irrelevant if we never charge.
4. **Publish the rules** and never adjust a published rate retroactively. Good practice regardless, and it is what s36 compliance looks like if we are ever deemed to be inside it.
5. **Get a legal opinion before any real-money launch.** The regulator is actively tightening: *"Regulators tighten scrutiny of till-slip and 'buy-and-win' competitions"* — [IOL, 14 May 2026](https://iol.co.za/business/2026-05-14-regulators-tighten-scrutiny-of-till-slip-and-buy-and-win-competitions/) `[SECONDARY]`

**The answer if a judge asks:** *"Our payments are consideration for validated work, not prizes distributed by chance, so we read them as outside CPA section 36 — which is the statute that actually governs promotional competitions in South Africa, not the Lotteries Act. That's also why our leagues award points and status only, never prizes, and why there's no randomised mechanic anywhere in the product. We'd take a formal opinion before a commercial launch."*

---

## THE MECHANIC SET I RECOMMEND

Ranked by evidence strength.

| # | Mechanic | Evidence | Grade |
|---|---|---|---|
| **1** | **Output agreement — two independent listeners** | ESP Game's own standard; the canonical GWAP validation mechanism | `[PRIMARY]` Strong |
| **2** | **Gold-standard honeypot cards** | The most consistently recommended quality control in the crowdsourcing and speech-annotation literature | `[PRIMARY]` Strong |
| **3** | **Banned words** | Doubles as the ESP Game's taboo-word **anti-collusion** device | `[PRIMARY]` Strong |
| **4** | **Random listener assignment** | ESP Game's second anti-collusion device; prevents repeated pairing | `[PRIMARY]` Strong |
| **5** | **Daily streak with an automatic weekly freeze** | Streaks work; rigid streaks cause abandonment; graceful recovery is the published fix | `[SECONDARY]` Good |
| **6** | **Leagues with tiered promotion/relegation** | Duolingo's strongest reported mechanic — but tiered, never one national table | `[SECONDARY]` Good |
| **7** | **Language league alongside place league** | Structural fix so small communities can win nationally | Design reasoning |
| **8** | **Elo-style scoring, β anchored on gold, decaying K** | Established in adaptive learning — **with the non-convergence constraint in §6** | `[PRIMARY]` Strong |
| **9** | **The Archive — permanent named credit** | Non-monetary recognition does not crowd out; the Wikipedia engine | `[PRIMARY]` (SDT) Good |
| **10** | **Explain the streak in one sentence in the UI** | Duolingo's eight-word change → 10,000+ DAU | `[SECONDARY]` Cheap, do it |

## MECHANICS TO AVOID, AND WHY

| Avoid | Reason |
|---|---|
| **Any randomised prize** — wheels, loot boxes, draws | CPA s36 exposure, and gambling-adjacent in a product aimed partly at unemployed young people |
| **Prizes attached to leaderboards** | The specific thing that would pull our leagues into s36 |
| **A single national leaderboard** | Creates a permanent losing majority; the 2024 *Learning and Instruction* result shows losers are harmed while winners gain nothing measurable |
| **Rigid streaks with a hard reset** | A churn mechanic in disguise |
| **Streak-loss push notifications** | Manufactures the anxiety the freeze exists to prevent |
| **Hearts / lives** | Punishes a bad connection, not a bad player — and our users have bad connections |
| **Paying listeners for being right** | Creates a Schelling point: the optimal strategy becomes guessing the *most likely* answer, not the correct one. Pay for the judgement |
| **Peer prediction / BTS** | Correct theory, wrong cost. Needs a second question per round in a 30-second game |
| **Raising the reward to drive participation** | Kenya RCT: more airtime did not raise response rates. Money is not the lever |

## HOW TO PAY WITHOUT DESTROYING QUALITY — the specific structure

1. **Pay for validated outcomes, never for activity.**
2. **Cap it.** R2.00 × 3 plays speaking, 10 paid judgements listening, hard ceiling **R11/day**. Past the cap it is a game or it is nothing — and that is the test running continuously.
3. **Keep two currencies and make points the loud one.** Points are celebrated; money is correct and quiet. This is also the legal wall (§9).
4. **Never cut a published rate retroactively.** The characteristic betrayal of this industry.
5. **Keep the free population.** Learners are the control group that tells us whether the game works.
6. **Credit, not just cash.** Named, permanent attribution in the Archive.
7. **Do not try to buy participation with a bigger number.** The evidence says it does not work, and §1 says it may actively harm.

---

## 🔴 THREE CORRECTIONS THIS RESEARCH MAKES TO THE PLAN

1. **`02_TECH.md` §4.1 — Elo non-convergence.** Adaptively selecting items on difficulty *while* updating difficulty makes ratings diverge. We are safe only because selection is driven by coverage, not ability. **Write the constraint down**: anchor β on gold cards, use a decaying K, and never add adaptive difficulty without freezing β first. (§6)
2. **`01_PRODUCT.md` §7 — team leaderboards.** The claim that team competition beats individual is **not settled**. Peer-reviewed evidence shows losing teams are harmed while winning teams gain nothing measurable. **Tier the leagues, never show a "you lost" state.** (§7)
3. **`07_TRUTH.md` §4.3 — the wrong statute.** Promotional competitions are governed by **CPA section 36**, not the Lotteries Act, and the definition catches competitions **regardless of skill**. Our per-contribution payments are very likely outside it as payment for services; **our leagues stay clear only because they award no prizes.** (§9)

## WHAT I COULD NOT VERIFY
- **The "63% more likely to quit" streak figure** — repeated widely, not traceable to the 2020 CHI paper. **Do not cite the number.**
- **A specific Krippendorff's α threshold for speech tasks** — no universal standard found. Report what you measure.
- **Duolingo's 25% and 4.5× figures** — first-hand but company-sourced, not independently replicated.
- **The SA cash-vs-airtime indifference claim** — vendor blogs only.
- **Whether any South African regulator has ever considered a paid microtask app** under s36. No precedent found either way.
