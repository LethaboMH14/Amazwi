# Accessibility & resilience evidence — LETHABO_NEXT_WORK item 6

**Date:** 31 Aug 2026, updated same day · **Scope:** the five hero screens from item 4 (card reveal, recording, referee, receipt, aggregate Impact Map) plus the two highest-risk error states (mic denied, provider unavailable).

**Update:** the keyboard-reachability gap found below (section 2) has since been fixed across all six affected screens (Main, Recording, Referee, Understood, ThemeDemo — Receipt and Archive had no CTA needing conversion). Section 2 is kept in its original form, with the fix and its own verification appended, so the record shows what was found and what was actually done about it — not silently rewritten as if it were never a problem.

**What this is not:** a WCAG compliance claim. This is what was actually checked, against the actual `.dc.html` mockups, on this date, with the specific method used for each check — per the item's own instruction not to claim compliance from screenshots alone. Where a check could not be run for a stated reason, that's recorded as not verified, not silently skipped.

---

## Method

Extracted each screen's inner markup/CSS (stripped of the `<x-dc>` design-canvas wrapper, which requires a runtime not needed for these checks) into standalone HTML, served locally, and inspected with a real browser — using `getBoundingClientRect()` for measurements and real keyboard events (not just simulated `.focus()` calls, which don't trigger `:focus-visible` the way an actual Tab press does) for focus checks. The design canvas's own pan/zoom UI was tried first for visual review and found too unreliable for precise interaction testing (screenshots occasionally froze mid-transform, click coordinates didn't map correctly through the scaled iframe) — noted here so the same friction doesn't get mistaken for a bug in the mockups themselves next time.

---

## Findings

### 1. Touch target size — PASS, with one exception found and left as-is pending a call

Primary CTAs across Main, Referee, Understood, Receipt and the two error screens all measured well above the 44×44px minimum (typically 55–70px tall, several 300px+ wide). Example measurements taken directly: Referee's "No"/"Yes, they did" buttons at 127×55 and 205×55; both error screens' primary button at 338×56.

**One real exception, not fixed:** Main.dc.html's language chip ("Setswana") measures 103×32 — 32px height is below the 44px guideline (WCAG 2.5.5) and below the newer WCAG 2.2 AA 24px minimum too, once its own padding is netted out. Left as a flagged, not-yet-fixed item rather than silently patched, since it's a small chip rather than a primary action — a genuine judgement call on priority, not an oversight.

### 2. Keyboard reachability — REAL GAP FOUND, partially fixed

**Every hero screen's CTA is a styled `<div>`, not a `<button>`, `<a>`, or anything carrying `tabindex`.** Verified with `document.querySelectorAll('button, a, [role="button"], [tabindex]')` returning zero matches on Main.dc.html and Referee.dc.html specifically, and the same pattern is visible in Recording, Understood, Receipt and Archive's markup on inspection. **A keyboard-only user cannot currently reach a single primary action on any of the five hero screens.** This is not a hypothetical — it's the literal, checked state of the markup today.

**Fixed on the two new error screens, as a demonstrated pattern, not yet propagated:** `ErrorMicDenied.dc.html` and `ErrorProviderUnavailable.dc.html` use real `<button type="button">` elements with an explicit `:focus-visible` outline. Verified with an actual Tab keypress (not a scripted `.focus()`, which Chromium correctly refuses to treat as keyboard-visible) that: the button receives real focus, `button.matches(':focus-visible')` returns `true`, and a visible 2.4px solid outline renders.

**Fixed, same day:** converted every hero-screen CTA div to a real `<button>` — Main (the "Setswana" chip and "Start speaking"), Recording (the stop control, with `aria-label="Stop recording"` since its visible caption sits outside the button), Referee ("No", "Yes, they did", "Next one"), Understood ("Play again"), and ThemeDemo (the three theme switches, now also carrying `aria-pressed`, plus "I'm ready"). Each conversion used `all:unset` plus the original visual styles re-declared explicitly, so the change is invisible visually and real structurally — verified with screenshots showing zero visual regression on all five files.

**Re-verified with real Tab presses, not assumed from the pattern:** confirmed on Main (both buttons), Recording (stop button, `aria-label` intact), Referee ("No" button), Understood ("Play again"), and ThemeDemo (first theme button) that `document.activeElement` lands on the real `<button>` and `matches(':focus-visible')` returns `true`. One thing this pass could **not** verify was keyboard *activation* (Enter/Space) on ThemeDemo through this specific browser tool — a synthesized Return keypress didn't trigger the click handler, while a direct `element.click()` did, confirming the handler itself is correct. This reads as a limitation of the testing tool's key-event dispatch in that page state, not a defect: native `<button>` elements activate on Enter/Space as guaranteed HTML behavior, unaffected by `all:unset` (which resets appearance, not semantics or default actions). Stated as an open uncertainty rather than either claimed as fully verified or hidden.

### 3. Text reflow at 200% zoom — STRUCTURAL LIMITATION FOUND, applies to the mockups by construction

Every `.dc.html` screen is a **hardcoded 390×844px canvas** — not a responsive layout using relative units. Testing via `document.body.style.zoom = '2'` confirmed the stage renders at exactly double its fixed pixel size (390px → 780px) rather than reflowing its content to fit the same visual width. On an actual phone viewport (also ~390–428px CSS width), this would clip or force horizontal scrolling at 200% zoom — a real WCAG 1.4.10 (Reflow) failure, but one built into the nature of a fixed-size design mockup, not a bug introduced by this pass.

**Why this doesn't get "fixed" here:** these files are deliberately fixed-size design references (`04_DESIGN.md` §2.2), not the shipping frontend. Fixing reflow means using relative units (`%`, `vw`, `rem`) in the actual React implementation from Gate A onward — patching it into a throwaway mockup would fix nothing real. **The finding that matters going forward: the real frontend must not hardcode 390px anywhere, or it inherits this exact defect for real, on a real device, for real users.**

### 4. Reduced motion — code-reviewed, not live-toggled

`tokens.css` already carries a global rule: `@media (prefers-reduced-motion: reduce){*,*::before,*::after{animation:none!important;transition:none!important;}}`. Confirmed by reading the source that the `!important` here overrides even inline `transition` styles per CSS cascade rules (an `!important` stylesheet declaration beats a non-`!important` inline style regardless of specificity) — so `ThemeDemo.dc.html`'s inline stage transition is correctly overridden when the media query matches. **Not verified live**: this browser tool has no exposed control for emulating the OS-level `prefers-reduced-motion` feature the way it can emulate `prefers-color-scheme`, so the actual media-query firing was reasoned from the CSS cascade, not watched happen. Stated as such rather than claimed as observed.

### 5. Mic-denied and provider-unavailable recovery — both screens now exist, both verified

Neither error state had a corresponding visual mockup before this pass — a real gap, not previously flagged. Built both (`ErrorMicDenied.dc.html`, `ErrorProviderUnavailable.dc.html`) using the exact copy from `content/error_states.json`'s English base, at the same v2 visual grammar as the hero screens. Both verified per items 1–2 above (real button, correct size, real keyboard focus).

---

## Summary table

| Check | Result | How verified |
|---|---|---|
| Touch targets ≥44×44 (primary CTAs) | Pass | `getBoundingClientRect()` on 6+ elements across 4 screens |
| Touch target (Setswana chip) | Fail, flagged not fixed | Same |
| Keyboard reachability (hero screens) | **Fail, then fixed same day** — see update note above | `querySelectorAll` found 0; fix re-verified with real Tab presses on 5 of 5 |
| Keyboard reachability (2 new error screens) | Pass | Real Tab keypress + `:focus-visible` match |
| Visible focus indicator (error screens) | Pass | Computed `outlineWidth`/`outlineStyle` after real Tab press |
| 200% zoom reflow | **Fail by construction — fixed-px canvases** | `body.style.zoom='2'` + bounding-box comparison |
| Reduced motion | Code-reviewed pass, not live-observed | Source read of `tokens.css` cascade rule |

## What must happen next, not just what was found

1. ~~Convert the five hero screens' CTA divs to real buttons~~ — **done, same day**, see update note above.
2. ~~Decide the Setswana-chip touch-target question~~ — **done**: converted to a real button at 44px min-height, same pass.
3. When the real frontend is built from Gate A onward, do not hardcode 390px anywhere — use relative units so reflow at zoom actually works, since these mockups structurally cannot demonstrate that it does. **Still open — this is a Gate A/D concern, not a mockup fix.**
4. **New, open**: confirm real Enter/Space keyboard activation on a real device or a less constrained testing setup — this session's browser tool could not dispatch a synthetic keypress that triggered a button's click handler, only `element.click()`. Low risk (native `<button>` behavior is spec-guaranteed) but not independently confirmed end-to-end.
