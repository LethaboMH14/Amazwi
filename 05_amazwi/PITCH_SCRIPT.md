# AMAZWI — Round 1 Pitch Script (six-beat structure, target ~2:50–3:00)

Deck: https://gamma.app/generations/jeKcuz4Nq5WcAJ8Pxw3mP (regenerating — replace with the finished `/docs/...` URL once it lands)
Rubric: Innovation & Creativity 25% · Relevance to Fintech 20% · Feasibility & Scalability 20% · Technical Execution 20% · Presentation & Pitch 15%

Revised against a "what gets this to 90+" critique. Six changes from the prior version:
1. Every mention of the MoMo call now says "funds the mission," never "pays your wallet."
2. A dedicated **PROVEN / PILOT / NOT BUILT** slide — the deck's most important card.
3. Both the agreement path and the disagreement path are demoed/shown, not just the happy path.
4. MoMo evidence is on one clean, minimal slide, labelled SANDBOX.
5. Closes with pilot outcomes we commit to *measure* (acceptance rate, cost per eligible contribution, repeat participation, settlement feasibility) — no numbers attached, since no pilot has run.
6. Removed every unsupported absolute ("the dataset nobody else has built", "only" / "first" claims).

**Feature work stays frozen.** Fixed shape, six beats:

| # | Beat | Time | Speaker |
|---|------|------|---------|
| 1 | Problem | 0:20 | Sbu |
| 2 | Product explanation | 0:30 | Sbu |
| 3 | Live demo — agreement path | 0:45 | Lethabo |
| 3b | Disagreement path (quick cut) | 0:15 | Lethabo |
| 4 | MoMo evidence (sandbox) | 0:20 | Sbu |
| 5 | Proven/Pilot/Not built + pilot ask | ~0:40–0:50 | Sbu |

Total ≈ 2:50–3:00. If judges give exactly 2:30, cut 3b to a single sentence over the same screen rather than dropping it — the disagreement path is now load-bearing evidence, not a nice-to-have.

**Scope calibration — do not undo:** the live MoMo Collections call funds a **mission**, it does not disburse to a speaker's own wallet. Speaker payout is a separate, not-yet-built settlement step. Say "the AMAZWI ledger is credited," never "your MoMo wallet is credited."

---

## 1 — Problem (0:20) — SBU

> "South African languages beyond English are under-resourced in speech AI. isiZulu alone has over twelve million speakers, yet very little open, high-quality speech data exists for it.
>
> And MTN needs meaningful daily engagement inside MoMo. Ayoba shuts down in March — its lifestyle layer goes with it. The wallet stays, with nothing pulling people back to open it."

---

## 2 — Product explanation (0:30) — SBU

> "AMAZWI addresses both. Speak → two human verifiers → a deterministic decision → a transparent reward receipt in an auditable ledger.
>
> A speaker records a short phrase in their own language, inside the MoMo Mini App. Two independent peers verify it — people are the authority, our AI is advisory and never overrules them. Agree, and the AMAZWI ledger is credited once, by construction. Disagree, and nothing is paid — the receipt says exactly why, in the speaker's own language."

*(→ hand to Lethabo)*

---

## 3 — Live demo, agreement path (0:45) — LETHABO

*(Drive the phone, narrate live. Fill in the actual phrase before rehearsal.)*

> "Watch the flow. I record a phrase — [isiZulu/Setswana phrase] — seconds, not minutes.
>
> A peer verifier, a real person on a separate device, hears it and confirms it matches.
>
> They agree — the AMAZWI ledger is credited once, right now. [show receipt]"

## 3b — Disagreement path (0:15) — LETHABO

> "Now the other outcome — pre-captured, for time. Two verifiers disagree. The resolver pays nothing, and the receipt shows R0.00 with the real reason. Refusal is a first-class result here, not a hidden failure."

**Backup if the live demo fails:** fall back to the receipt evidence already in the deck for both paths, say plainly that you're doing so, and move straight to beat 4. Don't stall trying to fix it live.

---

## 4 — MoMo evidence (0:20) — SBU

> "One transaction. Real. Sandbox-labelled. OAuth token issued, requesttopay accepted — 202 — status confirmed — 200. This funds the mission; it is not a payout to a speaker's wallet. Every ledger credit it produces is idempotent — recorded once, never twice, by construction."

---

## 5 — Proven / Pilot / Not built, then the ask (~0:40–0:50) — SBU

> "Here's exactly where we are. **Proven, running today:** consent-gated recording, two-verifier peer decision, an idempotent reward ledger, that live MoMo Collections call — sandbox — and two hundred sixty-four backend tests passing on CI. **Pilot, designed but not yet run with real users:** funded missions at scale, rollout beyond one language, real acceptance and repeat-participation numbers. **Not built, named honestly:** the speaker cash-out leg, automatic answer-correctness scoring, and any margin or cost-saving claim — because it's unmeasured, we're not claiming it.
>
> Which is exactly what the pilot is for. Give us one MTN-supported language and a MoMo partnership to test funded missions and provider settlement, and we'll report back real numbers — acceptance rate, cost per eligible contribution, repeat participation, and what it actually takes to build the settlement leg. Not projections. Measurements.
>
> Izwi lakho linenani — your voice has value, and MoMo is how it gets paid."

---

## Notes for rehearsal
- Time each beat separately, then the whole run against a stopwatch. Beat 3+3b together should not exceed 60s combined — Lethabo rehearses this as one continuous unit, not two separate pieces.
- If judges interrupt with a question, answer in one sentence and return to the next beat.
- Say the word **"sandbox"** out loud on beat 4 — never let it sound like a settled live payment.
- **Never say the MoMo call pays the speaker directly.** It funds the mission; speaker cash-out is Not Built. This was a real overclaim caught in an earlier draft.
- Never state a margin, savings percentage, or cost-reduction number — anywhere, including Q&A. It isn't measured.
- Never say "the dataset nobody else has built," "only," or "first" — these were flagged as unsupported absolutes and removed. If a judge asks about competitors, answer on capability and evidence, not on an unverifiable superlative.
- The Proven/Pilot/Not Built slide is now the deck's centrepiece — if a judge only remembers one slide, it should be this one. Don't rush past it.

---

## Deck history
Two earlier decks are superseded — do not present either:
- `.../docs/p6yb4zccmjy3sbi` — pre-calibration, overclaimed "wallet credited."
- `.../docs/i1kl0ftsc184hbx` — five-beat version, calibration correct but missing the Proven/Pilot/Not Built slide, the disagreement-path demo, and unscoped pilot-outcome metrics. Superseded by the deck linked at the top of this file.
