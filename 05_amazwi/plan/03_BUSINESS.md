# AMAZWI — THE BUSINESS CASE
### Unit economics · pricing · the buyers · how MTN makes money

**Parent:** `00_MASTER_PLAN.md` · **Written:** 2026-08-31
**Evidence:** `research/G_BUSINESS.md` · **Arithmetic:** computed, not asserted — every figure below is reproducible from the stated inputs.

---

## 1. THE ONE-PAGE ANSWER

> **AMAZWI produces one validated hour of South African conversational speech for about R1,175 (US$73), of which about 70% reaches the person who spoke and the people who understood them. The same hour, collected by the grant-funded academic fieldwork model, costs roughly US$244.**
>
> **We are not cheaper because we pay people less. We are cheaper because we deleted the fieldwork.**

That sentence is the entire commercial thesis, and it is the rare case where the efficient answer and the ethical answer are the same answer.

MTN's return does not depend on AMAZWI's revenue at all. It depends on four things MTN already wants:

| | What MTN gets | Why it is credible |
|---|---|---|
| **1** | **MoMo SA activation** — a daily reason to open the wallet | MoMo SA has ~13m *registered* users; in the 2020 relaunch only ~207k of 2.5m registered were active. Activation is MTN SA's live problem, and this is a daily-open product |
| **2** | **A licensable African-language speech asset** | MTN's own CEO has said Africa cannot be left out of the AI era. MTN owns no language asset. Google's WAXAL contains **zero South African languages** |
| **3** | **Cost avoidance inside MTN** | Botlhale AI — who sell into that sector — put it at up to 70% of South African call-centre conversations happening in languages other than English, while the tooling only processes English |
| **4** | **Supply for an empty mini app shelf** | The Ant International platform launched with Nigeria first. MTN needs proof that African developers will build on it |

---

## 2. UNIT ECONOMICS

### 2.1 The model
To produce **one validated minute** — four accepted 15-second clips, at **two listeners per clip**:

```
accepted clips needed          4          (60s ÷ 15s)
submitted clips needed         5.71       (4 ÷ 70% acceptance)

speaker rewards                R8.00      (4 × R2.00)
listener rewards               R5.71      (5.71 × 2 listeners × R0.50)
MoMo fees @ 2%                 R0.27
                              ───────
DIRECT SUBTOTAL                R13.99
platform overhead @ 40%        R5.60      (engineering, hosting, review, compliance)
                              ───────
TOTAL PER VALIDATED MINUTE     R19.58
TOTAL PER VALIDATED HOUR       R1,175     ≈ US$73  @ R16.15/USD

cash reaching people           R13.71     (speaker + listener rewards)
SHARE REACHING PEOPLE          70.0%      ← a result, not an input
```

**The total is the sum of the components.** Overhead applies to the full direct cost including fees. The 70% share is derived from the components, not assumed and back-solved.

> ⚠️ **Two listeners, not three — and this is why.** An earlier draft specified three listeners in the product and charged for two here. At three, the cost is **R23.66/minute, R1,420/hour, US$88**, and the margin at a $100/hr sale price falls from 27% to **12%**, which is not a business. Three also breaks guess supply: three plays a day × three listeners demands nine guesses per user per day, while the R216/month figure supplies exactly six. One clip in three would never resolve, and its reward would sit in `PENDING` forever — on the screen that must never lie. **Two listeners balances the loop exactly.**

### 2.2 Sensitivity — the two assumptions that actually matter

| R/clip | Daily quest | Cost/validated hr | US$/hr | Contributor earns/mo | vs SRD grant |
|---|---|---|---|---|---|
| R1.50 | 3 | R1,004 | $62 | R184 | 50% |
| **R2.00** | **3** | **R1,175** | **$73** | **R216** | **58%** |
| R2.50 | 3 | R1,346 | $83 | R248 | 67% |
| R3.00 | 3 | R1,518 | $94 | R279 | 75% |
| R2.00 | 5 | R1,175 | $73 | R360 | 97% |
| R3.00 | 5 | R1,518 | $94 | R465 | 126% |

*(SRD grant reference: R370/month. Cost per hour is independent of quest size — the quest sets what one person earns, not what a minute costs.)*

### 2.3 Margin
| Sale price | Comparable | Margin at R1,175/hr cost |
|---|---|---|
| $100/hr | Literature's "conventional cost floor" for low-resource collection | **27%** |
| $150/hr | Top of the conventional range | **51%** |
| $175/hr | Defined.ai blended data-access rate | **58%** |
| $244/hr | African Next Voices' all-in programme cost | **70%** |

### 2.4 Scale — supply side only
| Active users | Validated hours/month | **Cost to run**/month | All-in cost per active user |
|---|---|---|---|
| **1,000** | **262** | **R308,000** | **R308** |
| 10,000 | 2,625 | R3.1m | R308 |
| 100,000 | 26,250 | R30.8m | R308 |

> ⚠️ **This table has no demand side, and you must say so.** At 100,000 users you are producing **26,250 validated hours a month** — roughly **$2.6m of inventory monthly** against a market for South African speech data that has never absorbed anything close to that. **The 1,000-user row is the only one we would underwrite.** Present the others as capacity, never as a plan.
>
> ⚠️ **And note the distinction the earlier draft blurred.** The daily cap bounds **contributor earnings** at R216/month. It does **not** bound cost per user, which is **~R308/month all-in** once validation payouts, MoMo fees and platform overhead are included. Both numbers are correct; they measure different things, and a judge who catches you conflating them has found a real error.

**Reference point:** a **100-hour targeted campaign costs about R152,000.** That is a line item, not a capital project — which is precisely why a bank or a government department could fund one.

---

## 3. THE FARMING PROBLEM — and the design that fixes it

**This is the single most important number in the model, and the original plan did not have it.**

A 15-second clip, including reading the card and thinking, takes roughly 45 seconds of wall time. So:

| Reward | Effective hourly rate | vs minimum wage (R30.23/hr) |
|---|---|---|
| R1.00/clip | R80/hr | **2.6×** |
| R2.00/clip | R160/hr | **5.3×** |
| R3.00/clip | R240/hr | **7.9×** |

> **Left uncapped, this is not a game. It is a farm — and an unaffordable one.** At 7.9× minimum wage, every sophisticated actor in the country optimises against you within a week, quality collapses, and the cost per hour becomes unbounded.

### The fix — and it is elegant, because it is also the game design
> **Cash is capped by the daily quest. Beyond the quest, you play for points, league position and the Archive.**

Three plays a day at R2 = **R6/day, R216/month including listening rewards — 58% of the SRD grant.** Meaningful money in South Africa. Not a wage. Not farmable.

This single rule does five jobs at once:
1. **Bounds contributor earnings** at R216/month — forecastable, and the whole reason the business is modelable. *(All-in cost per active user is ~R308/month once validation, fees and overhead are added. Do not conflate the two — §2.4.)*
2. **Bounds fraud upside** — a stolen account is worth R6/day. Not worth industrialising.
3. **Keeps it a game**, which is the Track 2 argument and the retention argument.
4. **Enforces the anti-crowding-out principle** structurally: past the cap, the only reason to keep playing is that you want to. That is the test of whether the game works, run continuously, on every user.
5. **Creates the honest scarcity** that makes the daily quest feel worth showing up for.

---

## 4. THE PRICE LIST

| Product | Price | The comparable that justifies it |
|---|---|---|
| **Licensed dataset** (validated hours) | **$100–150/hr** | Undercuts Defined.ai's ≈$175/hr blended rate; sits at the literature's conventional cost floor |
| **Model / ASR API** | **R0.25–0.35/min** of audio processed | izwe.ai's own published South African-language API rates — the only SA-specific published price point found |
| **Targeted campaign** ("200 hours of banking-domain Sesotho") | **~R152k per 100 validated hours** + margin | Computed from §2. Priced per validated minute, delivered against a coverage target |
| **Learner subscription** | ⚠️ **Not priced** | No comparable found for SA indigenous-language learning. Requires primary willingness-to-pay research. Do not put a number on a slide |
| **Proficiency credential** | ⚠️ **Not priced** | Plausible product, no anchor: the per-employee GBS incentive grant rate is not published |

**Say the unpriced ones are unpriced.** A judge who asks "where did R49 a month come from?" and hears "we made it up" has stopped listening. A judge who hears *"we couldn't find a defensible comparable, so we're not going to invent one"* has just scored you higher on rigour than the number would have earned.

---

## 5. THE FIVE BUYERS

### 1 · The BPO / Global Business Services sector — **the real one**
The only buyer with a hard, sourced, quantified pain.

- **~150,000 people employed**, **R53bn revenue** (2024), growing at roughly **400 jobs per week** toward a **500,000-jobs-by-2030** target
- **R808m+** disbursed in government GBS incentives in 2024/25 — public money already flowing into this sector
- And the pain, in a competitor's own words: **"up to 70% of South African call-centre conversations happen in languages other than English"** — while the QA and analytics tooling can only process English

That is a sector with money, growth, state subsidy, a stated problem, and a competitor (Botlhale AI) already raising capital to sell into it — which proves willingness to pay.

### 2 · Global technology platforms
Google, Meta, Microsoft, Amazon, OpenAI. Demonstrable gaps in isiZulu, isiXhosa and Sesotho support. Google is already funding WAXAL to close exactly this class of gap. **Highest willingness to pay per hour; least proven at your deal size** — every audio-specific licensing deal found had an undisclosed value.

### 3 · South African government
The **Use of Official Languages Act 12 of 2012** creates a *statutory* obligation for departments to have a language policy and language unit. Home Affairs alone handles an estimated 13,000+ calls a day. **Slow procurement, and no evidence any department currently buys a commercial speech-AI product for this** — so it is a real need with an unproven purchase path.

### 4 · Banks and insurers
Absa runs a ~5,000-seat contact centre and has stated automation ambitions. The gap is language coverage, not automation tooling. Ranked fourth because the language-specific need is inferred from a multilingual customer base rather than directly evidenced.

### 5 · African-language AI companies — as customers, not competitors
izwe.ai, Botlhale, Lelapa, Intron Health all monetise African-language speech technology and all need data. **AMAZWI is more plausibly their supplier than their competitor.** Positioning it that way is both commercially smarter and politically smarter in a South African room.

---

## 6. HOW MTN MAKES MONEY — ranked

> ⚠️ **A deliberate disagreement with the research.** `G_BUSINESS.md` ranks Ayoba-style advertising as the most credible line because MTN has run that playbook before. **I rank it fourth.** Ayoba *had* 35 million monthly active users and brand campaigns — and was shut down in March 2026 anyway. Advertising revenue at MTN Group scale is a rounding error, and it did not save the last product that tried it. Leading with it in the pitch invites exactly the wrong comparison.

### 1 · MoMo South Africa activation — **the strongest, and it needs no AMAZWI revenue at all**
MoMo SA is on its **third launch attempt**. It reports ~13 million *registered* users and does not report active ones; in the 2020 relaunch, roughly **8% of registered users were active**. The problem is not sign-ups. It is a daily reason to open the wallet.

AMAZWI delivers small, frequent, *inbound* credits to a wallet, every day, tied to a habit. That is the textbook activation mechanic, and it accrues entirely to MTN's own P&L. **This is the line to lead with, because it is a problem the people in the room actually own.**

### 2 · Licensed data and model access
Sold to §5's buyers at §4's prices. Real comparables, real margins (27–58%), no telco anywhere has done it — which is both the opportunity and the reason to be honest that it is unproven.

### 3 · Internal cost avoidance
MTN's own contact centre, in a country where English is the fifth home language at 8.7%, and where **Botlhale AI put it at up to 70%** of call-centre conversations not being in English. ⚠️ **Attribute that figure every time you use it** — it is a vendor's claim, not an independent statistic, and naming the source makes it stronger. `07_TRUTH.md` §2.1. **MTN is its own first customer.** ⚠️ MTN's actual customer-care spend is not published, so do not quote a deflection saving — make the argument qualitatively and let them do the arithmetic.

### 4 · Sponsored campaigns and brand placement
Real, and MTN has run it before. Not the headline, for the reasons above.

### 5 · Learner subscriptions
Genuine, unpriced, and honestly the most speculative. Present as upside, never as the model.

---

## 7. THE REWARD, CALIBRATED TO SOUTH AFRICA

| Reference | Amount |
|---|---|
| SRD grant | **R370/month** |
| National minimum wage | **R30.23/hour** |
| 1GB data | **~R85** |
| Loaf of bread | **~R19.61** |

**Recommended: R2.00 per validated clip, three-play daily quest.**

- **R6/day speaking + up to R5/day listening. R216/month** at the balanced rate — 58% of the SRD grant. Hard ceiling R11/day.
- **Three days of playing buys a loaf of bread** (R6/day, bread ≈ R19.61). ⚠️ **Not "three clips"** — that is wrong by a factor of 3.3 and your own research file says so.
- A month of playing is **more than two gigabytes of data** — which matters, because data cost is the thing standing between the contributor and the product

**And the rule that protects everyone:** rates are published before the task and **never reduced retroactively.** Retroactive rate cuts are the characteristic betrayal of this industry, and refusing to do them is a policy you can state out loud.

---

## 8. THE NUMBERS THAT ARE NOT VERIFIED

Say these are estimates. Every one of them.

- **The whole unit-economics model is a plausibility model, not a forecast.** The two assumptions that move it most are the **70% acceptance rate** (no South African benchmark exists) and the **2% MoMo fee** (a disclosed *consumer* rate that may not apply to bulk B2C disbursement).
- ⚠️ **The biggest single financial unknown: MTN MoMo's actual bulk disbursement fee.** This one number determines whether R2 micro-rewards are economical at all. **It is not publishable from open search — ask the MoMo team on day one.** It is question one in `05_BUILD.md`.
- **MTN's customer-care spend** — no published figure. Do not quote a deflection saving.
- **MTN South Africa's absolute revenue** — not isolated from Group in accessible sources.
- **SASSA and SARS call volumes** — no published figures.
- **The GBS per-employee incentive grant rate** — not published, which is why the certification product cannot be priced.
- **A $345/hour Hausa speech-data figure** circulating in AI-search summaries could not be traced to a primary source. **Do not cite it.**
