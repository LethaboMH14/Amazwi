# AMAZWI mockups — V2

**Canvas:** https://claude.ai/code/artifact/27d81ae1-89f7-4f3c-91be-a29d972597b6

Three screens rebuilt to fix a fair critique: the v1 set was generic.

## What was actually wrong with v1

Not "needed more polish". Five specific structural failures:

1. **One elevation plane** — nothing sat above or below anything else
2. **Symmetric vertical stacks** with uniform 24px padding on every screen
3. **No scale contrast** — everything was mid-sized
4. **Nothing overlapped or bled off canvas**
5. **No signature device** — nothing recognisable if you cropped it

## The visual grammar that fixes it

| | |
|---|---|
| **Type** | Archivo (expanded, 800) for display + **Instrument Serif italic** for accents. The serif is what makes it read editorial rather than app-generic |
| **Scale** | 66–88px display against 10px kickers at 0.34em tracking. No mid-sizes |
| **Signature** | **Overlapping circles.** Two listeners agreeing *is* the mechanic, so two overlapping avatars are simultaneously the content and the logo |
| **Treatments** | Editorial over form-control: banned words are **struck through**, not chips. Meta is a hairline rule, not a card |
| **CTA** | Circle + two lines of type, never a full-width slab |
| **Space** | Fill it with **meaning**, not decoration — v1's dead space became "two people are waiting to hear you" |

## The one that mattered most

The first pass put a large decorative "agreement lens" in the middle of the card screen. It rendered as a smudge. The fix wasn't to make it prettier — it was to realise the lens should be **literal**: the two people who will actually hear the clip. Device and content collapse into the same element, and the dead space disappears.

## Status — updated 31 Aug 2026

| | |
|---|---|
| ✅ V2 | Card reveal · Recording · Proficient verifier/referee · The money moment · Voice Value Receipt · Impact Map (aggregate) |
| ⚠️ Still v1 or unbuilt | Consent · Listen (learner MCQ) · Wallet |
| ✂️ Cut, not built here | League — per `plan/05_BUILD.md` §6 kill rules, deliberately absent from this canvas |

This now covers all five of `LETHABO_NEXT_WORK.md` item 4's named hero screens (card reveal, recording, proficient-verifier/referee, receipt, aggregate Impact Map) plus the money-moment transition between them. Referee, Receipt and Archive were built directly to the v2 grammar below, not upgraded from v1 — there is no v1 version of them still lying around to confuse with.

**Do not mix v1 and v2 in front of a judge.** Consent, Listen and Wallet remain v1 wireframes if they're needed — bring them up before a demo, or route around them.

## Theme wiring — LETHABO_NEXT_WORK item 5, done 31 Aug 2026

`ThemeDemo.dc.html` (artboard 7, marked `is_interactive`) is a real hero screen built entirely from `04_assets/themes/tokens.css` variables — every colour, radius and type value in its component CSS is a `var(--token)`, none hardcoded, matching the source file's own rule ("every component consumes tokens, never hex"). It has three working buttons that call `element.setAttribute('data-theme', ...)` live in the browser.

**Verified, not assumed** — the design canvas's own pan/zoom made in-canvas click testing unreliable, so the exact same markup/CSS/JS was tested standalone (stripped of the `<x-dc>` wrapper only, zero other changes) in a real browser: clicked through all three themes (Midnight Shweshwe default → Red Earth → Ink), confirmed via `getComputedStyle` that `data-theme` and the resolved background colour actually changed (not just visually inspected), and confirmed by eye that text stayed legible and no element moved position in any of the three states. That satisfies the item's exit condition in full: *"one hero screen switches themes with `data-theme`, retains readable contrast and does not move layout."*

Earth and Ink were chosen for the demo because they're the two most divergent grounds (light vs. dark-neutral) — the hardest contrast case, not the easiest. Dusk and Ndebele are not wired into this demo file; per `P0.md`, the final three-theme shortlist is still Sbu's and Lethabo's call after a target-device contrast check, not something to preempt here.

## Accessibility & resilience evidence — LETHABO_NEXT_WORK item 6, done 31 Aug 2026

Full findings in **[`ACCESSIBILITY_EVIDENCE.md`](ACCESSIBILITY_EVIDENCE.md)**. Headline: a real keyboard-reachability gap was found (every hero-screen CTA was a styled `div`, not a button) **and fixed the same day** — all CTAs across Main, Recording, Referee, Understood and ThemeDemo are now real `<button>` elements with verified `:focus-visible` outlines, re-tested with actual Tab presses after the fix. The Setswana chip's under-sized touch target was fixed too (32px → 44px min-height). Still open: these mockups are fixed 390px-wide canvases and cannot pass a real 200%-zoom reflow check by construction — the real frontend must use relative units from Gate A onward or it inherits the same defect for real.

✅ **`SEFOFANE` is real, not placeholder** — it's `sw-001` in `05_amazwi/content/cards_setswana.json`, native-confirmed 31 Aug with the identical target and all four blocked words. No change needed here.
⚠️ Only `Main.dc.html` carries the theme tweak so far.
⚠️ League and Impact Map are v1 wireframes; League is additionally cut per `plan/05_BUILD.md` §6 kill rules and must not appear in any judge-facing compiled canvas regardless of fidelity.
