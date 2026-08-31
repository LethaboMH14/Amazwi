# Lethabo — next experience-lane work

> ✅ **CLOSED 31 Aug 2026 — items 1–6 done, item 7 half.** Full detail of what was done, how, and what's still open per item: `P0.md`'s LETHABO_NEXT_WORK section and `BUILD_LOG.md`'s entries from ~20:35 onward. Headlines: real bugs found and fixed along the way (not just the listed warnings) — a mislabelled-language word bug, a keyboard-reachability gap now fixed with real `<button>` elements, an under-sized touch target. Item 7's fallback recording is explicitly not produced yet (needs a real running golden path — Gate D/E — to record honestly). One open item is Lethabo's own, not Sbu's: the sw-004/005/007 distractor swaps in `cards_setswana.json` still need a native read-aloud confirmation, same bar as the original 8 — flagged here so it doesn't get missed, not asking Sbu to do it. Sbu: everything else is ready for your review.

This is the current handoff from Sbu. It does not reopen scope. Work top to bottom; every task has an observable exit condition.

## 1. Close the Setswana content warnings

The deck is validator-clean but still emits three review warnings because blocked words are reused as learner distractors:

- `sw-004`: `phaphosi`
- `sw-005`: `pula`
- `sw-007`: `seswaa`, `morogo`

For each card, either replace the distractor or record why reuse is intentional. **Exit:** `validate_cards.mjs` has zero errors and every remaining warning has an explicit native-owner acceptance in `BUILD_LOG.md`.

## 2. Finish the Setswana error-copy pass

Read all ten states aloud on a phone-sized screen. Pay special attention to `campaign_empty`, where replacing `tekanyo` with class-3/4 `mogato` required concord changes. Check titles for natural game language, not dictionary correctness alone.

**Exit:** Lethabo marks the `tn` pack reviewed in `_meta.status`; `validate_error_states.mjs` passes; no uncertain wording remains hidden in metadata.

## 3. Reconcile stale mockup content

The mockup READMEs still say `SEFOFANE` and its blocked words are unverified, although the Setswana deck is now native-reviewed. Replace stale warning text and ensure every visible card value comes from `content/cards_setswana.json` or `content/cards_isizulu.json`.

Remove or clearly label non-P0 surfaces such as League from the judge-facing compiled canvas. Regenerate the compiled mockup only from the corrected source screens.

**Exit:** no judge-facing mockup contains placeholder/unverified card copy or implies leagues are P0.

## 4. Produce the five hero screens

Complete the craft pass for:

1. card reveal;
2. recording;
3. proficient-verifier/referee;
4. Voice Value Receipt;
5. aggregate Impact Map.

Receipt must say `DEMO_PROVIDER` / “demo provider, not a real transfer.” Learner MCQ stays XP-only. Own-clip replay appears only under active consent.

**Exit:** all five screens form one judge-only story and use the frozen product/state copy.

## 5. Wire and choose the visual ground

Use `04_assets/themes/tokens.css`; component CSS must not add theme-specific hex values. Keep `earth` available as the day/accessibility theme. Shortlist three themes only after a target-device check.

**Exit:** one hero screen switches themes with `data-theme`, retains readable contrast and does not move layout.

## 6. Accessibility and resilience evidence

Test the five-screen path at phone width, 200% zoom, keyboard-only navigation and reduced-motion preference. Check visible focus, 44×44 minimum touch targets, text reflow, microphone-denied recovery and provider-unavailable copy.

**Exit:** capture one screenshot per hero screen plus the two highest-risk error states, and log what was actually verified. Do not claim WCAG compliance from screenshots alone.

## 7. Pitch skeleton and rehearsal pack

Use real screenshots only. Build the ten-slide skeleton around the golden path, limitations and honest provider state. Prepare a judge-only demo script plus a no-network fallback recording. Rehearse the open and close so either teammate can present alone.

**Exit:** every product claim shown in the deck is visible in the demo or explicitly labelled as future work.

## Do not add

- leagues, redemption, synthesis, public audio or new game modes;
- live MoMo claims—the current account has no subscriptions;
- learner guesses as eligibility or speaker feedback;
- a declared-language shell before both complete shell-copy packs exist.
