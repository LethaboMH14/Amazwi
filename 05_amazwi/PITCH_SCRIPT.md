# AMAZWI - Round 1 Pitch Script (six-beat structure, target ~2:15-2:30 at real speaking pace)

Deck: https://gamma.app/docs/AMAZWI-sn28skr7k2plcyd?mode=doc
This is the current Gamma pitch supplied by the team. Align the spoken claims below to this deck before presenting. Stale links, do not present any of them: `35l5lmuw841k199`, `i1kl0ftsc184hbx`, `1dhqhqj19mgd758`, `p6yb4zccmjy3sbi`, `ws921eo2ozpw8bp`.

**Gamma credits are now at 0.** This deck cannot be regenerated again from this environment. Any further changes need a manual pass in the Gamma editor, **or use [`GAMMA_PROMPT_V2.md`](GAMMA_PROMPT_V2.md) on an account that still has credits**: a full, self-contained paste-ready prompt for a v2 deck that keeps everything below and adds a tech architecture diagram, an unemployment/skills-gap card, an illustrative cost breakdown, and a scaling card.
Rubric: Innovation & Creativity 25% · Relevance to Fintech 20% · Feasibility & Scalability 20% · Technical Execution 20% · Presentation & Pitch 15%

**Revised again against Codex's external review (provisional score 84/100, ceiling ~88-90 if these land and rehearsal is real).** Codex reviewed the repo, the handover notes and this file, but could not open the live Gamma pixels from its environment - the fixes below are applied to the script text and to the paste-ready card text; the actual Gamma cards still need the same manual pass described further down.

**What changed this pass:**
1. Cut ~70 words from the opening and closing. Word counts were measured at normal speaking pace (roughly 2.2 words/second), not guessed.
2. Fixed a real contradiction: the old closing line "MoMo is how it gets paid" implied a live payout that doesn't exist yet. Replaced.
3. Beat 4 (MoMo evidence) rewritten to answer "why should MTN care", not just report status codes.
4. Opening cut from seven statistics to two, plus one MTN-facing implication. Dropped the Ayoba reference (risk: can read as criticizing MTN); replaced with framing the MoMo mini-app opportunity directly.
5. Product-explanation sentence de-jargoned; technical detail now follows, not leads.
6. The claim "the receipt explains why, in the speaker's own language" was checked against `starter/backend/app/resolver.py` (lines 193-218): the resolver's reason strings are hardcoded English (e.g. `"understood by both verifiers, audio quality passed, consent active"`). There is no localization. The claim was false and is now removed from the script.
7. Closing restructured around the commercial ask MTN actually needs to hear: what to measure, not just what was built.
8. **Latest:** the Mupita quote was traced to its exact source (byline, date, URL) and split from a verbatim quote vs. a journalist's paraphrase, recorded in `07_TRUTH.md`; the problem statement was refined against Google Research's own WAXAL challenge description (supplied by the user) to lead with WAXAL's real scale rather than wait for a judge to raise it; and the "how does this benefit MTN" answer was expanded into a full NLP / AI data centres / AI race argument for why MTN specifically should invest, still without a revenue number.

**Feature work stays frozen.** Fixed shape, six beats:

| # | Beat | Time | Speaker |
|---|------|------|---------|
| 1 | Problem: market gap (BLUF) | 0:18 | Sbu |
| 2 | Product explanation | 0:22 | Sbu |
| 3 | Live demo: agreement path | 0:40 | Lethabo |
| 3b | Disagreement path (quick cut) | 0:12 | Lethabo |
| 4 | MoMo evidence + commercial "why" | 0:25 | Sbu |
| 5 | Proven/Pilot/Not built + pilot ask | 0:30 | Sbu |

Target total ≈ 2:15-2:30 at real pace, leaving headroom inside a 2:30-3:00 slot for handoff, clicks, and judge reaction. If time is tight, cut adjectives from beat 5 first; never cut the MoMo evidence line, the Proven/Pilot/Not Built structure, or the final ask.

**Deck status:** the current deck is `AMAZWI-sn28skr7k2plcyd?mode=doc`. Treat it as canonical and confirm its visible wording against this script before presenting. The previous generated deck and its verification record are historical; do not assume those checks automatically apply to this updated Gamma pitch.

**Scope calibration, do not undo:** the live MoMo Collections call funds a **mission**; it does not disburse to a speaker's own wallet. Speaker payout is a separate, not-yet-built settlement step. Say "the AMAZWI ledger is credited," never "your MoMo wallet is credited." Also never say: "cash-out is live," "money crossed MoMo twice," "k-anonymised" (not in this build), or "the dataset nobody else has built."

---

## 1 - Problem: market gap (0:18) - SBU

**Refined against Google Research's own WAXAL challenge description (Zindi/Kaggle brief for the ASR challenge targeting Lingala, Shona and Luganda), which the user supplied directly.** WAXAL is real, large, and a genuine multi-year Google Research collaboration: 27 African languages, 100 million+ speakers, thousands of hours of natural speech. That is the strongest possible version of "Google is investing here" a judge could bring up, so lead with it rather than waiting for it to be raised. The point AMAZWI makes is sharper for including it: even WAXAL's named target languages for this exact challenge, Lingala (DRC/Congo), Shona (Zimbabwe), Luganda (Uganda), are not South African languages. Google's own flagship African-speech effort, by its own current challenge brief, still does not reach isiZulu, Setswana, isiXhosa or Sesotho. This is Google's own framing being used to make the gap undeniable, not an accusation.

**Card 2 text, paste this into the Gamma editor, replacing the current card 2:**

> **African languages are structurally missing from speech AI. This is a data gap, not a demand gap.**
>
> Google Research's WAXAL programme is real and substantial: 27 African languages, over 100 million speakers, thousands of hours of natural speech, built with African academic and community partners. It is exactly the kind of investment this problem needs.
>
> Its current challenge targets Lingala, Shona and Luganda. None of South Africa's official languages are among them. Foundation ASR models separately exceed 100% word-error-rate zero-shot on Southern Bantu languages: for a real person, that means these languages are effectively unusable with today's voice AI.
>
> MTN already has the daily-use surface this data needs to come from: MoMo. A funded, verified mini-app mission gives MTN a governed, consented source of local-language voice-intent data tailored to MoMo use cases.

**Spoken (0:18):**

> "Google's own WAXAL programme is real: 27 African languages, thousands of hours, a genuine investment. Its current challenge targets Lingala, Shona and Luganda. Not one South African language is among them. MTN already owns the daily-use surface that data needs to come from: MoMo."

**If a judge asks "which model, which dataset, which languages" - the backup answer:** "Whisper large-v3-turbo, zero-shot, scores 146.30% WER across the tested Southern Bantu set and 223% on Setswana, in a named published benchmark (arXiv 2606.31642). Separately, foundation ASR models broadly exceed 100% WER zero-shot across all six Southern Bantu languages per Marivate et al. (arXiv). These are specific, named benchmarks, not a claim that every ASR system fails this way." Do not put this level of detail on the slide; have it ready verbatim for Q&A only.

**If a judge asks "isn't WAXAL solving this already" - the exact answer:** "WAXAL is a real, substantial contribution, and we'd rather build alongside it than pretend it doesn't exist. But its own current challenge brief names Lingala, Shona and Luganda, not a single South African language. That's not a criticism of Google, it's the specific gap this pilot fills." Never say "Google skipped us" or any accusatory framing; the gap speaks for itself from Google's own materials.

---

## 2 - Product explanation (0:22) - SBU

> "One person speaks. Two approved peers independently verify the meaning. Agreement credits the AMAZWI ledger once; disagreement pays nothing and records why. Inside MoMo, that gives the mission a funding rail and the reward a transparent record, without pretending production cash-out is live."

*(→ hand to Lethabo)*

---

## 3 - Live demo, agreement path (0:40) - LETHABO

*(Drive the phone, narrate live. Fill in the actual phrase before rehearsal.)*

> "Watch the flow. I record a phrase, [isiZulu/Setswana phrase].
>
> A peer verifier, a real person on a separate device, confirms it matches.
>
> They agree: the AMAZWI ledger is credited once, right now. [show receipt]"

## 3b - Disagreement path (0:12) - LETHABO

> "Now the other outcome, pre-captured for time. Two verifiers disagree. The resolver pays nothing, and the receipt records why. Refusal is a first-class result here, not a hidden failure."

**Backup if the live demo fails:** fall back to the receipt evidence already in the deck for both paths, say plainly that you're doing so, and move straight to beat 4. Don't stall trying to fix it live.

---

## 4 - MoMo evidence + commercial "why" (0:25) - SBU

> "We've proven a sandbox MoMo Collections funding request for a fixed campaign: OAuth token, requesttopay accepted, status confirmed. No speaker was paid; cash-out is deliberately labelled not built.
>
> The business test is whether sponsor-funded missions create repeat MoMo engagement and useful, consented voice-intent labels at a cost MTN can support. That's the question we're asking MTN to measure with us."

**If a judge asks "how does MTN make money" - the exact answer:** "We are not claiming revenue before measuring it. The pilot tests whether funded mini-app missions increase repeat MoMo use and produce useful, consented voice-intent data, at a cost MTN can support." Never answer this question with a margin, savings percentage, or revenue projection.

**If a judge asks "what specifically does better African-language data let MTN do, and how could this make MTN money if they invest" - the full backup answer, expanded to cover NLP, AI/data science, AI data centres and the AI race directly. This is Q&A-depth material, not a slide; deliver the first paragraph if time is short, add the rest only if pressed:**

> "Three layers, all pointing at the same potential asset.
>
> **NLP and AI products.** Voice-operable MoMo could support South African-language intents such as balance checks, sending money, and agent or merchant transactions by voice. Governed, consented speech data would be a necessary input to those products. MTN's own Group President, Ralph Mupita, told TechAfrica News in April 2026: 'I think the next frontier is how do we develop the digital services ourselves that we can have our customers consume.' AMAZWI is a small, testable way to explore that opportunity; we are not claiming MTN has no existing language data.
>
> **AI data centres.** MTN has disclosed a 150MW AI data centre investment, with South Africa and Nigeria named as priority markets, in its H1 2026 results. We are not claiming this prototype feeds that infrastructure today. The pilot tests whether governed South African speech data creates a useful local workload before MTN commits further capital.
>
> **The AI race.** African-language data is scarce, which is why initiatives such as WAXAL exist. A governed, consent-clean, provenance-traceable South African corpus could become a strategic asset that MTN might use internally, license, or use to negotiate from a stronger position. We are not putting a value on that asset today. This pilot tests whether the strategic logic holds before MTN commits further capital."

Never turn this into a specific revenue, margin, or savings figure. The argument is strategic and evidence-based (Mupita's own words, MTN's own disclosed data centre plan, the AI industry's well-known data scarcity problem), not a financial projection we haven't earned the right to make.

**Optional card-9 addition (manual paste, since Gamma credits are at 0):**

> A potential local-language use case for MTN's disclosed AI infrastructure investment: the 150MW AI data centre programme named in MTN's H1 2026 results, with South Africa and Nigeria as priority markets. The pilot must test usefulness before this is treated as an infrastructure input. As MTN's own Group President has said, "the next frontier is how do we develop the digital services ourselves that we can have our customers consume."

---

## 5 - Proven / Pilot / Not built, then the ask (0:30) - SBU

> "Proven today: consent, recording, two-peer verification, refusal handling, an idempotent ledger, and sandbox campaign funding. Not built yet: production cash-out and scale economics.
>
> Give us one MTN-supported language and one contained MoMo mission. We'll measure repeat opens, cost per eligible contribution, verifier liquidity, and settlement feasibility before claiming scale.
>
> Speak. Be understood. Earn."

---

## Notes for rehearsal
- These word counts were measured, not estimated, at ~2.2 words/second normal speaking pace including natural pauses. Time each beat separately against a stopwatch before combining them; if a beat runs long in rehearsal, cut from that beat specifically rather than assuming the total will average out.
- Beat 3+3b together should not exceed 52s combined; Lethabo rehearses this as one continuous unit.
- If judges interrupt with a question, answer in one sentence and return to the next beat.
- Say the word **"sandbox"** out loud on beat 4; never let it sound like a settled live payment.
- **Never say the MoMo call pays the speaker directly.** It funds the mission; speaker cash-out is Not Built.
- **Never claim the receipt/reason text is shown in the speaker's own language.** Checked against `resolver.py`: reason strings are hardcoded English. If localization ships before presenting, this line can be reinstated, but only then.
- Never state a margin, savings percentage, or cost-reduction number, anywhere, including Q&A. It isn't measured.
- Never say "the dataset nobody else has built," "only," "first," "cash-out is live," "money crossed MoMo twice," or "k-anonymised."
- The Proven/Pilot/Not Built structure is the deck's centrepiece. Don't rush past it, but it no longer needs a full separate slide's worth of spoken time given the tighter close above.
- Close on "Speak. Be understood. Earn." Let it land. Don't follow it with "thank you" or immediately field a question.

---

## Deck status: current Gamma pitch (visual confirmation required)

The team has supplied an updated Gamma pitch. Use the checklist below to verify the live deck manually before presenting; the new link has not been independently read back in this environment.

1. **Cover slide:** official MTN/MoMo logo placement is intentional, with no fabricated logo.
2. **Card 2 wording:** uses the corrected WAXAL and market-gap wording, without claiming MTN lacks existing language data.
3. **Em dashes:** none remain in generated card text.
4. **MoMo evidence card:** visibly says "SANDBOX ONLY", identifies a Collections funding request and states that no speaker was paid.
5. **Banned-phrase sweep:** no wallet-payout, live-cash-out, k-anonymity, unsupported-superlative or guaranteed-revenue claims appear anywhere.
6. **Pilot-outcomes card:** all six measures are visible: repeat MoMo opens, funded mission participation, cost per eligible contribution, verifier liquidity, settlement feasibility and usefulness of intent-labelled speech.

**Gamma credits are now at 0** after this regeneration. If anything needs to change from here, it has to be a manual edit in the Gamma editor, not another regeneration from this environment.

---

## Gap history: "how does better data help MTN" was under-answered, now fixed

The deck originally gestured at the dataset being "useful" or "tailored to MoMo use cases" without naming a mechanism. This was fixed in two stages: first with a two-point answer (voice-operable MoMo + the disclosed data centre investment), then expanded on Sbu's direct request into the full three-layer NLP / AI data centre / AI race answer now under beat 4 above, including the verbatim, directly-quotable Mupita line sourced and byline-checked in `07_TRUTH.md`. That expanded answer is the current version, deliver from there. The optional card-9 bullet is also now under beat 4, above.

---

## Final go/no-go - confirm all seven before presenting

1. The team uses `https://gamma.app/docs/AMAZWI-sn28skr7k2plcyd?mode=doc`, not any stale link listed at the top of this file.
2. Card 2 uses the corrected market-gap wording and avoids claiming MTN lacks existing language data.
3. The MoMo card says "Sandbox Collections funding request" with a SANDBOX ONLY label.
4. Pilot metrics are visible on a slide, not only spoken.
5. No banned claims remain anywhere in the deck.
6. Lethabo rehearses the agreement and refusal paths as one continuous demo, not two separate pieces. **Not yet done, human rehearsal only.**
7. Both teammates say "AMAZWI ledger credit," never "MoMo wallet payout," in every beat and in Q&A. **Not yet done, human rehearsal only.**

---

## Deck history
Four earlier decks are superseded, do not present any of them:
- `.../docs/p6yb4zccmjy3sbi`: pre-calibration, overclaimed "wallet credited."
- `.../docs/ws921eo2ozpw8bp`: original 10-card rubric-mapped version, pre-timing-freeze.
- `.../docs/i1kl0ftsc184hbx`: six-beat version, calibration correct but missing the Proven/Pilot/Not Built slide, the disagreement-path demo, and unscoped pilot-outcome metrics.
- `.../docs/1dhqhqj19mgd758`: correct structure and calibration, but had the pre-second-review card 2 wording, em dashes, and no SANDBOX ONLY label.
- `.../docs/35l5lmuw841k199`: previous regenerated deck, now superseded by the team's updated Gamma pitch.
Current deck (`AMAZWI-sn28skr7k2plcyd?mode=doc`) supersedes all five. Confirm the visible checklist and complete human rehearsal (go/no-go items 6 and 7) before presenting.
