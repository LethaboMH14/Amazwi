# AMAZWI - Round 1 Pitch Script (six-beat structure, target ~2:15-2:30 at real speaking pace)

Deck: https://gamma.app/docs/1dhqhqj19mgd758
The link `i1kl0ftsc184hbx` is stale and must not be presented; `1dhqhqj19mgd758` is current and correct. `p6yb4zccmjy3sbi` and `ws921eo2ozpw8bp` are also stale.
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

## Deck fixes still needed in the live Gamma (manual, not yet verified from this environment)

All six items below now have final, exact text or a precise check to perform. None of this can be applied programmatically (no per-card edit tool for a live Gamma, and Gamma credits are nearly exhausted) - each needs a human pass in the editor.

1. **Cover slide - verification only, no text change.** Open card 1 and confirm the logo band still reads as empty/placeholder ("[LOGO ZONE...]" or similar), not a fabricated MTN/MoMo logo. If real logo files are available, paste them into that band now; if not, leave the placeholder text exactly as-is - an honest empty band beats a fake logo every time.

2. **Card 2 - paste this exact text, replacing whatever is currently there:**

   > **African languages are structurally missing from speech AI. This is a data gap, not a demand gap.**
   >
   > Foundation ASR models exceed 100% word-error-rate zero-shot on Southern Bantu languages. For a real person, that means South African languages are effectively unusable with today's voice AI.
   >
   > MTN already has the daily-use surface this data needs to come from: MoMo. A funded, verified mini-app mission gives MTN a governed, consented source of local-language voice-intent data tailored to MoMo use cases.

3. ~~**Em dashes:** sweep every remaining card for "-" and replace with comma, period, or colon.~~ **Done (3 Sep, Sbu, manual pass in Gamma editor).**

4. **MoMo evidence card - paste this exact text, replacing whatever is currently there:**

   > **Sandbox Collections funding request**
   >
   > OAuth token issued. requesttopay accepted, status 202. Status confirmed, status 200.
   >
   > A 202 request and a 200 status confirm the funding call reached MTN's sandbox. They do not mean a speaker was paid. This funds the mission, via the AMAZWI ledger. Speaker cash-out is a separate, not-yet-built settlement leg.

5. **Banned-phrase sweep - verification checklist, search every card for these exact fragments and rewrite any hit:**
   - "your MoMo wallet is credited"
   - "cash-out is live"
   - "money crossed MoMo twice"
   - "k-anonymised" / "k-anonymity" (not implemented in this build)
   - "the dataset nobody else has built"
   - any percentage or number attached to MTN revenue, savings, or margin
   - "only" / "first" used as a competitive superlative

6. **Pilot-outcomes card - paste this exact text as a new card (or append to the existing Proven/Pilot/Not Built card if there's room), so this is visible, not only spoken:**

   > **What the pilot measures**
   >
   > Repeat MoMo opens. Funded mission participation. Cost per eligible contribution. Verifier liquidity. Settlement feasibility. Usefulness of intent-labelled speech for MTN's own voice products.
   >
   > None of these numbers exist yet. Each is a commitment to measure and report back, not a claim.

   This card matters more than its size suggests: without a visible commercial-outcomes line, the deck reads as a governed language game. With it, it reads as a proposed MoMo engagement and voice-intent pilot, which is what it actually is.

---

## Final go/no-go - confirm all seven before presenting

1. The team uses `https://gamma.app/docs/1dhqhqj19mgd758`, not the stale `i1kl0ftsc184hbx`.
2. Card 2 uses the corrected market-gap wording (item 2 above - "gives MTN a governed, consented source," not "MTN doesn't have today").
3. The MoMo card says "sandbox Collections funding request" (item 4 above), not "real transaction."
4. Pilot metrics are visible on a slide (item 6 above), not only spoken.
5. No banned claims remain anywhere in the deck (item 5's checklist).
6. Lethabo rehearses the agreement and refusal paths as one continuous demo, not two separate pieces.
7. Both teammates say "AMAZWI ledger credit," never "MoMo wallet payout," in every beat and in Q&A.

---

## Deck history
Three earlier decks are superseded, do not present any of them:
- `.../docs/p6yb4zccmjy3sbi`: pre-calibration, overclaimed "wallet credited."
- `.../docs/ws921eo2ozpw8bp`: original 10-card rubric-mapped version, pre-timing-freeze.
- `.../docs/i1kl0ftsc184hbx`: six-beat version, calibration correct but missing the Proven/Pilot/Not Built slide, the disagreement-path demo, and unscoped pilot-outcome metrics.
Current deck (`1dhqhqj19mgd758`) supersedes all three, but still needs the manual fixes listed above before presenting.
