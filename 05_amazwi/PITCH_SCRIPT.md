# AMAZWI - Round 1 Pitch Script (six-beat structure, target ~2:15-2:30 at real speaking pace)

Deck: https://gamma.app/docs/35l5lmuw841k199
This is the final regeneration with every fix from both Codex review rounds baked directly into the generated card text (no manual paste needed). Stale links, do not present any of them: `i1kl0ftsc184hbx`, `1dhqhqj19mgd758`, `p6yb4zccmjy3sbi`, `ws921eo2ozpw8bp`.

**Gamma credits are now at 0.** This deck cannot be regenerated again from this environment. Any further changes need a manual pass in the Gamma editor.
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

**Deck edit needed, still outstanding:** the live deck (`1dhqhqj19mgd758`) still has em dashes throughout its generated card text, and several cards need the wording fixes below applied by hand in the Gamma editor. This tool cannot patch cards in an existing Gamma, and regenerating from scratch isn't reliable right now (Gamma credits are nearly exhausted).

**Scope calibration, do not undo:** the live MoMo Collections call funds a **mission**; it does not disburse to a speaker's own wallet. Speaker payout is a separate, not-yet-built settlement step. Say "the AMAZWI ledger is credited," never "your MoMo wallet is credited." Also never say: "cash-out is live," "money crossed MoMo twice," "k-anonymised" (not in this build), or "the dataset nobody else has built."

---

## 1 - Problem: market gap (0:18) - SBU

**Card 2 text, paste this into the Gamma editor, replacing the current card 2:**

> **African languages are structurally missing from speech AI. This is a data gap, not a demand gap.**
>
> Foundation ASR models exceed 100% word-error-rate zero-shot on Southern Bantu languages. For a real person, that means South African languages are effectively unusable with today's voice AI.
>
> MTN already has the daily-use surface this data needs to come from: MoMo. A funded, verified mini-app mission gives MTN a governed, consented source of local-language voice-intent data tailored to MoMo use cases.

**Spoken (0:18):**

> "Foundation speech models exceed 100% word-error-rate on South Africa's Bantu languages, zero-shot. In practice, that means these languages don't work with today's voice AI. MTN already owns the daily-use surface this data needs to come from: MoMo."

**If a judge asks "which model, which dataset, which languages" - the backup answer:** "Whisper large-v3-turbo, zero-shot, scores 146.30% WER across the tested Southern Bantu set and 223% on Setswana, in a named published benchmark (arXiv 2606.31642). Separately, foundation ASR models broadly exceed 100% WER zero-shot across all six Southern Bantu languages per Marivate et al. (arXiv). These are specific, named benchmarks, not a claim that every ASR system fails this way." Do not put this level of detail on the slide; have it ready verbatim for Q&A only.

---

## 2 - Product explanation (0:22) - SBU

> "One person speaks. Two approved peers independently verify the meaning. Agreement credits the AMAZWI ledger once; disagreement pays nothing and records why."

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

> "We've proven a sandbox MoMo Collections funding request for the campaign: OAuth token, requesttopay accepted, status confirmed. The speaker cash-out leg is deliberately labelled not built.
>
> The pilot will measure whether funded missions increase repeat MoMo engagement, while producing useful, consented voice-intent labels. That's the commercial question, and it's the one we're asking MTN to help us answer."

**If a judge asks "how does MTN make money" - the exact answer:** "We are not claiming revenue before measuring it. The pilot tests whether funded mini-app missions increase repeat MoMo use and produce useful, consented voice-intent data, at a cost MTN can support." Never answer this question with a margin, savings percentage, or revenue projection.

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

## Deck status: regenerated and verified (3 Sep)

The deck was fully regenerated with every fix from both Codex review rounds baked directly into the generated card text (no manual paste needed this time). I then read the actual generated content back via the Gamma API and checked it card by card against the checklist below, rather than assuming the generation instructions were honoured. All items pass:

1. **Cover slide:** logo band reads as an empty placeholder ("LOGO ZONE: Paste the official MTN and MTN MoMo logos in this band before presenting"), no fabricated logo. Still needs real logo files pasted in before presenting.
2. **Card 2 wording:** confirmed present verbatim, "gives MTN a governed, consented source... tailored to MoMo use cases," not the earlier "MTN doesn't have today" phrasing.
3. **Em dashes:** confirmed none anywhere in the generated card text.
4. **MoMo evidence card:** confirmed labelled "SANDBOX ONLY" with an explicit warning callout, "No speaker was paid. Speaker cash-out is a separate, not-yet-built settlement leg," directly on the card, not only in the spoken line.
5. **Banned-phrase sweep:** confirmed none of the banned phrases appear anywhere in the generated text.
6. **Pilot-outcomes card:** confirmed present as its own card with all six items (repeat MoMo opens, funded mission participation, cost per eligible contribution, verifier liquidity, settlement feasibility, usefulness of intent-labelled speech) visible, plus the "none of these numbers exist yet" line.

**Gamma credits are now at 0** after this regeneration. If anything needs to change from here, it has to be a manual edit in the Gamma editor, not another regeneration from this environment.

---

## Final go/no-go - confirm all seven before presenting

1. The team uses `https://gamma.app/docs/35l5lmuw841k199`, not any of the four stale links listed at the top of this file.
2. Card 2 uses the corrected market-gap wording. Confirmed present in the current deck.
3. The MoMo card says "Sandbox Collections funding request" with a SANDBOX ONLY label. Confirmed present.
4. Pilot metrics are visible on a slide, not only spoken. Confirmed present.
5. No banned claims remain anywhere in the deck. Confirmed via full-text read-back.
6. Lethabo rehearses the agreement and refusal paths as one continuous demo, not two separate pieces. **Not yet done, human rehearsal only.**
7. Both teammates say "AMAZWI ledger credit," never "MoMo wallet payout," in every beat and in Q&A. **Not yet done, human rehearsal only.**

---

## Deck history
Four earlier decks are superseded, do not present any of them:
- `.../docs/p6yb4zccmjy3sbi`: pre-calibration, overclaimed "wallet credited."
- `.../docs/ws921eo2ozpw8bp`: original 10-card rubric-mapped version, pre-timing-freeze.
- `.../docs/i1kl0ftsc184hbx`: six-beat version, calibration correct but missing the Proven/Pilot/Not Built slide, the disagreement-path demo, and unscoped pilot-outcome metrics.
- `.../docs/1dhqhqj19mgd758`: correct structure and calibration, but had the pre-second-review card 2 wording, em dashes, and no SANDBOX ONLY label.
Current deck (`35l5lmuw841k199`) supersedes all four and has been read back and verified against the checklist above. Only the real MTN/MoMo logos and human rehearsal (go/no-go items 6 and 7) remain.
