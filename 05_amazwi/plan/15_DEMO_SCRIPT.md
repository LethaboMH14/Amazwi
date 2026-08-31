# AMAZWI — JUDGE-ONLY DEMO SCRIPT (L5/item 7)
### The exact click-through runbook, so either teammate can run it alone

**Status:** the script below is real and ready to rehearse against. The **no-network fallback recording** LETHABO_NEXT_WORK item 7 also asks for is **not producible yet** — a fallback recording has to be a screen capture of the actual running golden path, and that path doesn't exist until Gate D (real recording) and Gate E (real verification) are built. Recording the current static mockups and presenting that as a "fallback demo" would be exactly the kind of dishonesty `06_PITCH.md` §5 and §12 explicitly rule out ("we are not presenting simulated rands as a production transfer" — the same logic extends to presenting a mockup click-through as if it were the live app's fallback). **This file gets a second half — the recording itself — once Gate D/E exist,** not before.

---

## Setup, before judges arrive

1. Speaker device: fully charged, mic permission pre-granted, on the judge-only path (not room-guest mode).
2. Two verifier devices: same — permissions pre-granted, logged into distinct verifier accounts.
3. One display/laptop for the deck (`plan/14_DECK_SKELETON.md`).
4. Confirm provider mode banner reads `DEMO_PROVIDER` on the speaker device before judges walk up — if it doesn't, fix it before the demo starts, not during.
5. Confirm the reset script has run — `05_BUILD.md` §7 "Seeded recovery" — so the golden path starts from known state.

## The script

| Beat | What you say | What you tap | What judges see |
|---|---|---|---|
| 1. Open | *(§3, verbatim)* "Who understood that?" — play the pre-recorded clip/transcript comparison | Play clip on the deck | The gap between human and system understanding |
| 2. Product sentence | *(§3, verbatim)* "AMAZWI is a MoMo voice game..." | Advance deck | The one-sentence pitch |
| 3. Consent | — | Speaker device: accept purpose-specific consent | Five separately declinable items, not one bundled toggle |
| 4. Card reveal | "Here's their word" | Speaker device: card appears | Target word + gloss + four banned words as chips |
| 5. Recording | "Thirty seconds, banned words in view the whole time" | Speaker records a clue | Ring timer, live waveform |
| 6. Verifier flow ×2 | "Two independent phones, no coordination between them" | Each verifier: free-text guess, then referee decision | Answer locks before reveal; banned-word question after |
| 7. The money moment | *(pause, let it land)* | — | "Both of them understood you", R2.00 lands |
| 8. Receipt | *(§6, verbatim)* "One screen proves what was contributed, why it qualified, what it earned, what the person consented to and where the value is now." | Open Voice Value Receipt | Full field set — contribution ID through consent version |
| 9. Technical truth | *(§5, verbatim, the demo-provider line if active)* | — | Sbu takes this beat |
| 10. Why MoMo | *(§7, verbatim)* | — | Sbu takes this beat |
| 11. Close | *(§9, verbatim)* "This voice stayed under the contributor's control..." then "Speak. Be understood. Earn." | Show Impact Map | Aggregate map + the ask |

**Room-guest MCQ mode** (optional, only if the judge-only path is healthy and there's time): say the exact §4 line before inviting the room in — *"This audience round is the learner game. It moves XP and popularity, not the governed corpus decision."*

## Substitution triggers — decide the tell, not just the switch

Per `05_BUILD.md` §7 and `06_PITCH.md` §12, every substitution is **said out loud**, not silently absorbed:

| If this happens | Say this, then do this |
|---|---|
| Room Wi-Fi is bad or absent | "We're staying on the judge-only path — that's the actual product proof, not a compromise." Skip room-guest mode entirely. |
| Speaker's phone fails to record | "Switching to our tested backup speaker phone." Use it — don't troubleshoot live. |
| One verifier device fails | "Down to one tested backup verifier — the second one stays honestly in the waiting state until it's fixed." Show the honest waiting state on the receipt, don't fake a second confirmation. |
| Collections is unavailable | "This funding leg is a labelled seeded mission, not a live inbound payment." |
| Disbursement is unavailable | "This is our labelled demo provider — the state machine and idempotency are real; the rand amount is not a production transfer." |
| Mini App host is unavailable | "We're in browser demo mode — labelled, and the host adapter spec is documented separately." |
| Everything fails | *(once the real fallback recording exists — see status note above)* Play it, narrate over it, no repeated apologising. |

## Rehearsal checklist — L6, still open

- [ ] Both teammates can run beats 1–8 alone, start to finish, without the other prompting them.
- [ ] Both teammates can say every substitution line from memory, not read off this page.
- [ ] Timed at least once — the whole judge-only path should comfortably fit inside the pitch's live-demo window.

This checklist is the actual content of L6. Per Lethabo's explicit call on 31 Aug, L6 itself is deferred — "we will do later" — this script exists now so the rehearsal has something concrete to rehearse against when it happens, not a blank page.
