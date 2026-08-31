# AMAZWI — EXPANSION IDEAS, ASSESSED
### Sign language · avatars · computer vision · what I'd add · tooling and workflow

**Parent:** `00_MASTER_PLAN.md` · **Written:** 2026-08-31

> **Integration status — Sbu review, 2026-08-31:** this is a roadmap and creative-exploration document, not competition scope. The canonical P0 is defined by `00_MASTER_PLAN.md` and `05_BUILD.md`. New factual, competitive, legal or model claims in this document must be verified and entered into `07_TRUTH.md` before they are used in a pitch. See `../../HANDOVER_LETHABO.md` for the integration critique.

> Every idea below gets a straight verdict: **top tier**, **top tier with a rewrite**, or **cut**. One of yours I think actively damages the pitch, and I say which and why.

---

## 1. SASL AS A LANGUAGE — 🟢 TOP TIER IDEA, WRONG TIMING, AND THERE IS A BETTER VERSION

### Why it is genuinely strong
- **SASL is the 12th official language** — Constitution Eighteenth Amendment Act, signed 19 July 2023. Including it is *constitutionally* grounded, not a diversity gesture.
- **The mechanic transfers exactly.** A signer records a video clue; two signing viewers guess; agreement validates. Output agreement does not care whether the signal is audio or video.
- **Sign language data is scarcer than speech data.** There is essentially no SASL corpus for machine learning. Our whole scarcity argument gets *stronger*, not weaker.
- **It inverts the usual accessibility posture.** Deaf South Africans are systematically excluded from voice-first products. This makes them **earners**, not beneficiaries. That is a categorically different — and much better — relationship.
- No competitor anywhere is doing this.

### Why it cannot be in this build — four hard problems
1. **Video is 50–100× the payload of audio.** A 15-second clip is ~1–2 MB against our 200 KB design thesis. **And the bandwidth cost falls on the contributor**, who is likely low-income. Paying R2 for a clip that costs R3 of data to upload is worse than not paying at all — it directly contradicts our own ethical argument.
2. **You cannot quality-gate video on-device** the way you can audio. RMS and clipping are cheap; framing, lighting and hand visibility are not.
3. 🔴 **We have no Deaf collaborator.** Building a SASL product without Deaf leadership is precisely the *"nothing about us without us"* violation our own ethics research flagged. This is the blocking objection, not the bandwidth.
4. Not buildable in 26 hours alongside everything else.

### 🟢 The better version — and it IS buildable
> **Put SASL on the LEARNER side first, not the contributor side.**

A learner watches a signed clue and guesses. That needs a small seeded set of SASL clips (sourced with permission from an existing Deaf organisation), **no contributor upload at all**, so:
- The bandwidth problem disappears — a handful of clips cached once, not thousands uploaded
- The quality problem disappears — the seed set is curated
- **Deaf people can play from day one**, which is real accessibility rather than promised accessibility
- It proves the mechanic is modality-agnostic, which is the scaling argument

Then the contribution side arrives later, with Deaf partnership, a bandwidth plan and a zero-rating conversation with MTN.

**And it reframes the scale answer, which is the best strategic consequence:**
> *"How does this scale? Not more countries first — more modalities. The same agreement mechanic works for signed language, and signed language has even less data than spoken."*

---

## 2. AVATAR FROM YOUR FACE (computer vision) — 🔴 CUT IT

**This is the one idea in the set that actively damages the pitch, and I'd argue hard against it.**

- **Face capture is biometric data.** Under POPIA, biometric information is **special personal information** with a materially higher compliance burden. Our entire security architecture is built on *avoiding* biometrics — *"voice is the interface, never the lock"* — and that decision is currently one of the strongest things we say on stage.
- **It reverses that in one feature**, and hands a judge a devastating question: *"You told us you deliberately avoid biometric processing for POPIA reasons. Then you built a face scanner. Which is it?"*
- **It costs 10–30 MB** of on-device model against a 200 KB budget.
- **And it does nothing for the user.** An avatar that looks like you is a novelty. It does not make the game better, does not improve data quality, does not earn anyone money. It is a feature in search of a reason.

Every argument that makes this product credible — minimal data collection, no biometrics, tiny payload, contributor-first economics — this feature contradicts. **Cut it.**

*(The good ideas sitting next to it survive. See §3 and §4.)*

---

## 3. LIP MOVEMENT FOR PRONUNCIATION — 🟢 TOP TIER, ONCE YOU SEPARATE IT FROM FACE CAPTURE

The instinct here is right and the implementation was pointed the wrong way. **You do not need to capture the learner's face. You need to *show* them an articulation.**

### And there is a version of this that is genuinely world-class
> ### The click-consonant trainer

- **Clicks — ǀ ǁ ǂ ǃ — are the single most identifiable feature of Nguni languages and the single hardest thing for a non-speaker to produce.** Every South African language-learning attempt dies on them.
- They are **visually distinctive**: the tongue position for a dental click versus a lateral click is a *visible* difference, which is exactly the case where showing beats telling.
- **Nobody has built one.** Not Duolingo — which dropped isiXhosa in 2023 for low engagement, and clicks are a plausible reason why.
- It is cheap: a small set of recorded or illustrated articulations, not a live CV pipeline.
- And it is the perfect learner hook: *"in ninety seconds you'll produce a click that isn't in your language."*

**Why this is top tier:** it takes the hardest, most distinctive, most-failed part of learning a South African language and makes it the *first* thing you succeed at. That is a product wedge, not a feature.

---

## 4. VOICE CLONING FOR LEARNING — 🔴 REFUSE THIS ONE, AND SAY WHY

I would not build this, and I think it is important to be direct about why rather than quietly dropping it.

1. **Our own research says voice cloning bypasses speaker verification 82.7% of the time** on 10–30 minutes of audio. Building a voice cloner *inside* a product that collects voice from low-income people writes its own headline: *"App pays poor South Africans for their voices, then clones them."*
2. **It is outside what contributors would reasonably anticipate**, which undermines the consent model that is our strongest ethical asset.
3. 🔴 **It may be contractually barred.** African Next Voices' South African subset **explicitly prohibits TTS, voice cloning and voice synthesis uses** of the data. If we seed from Swivuriso — and the plan does — we could be building a use the licence forbids. *Check this before anyone writes a line of it.*

### 🟢 The safe version delivers the same learning benefit
> **"Hear yourself against a speaker."** Record your attempt, play it back against the native clip, show both waveforms and a similarity score.

No cloning, no synthesis, no licence problem — and pedagogically it is *better*, because self-comparison is how pronunciation is actually taught.

---

## 5. THREE MORE I'D ADD

### 🟢 "Ask the Archive" — the answer to "is this extractive?"
Once you have validated speech, let people **query** it. *"How do people in Giyani actually say 'I'm on my way'?"*

**Why it is top tier:** it converts the corpus from something taken *from* the community into something usable *by* the community. Every data-collection project in Africa fails this test. It is the single strongest answer to the extraction objection, it costs almost nothing once the data exists, and it makes the Archive a destination rather than a trophy case.

### 🟢 The dialect map — a research asset nobody has
You have coarse location plus validated speech. That yields **the first live map of how South African languages are actually spoken by region** — not what the dictionary says, what Soweto says versus what Mahikeng says.

**Why it is top tier:** it is a genuinely new artefact, it is beautiful on screen, and it is a second sellable product from data you already collected. Linguistics departments would want it on day one.

### 🟡 Proficiency certification — already in the plan, under-exploited
The latent-trait model already produces a proficiency estimate. **The BPO sector hires on exactly this and has no objective instrument** for African languages — 150,000 people employed, ~400 jobs a week, and a competitor's own claim that up to 70% of call-centre conversations are not in English.

**Why only amber:** it needs external validation before it can be called a certification, and that is months of work. But it is plausibly a bigger business than the data itself, and it deserves a line on the roadmap slide rather than a footnote.

---

## 6. THE VERDICT TABLE

| Idea | Verdict | Where it goes |
|---|---|---|
| **SASL on the learner side** | 🟢 Top tier, buildable later | Roadmap, with the modality-scaling line |
| **SASL contribution** | 🟢 Top tier, needs Deaf partnership + bandwidth plan | Roadmap, honestly caveated |
| **Click-consonant trainer** | 🟢 Top tier — the strongest new idea here | Roadmap, and arguably the v2 wedge |
| **Ask the Archive** | 🟢 Top tier — best answer to extraction | Roadmap, mention on stage |
| **Dialect map** | 🟢 Top tier — second product from the same data | Roadmap |
| **Hear yourself vs a speaker** | 🟢 Good, safe, cheap | Post-MVP |
| **Proficiency certification** | 🟡 Real, needs validation | Business slide |
| **Voice cloning** | 🔴 Refuse — reputational and possibly contractual | Nowhere |
| **Face-capture avatar** | 🔴 Cut — contradicts the POPIA position | Nowhere |

> **The line that ties the greens together on stage:**
> *"The mechanic doesn't care what the signal is. Speech today, signed language next, and the same agreement between two strangers validates both. That's why this scales into modalities before it scales into countries."*

---

## 7. TOOLING — what I found

### The repos you named

**`claudex-loop`** *(github.com/chaseai-yt/claudex-loop)* — 🟢 **directly relevant.** A Claude Code skill: four-stage plan reinforcement — reconnaissance, inquiry, adversarial review, cross-model construction and verification — where two models reinforce a plan then **switch roles** to build it. **That is almost exactly the workflow you just described**, formalised. Worth reading before Wednesday.
Adjacent: `promptadvisers/claudex` (autonomous Claude+Codex review loop via a Stop hook — reportedly the only mechanism that can force an autonomous loop in Claude Code), `hamelsmu/claude-review-loop` (plugin: automated review loop with Codex), `axeldelafosse/loop` (Bun CLI running both in tmux).

**`OmniRoute`** *(github.com/diegosouzapw/OmniRoute)* — ⚠️ **I would not use this, and here is the honest reason.** It is a local gateway fronting 350 providers, and it works by pointing `ANTHROPIC_BASE_URL` at a proxy. There is published criticism specifically about **security risks and CVEs** — I could not read the full article (403) so I am not asserting the specific claims, **but the shape of the risk is structural and does not need a CVE to matter**: routing Claude Code through a third-party endpoint means your prompts, your code and your unpublished product strategy transit software you do not control. Two days before a competition with an IP clause, against a repo you have not audited, that is not a trade I would make for cheaper tokens.

**`Archy`** *(github.com/hslee16/Archy)* — an architectural sensor for **Python** codebases that makes assertions which **break the build** when structure drifts. 🟡 Genuinely good idea, wrong moment: it is for defending an architecture over months, and we have 26 hours. **Note it for after.**
Better fits for us if you want one: **`BitRaptors/Archie`** (generates `AGENTS.md`, per-folder `CLAUDE.md` and hooks from your codebase — that *is* useful now, because it makes the rules in these docs machine-enforced), and **`Hainrixz/the-architect`** (interviews you, writes a blueprint another instance builds from).

### Design skills worth adding
- **`design-style-picker`** — turns vague taste into concrete visual directions by batch-generating a structured set. Directly the thing we did by hand with the four themes.
- **`nextlevelbuilder/ui-ux-pro-max-skill`**
- Registries: **claude-plugins.dev**, **open-design.ai/plugins** (469+ design plugins), `JanSzewczyk/claude-plugins` (design systems & styling), `daymade/claude-code-skills`

⚠️ **Audit before installing.** A skill is instructions that execute in your session; a plugin can carry hooks. Two days out, install nothing you have not read.

### Figma — connected, and better than expected
Twelve skills are live. The three that matter:
- **`figma-generate-library`** — builds a **production-grade design system**: variables/tokens, components with variant sets, light/dark theming, foundations. This is how `04_DESIGN.md` §2.2 becomes a real library rather than a CSS file.
- **`figma-generate-design`** — pushes screens into Figma from code, using design-system tokens rather than hardcoded values.
- **`figma-generate-diagram`** — Mermaid → FigJam. **The architecture diagram for the deck comes from here**, not from hand-drawing it at 3am.

**Recommended sequence:** tokens → `figma-generate-library` → screens via `figma-generate-design` → architecture into FigJam → export for the deck.

---

## 8. MODEL WORKFLOW — agreed, and here is the switching rule

| Work | Model | Why |
|---|---|---|
| Research, critique, red-teaming, planning, architecture, **design and UI direction**, business reasoning, ethics and legal calls | **Opus** | Judgement work where being wrong is expensive and the error is not visible until later |
| Implementation against a settled spec, iteration, refactors, tests, wiring, content entry, debugging a known failure | **Sonnet** | Verifiable work — the spec says what right looks like, so a cheaper model with a clear target is the correct tool |

**I'll say "switch to Sonnet" explicitly** when we cross from deciding into building, and **"switch back to Opus"** when something needs judgement again.

**The three triggers to come back to Opus mid-build:**
1. A spec turns out to be wrong or ambiguous — that is a decision, not a bug
2. A design or UI direction is genuinely open
3. Something is about to be *claimed* — a number, a benchmark, a slide

**Right now:** we are planning and designing. **Stay on Opus.**
**The switch point:** the moment the theme is picked and the card content is written. Everything after that — scaffolding, screens, endpoints, the ledger, wiring — is Sonnet work against a spec that already exists.

---

# ADDENDUM — 31 Aug 14:25 · Lethabo's counter, and where I was wrong

> **All of this is roadmap, not competition scope.** P0 is unchanged: one audio loop, isiZulu and Setswana. Nothing below enters the 26-hour build.

Lethabo pushed back on two of my three verdicts. **On two of them he is right and I was too absolute.** On the third I am holding — and there is a better version of what he wants anyway.

---

## 1. FACE CAPTURE — I overstated it. Viable with separate consent. 🟡

**Where I was wrong:** I treated POPIA as a prohibition. It is not. **Special personal information may be processed with the data subject's consent** — that is the mechanism the Act provides. Consent genuinely does unlock it.

**And the data-value argument is correct.** Face and video data *is* worth more than audio, so under coverage pricing it should *pay* more. That is not a special case; it is the pricing rule extended to modality.

**What survives from my objection — narrower than I made it:**
- Not the legality. **The consent architecture.** A **separate, explicit, independently declinable opt-in** on its own surface — never bundled into the voice consent, never a toggle someone flips past. Bundling biometric consent with ordinary consent is what turns a lawful basis into a scandal.
- **The pitch line changes.** *"We avoid biometrics"* becomes **"we never use biometrics for authentication"** — still true, still strong, still the reason the architecture is sound. Voice is the interface, never the lock; that sentence survives intact.
- Payload is real but solvable: this lives in a separate opt-in surface, not the 200 KB core.

**Verdict: roadmap, viable, hard consent boundary.** Not a cut.

---

## 2. VOICE CLONING — the objection was real but aimed at the wrong thing. 🟡

**Consent fixes the ethics. It does not fix the licence** — two different problems that I ran together.

| Data | Cloning / synthesis |
|---|---|
| **Our own contributors, under explicit synthesis consent** | 🟡 **Defensible.** Their data, their consent, their choice |
| **Anything derived from Swivuriso / African Next Voices** | 🔴 **Potentially barred.** The SA subset explicitly prohibits TTS, cloning and synthesis. **Our users cannot consent away a third party's licence** |

**So the rule is a data-provenance boundary, not a ban:** any synthesis capability trains only on data collected under a synthesis consent, with Swivuriso-seeded lineage kept separate and excluded. The pipeline already supports this — consent lineage per row, `02_TECH.md` §6 Stage 6.

**Still true:** the reputational asymmetry is real. *"Pays low-income people for their voices, then clones them"* is a headline whatever the consent says. Ship **"hear yourself against a speaker"** first — same learning benefit, none of the exposure — and treat cloning as a later, separately-consented capability.

**Verdict: roadmap, with a provenance firewall.** Not a refusal.

---

## 3. SPIN-TO-WIN — holding here, because this version is *worse*, not better

The proposal: wager earned credits on a spin for a bonus or discount before cashing out.

**That is more exposed than a free promotional spin, not less.** The three elements regulators look for are **consideration, chance and prize.** A free spin has two. **Wagering credits that carry monetary value supplies the third.** The credits are precisely the thing that completes the set.

And it lands in a product that pays low-income people — the worst possible place for a mechanic that looks like gambling.

### But the idea underneath is good, and there is a version I would build first 🟢

**Fixed-rate redemption. No chance anywhere.**

> Earn credits → spend them at a **published, fixed rate** on airtime, data or a discount → or cash out to MoMo at a threshold.

No chance, no wager, no s36 exposure — an ordinary loyalty programme. **And it beats the spin commercially on every axis:**

| | Why it wins |
|---|---|
| **Cheaper for MTN than cash** | Airtime and data cost MTN marginal cost, not face value. Cash costs the full amount **plus the bulk B2C fee we still cannot get a number for** |
| **It shrinks our worst open question** | If most value is redeemed in-ecosystem, *"are R2 disbursements economical"* applies only to the minority who cash out |
| **Airtime is near-cash in South Africa** | Not a lesser reward here — a parallel currency |
| **Keeps value inside MoMo** | Which is the entire strategic argument we make to MTN |
| **Redemption beats a gamble on retention** | A guaranteed visible rate is a reason to return. A spin is a reason to feel cheated four times in five |

**A better exchange rate for redeeming rather than cashing out is a discount, not a lottery** — and it drives exactly the behaviour MTN wants.

**Verdict: no spin. Fixed-rate redemption instead — and it is the better product.**

---

## 4. THE LEARN / ACTIVITIES SECTION — yes, and it fixes a real gap 🟢

Right now the two-sided product is *implied* by the plan and *invisible* in the app.

A distinct **Learn** surface — click trainer, hear-yourself, guided modes, vocabulary — does three things at once:
1. Makes the learner population **visible** rather than theoretical, which is the Track 2 argument
2. Gives redeemed credits somewhere to go that is not cash
3. Separates *play to earn* from *play to learn* in the navigation, so neither has to pretend to be the other

**Verdict: roadmap, high value, and it should shape the IA even before it is built.**

---

## 5. THE PRINCIPLE UNDERNEATH ALL OF IT

The core argument — **richer data is worth more, so it should pay more** — is right, and it generalises:

```
reward = base × coverage_need × difficulty × MODALITY_VALUE
```

Audio → video → signed → multimodal, each tier priced by what it is actually worth, each behind its own consent gate. Same coverage-pricing logic already in `01_PRODUCT.md` §5, extended one axis.

**Better than a flat rate long-term.** And it relocates the ethical boundary: not *"don't collect richer data"* but **"price it honestly and consent for it separately."**
