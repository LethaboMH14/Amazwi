# Accessibility evidence — the real React frontend

**Date:** 2 Sep 2026 · **Scope:** `starter/frontend/src/`, all five routes (`/`, `/consent`, `/record/:contributionId`, `/verify`, `/result/:contributionId`), Chromium at 320 / 360 / 390 / 430 / 480 CSS px, in both selectable themes.
**Task:** `docs/superpowers/plans/2026-09-01-amazwi-03-signal-flow-ops.md` Task 11 — "Add 320–480px, 200% zoom, keyboard, and screen-reader gates".

**What this is not:** a WCAG conformance claim. It is a record of what an automated suite actually measured on this date, in a real browser, on the real application — plus the specific things it does **not** cover, listed in §6. Automated tooling catches a minority of real accessibility barriers; passing it is a floor, not a certificate.

The companion document for the static design mockups is [`04_assets/mockups_v2/ACCESSIBILITY_EVIDENCE.md`](../../04_assets/mockups_v2/ACCESSIBILITY_EVIDENCE.md). That file's §3 warned that the fixed-390px mockup canvases structurally cannot pass WCAG 1.4.10 Reflow, and that the real frontend must not inherit the defect. §2 below is the check of whether it did.

---

## Method

`@playwright/test` + `@axe-core/playwright`, driving the actual Vite dev server — not a static snapshot, not jsdom. Config: `playwright.config.ts`; specs: `e2e/accessibility.spec.ts`, `e2e/routes.spec.ts`; run with `npm run test:e2e`.

Five Chromium projects at 320/360/390/430/480 px wide cover the low-end Android band the product targets. Every spec stubs `/api/*` itself, so the gates measure layout and semantics rather than backend availability.

Measurements are taken from the live DOM — `getBoundingClientRect()` for sizes, `document.documentElement.scrollWidth` vs `clientWidth` for reflow, and **real `page.keyboard.press("Tab")` presses** for focus, because Chromium only sets `:focus-visible` from a genuine keyboard interaction and a scripted `.focus()` would produce a false pass.

### Two harness bugs found first, both of which had been producing false evidence

Recording these because the run that preceded this one produced 15 "failures" that were not real, and this pass nearly inherited them.

1. **The suite was measuring a different application.** `playwright.config.ts` had `reuseExistingServer: true` on port 5174. An unrelated project's dev server was already listening there, so Playwright silently attached to it. The captured `test-results/**/error-context.md` snapshots are of that other app's page, not AMAZWI. Fixed: dedicated port 5199, `reuseExistingServer: false`, with the reason recorded in a comment so nobody restores it.

2. **The API stub was breaking the app under test.** `e2e/fixtures.ts` routed the glob `**/api/**`, which also matches the application's own source module `/src/api/client.ts`. Vite's JavaScript was answered with `application/json`; the browser refused the module (`Expected a JavaScript-or-Wasm module script but the server responded with a MIME type of "application/json"`), React never mounted, and every route rendered an empty `<div id="root">`. **The reflow, touch-target and axe gates were all passing vacuously against a blank page.** Fixed: the route now matches a URL predicate, `url.pathname.startsWith("/api/")`.

Only after both fixes does anything below mean anything. A green gate on an unmounted page is worse than no gate, because it looks like evidence.

Two portability fixes were needed to run at all on Windows and are noted in the config: `npm run dev` cannot be spawned by Playwright's `webServer` (`The system cannot execute the specified program`), so Vite's bin is invoked through `node`; and Vite binds IPv6 `::1` only by default, so a `127.0.0.1` readiness probe never resolves — `--host 127.0.0.1` is required.

---

## Findings

### 1. Touch target size — REAL FAILURE ON ALL FIVE ROUTES, fixed

Every interactive control rendered at the Chromium UA default height of **19–21px**. Literal measurements from the failing run:

| Route | Control | Measured |
|---|---|---|
| home | theme `<select>` | 141 × **19** |
| home | "Contribute an isiZulu voice card" | 276 × **21** |
| consent | "Continue" | 69 × **21** |
| recording | "Start recording" | 103 × **21** |
| verification | "Submit answer" | 104 × **21** |
| result | "Back to AMAZWI" | 120 × **21** |

Cause: the `.route` class every route already carried **had no CSS rule defined anywhere**. The markup was fine; there was simply no stylesheet behind it.

Note on the fix pattern: the mockup pass had to convert styled `<div>`s into real `<button>`s using `all: unset` plus re-declared styles. **That conversion does not apply here** — these are already genuine `<button>`, `<a href>` and `<select>` elements, so the semantics were never the problem. What was missing was size and colour. Fixed in `src/signal-flow.css` with `min-height: 44px; min-width: 44px` on controls and a 44px-minimum `<label>` row, all in relative/percentage units.

**Now passes on all five routes at all five widths.**

### 2. Reflow at 200% zoom — one real failure, fixed; the mockup defect was NOT inherited

The check doubles the root font size and asserts `scrollWidth <= clientWidth`.

Four of five routes passed before any change — the React app genuinely uses relative units, so the fixed-pixel-canvas defect from the mockups did **not** carry over. That was the specific risk flagged in the mockup evidence, and it is confirmed clear.

`/result` failed: **`scrollWidth` 377 vs `clientWidth` 320** at the 320px viewport. Fixed by the same `.route` block — `max-width: 100%` on children and `overflow-wrap: anywhere`, so long unbroken tokens (ids, currency strings) wrap instead of widening the document.

**Now passes on all five routes at all five widths.** A `do not reintroduce a fixed pixel width` comment sits on the rule.

### 3. Keyboard — passed once the app actually rendered; no gap found

For every route the suite Tabs through every visible interactive element and asserts, per stop: `:focus-visible` matches after a **real** Tab press, computed `outline-width > 0`, focus never enters an `aria-hidden` subtree, and the element has a non-empty accessible name. It also asserts Enter activates the consent primary action and Space activates the recording control, both observed in Chromium.

All passed. Note this was **not** verified before the fixes — those runs failed for the blank-page reason in the method section, not for a keyboard reason. The `:focus-visible` outline is now explicit (`3px solid var(--voice-1)`) rather than the UA default, since restyling the controls would otherwise have removed the very ring the gate checks.

The `<audio>` element on `/verify` is treated as a single stop; its shadow-DOM internals are UA-provided and are not ours to name or style. Stated as a deliberate exclusion, not an oversight.

### 4. Screen-reader semantics — two real gaps, both fixed

**`/verify` exposed no `aria-live` region at all.** `StatusAnnouncer` (polite + assertive, `aria-atomic`) already existed in `components/SignalPrimitives.tsx` and was **never wired into any route**. `VerificationRoute` drove four status transitions (loading, ready, submitting, recorded) through bare `<p>` tags, which a screen reader does not announce. Fixed by rendering `StatusAnnouncer`, which also means the regions are present in the accessibility tree *before* their text changes — a live region injected at the same moment as its content is frequently missed.

**`/` had an unlabelled `<main>` landmark.** The other four routes carried `aria-labelledby`; home did not. Fixed with `aria-labelledby="home-title"` pointing at its own `<h1>`.

### 5. axe-core — real `color-contrast` violations on two routes, fixed

Tags `wcag2a, wcag2aa, wcag21a, wcag21aa`; the gate fails on `serious` or `critical`. Violations found, identical in both themes:

```
color-contrast: a     (home)
color-contrast: a     (result)
```

Cause: unstyled `<a>` elements rendered in the UA default link blue (`#0000EE`) against the dark `--ground`. Fixed by giving links the theme's own `--text` colour with a visible underline, so they inherit whatever contrast the palette already guarantees rather than a hardcoded value.

**All 10 route×theme axe checks now pass at all five widths, with zero serious or critical violations.**

### 6. Theme switching was broken, found while checking §5 — fixed, but the naming needs Lethabo's confirmation

Not part of the Task 11 brief; found because the axe results were suspiciously identical across "midnight" and "daylight".

`theme.tsx` writes `data-theme="midnight" | "daylight" | "ndebele"`. The canonical `tokens.css` defines `shweshwe` (as `:root`) · `dusk` · `earth` · `ndebele` · `ink`. **Neither `midnight` nor `daylight` matched any selector.** `midnight` fell through to `:root`, which happens to be the intended dark palette — so it looked correct by accident. `daylight` also matched nothing, so **selecting the light theme rendered the dark palette**. That is a real user-visible bug, and it meant the axe sweep was testing one palette twice while appearing to cover two.

Fixed with a `[data-theme="daylight"]` alias in `src/signal-flow.css`, not in `tokens.css` — that file is byte-for-byte synced against `04_assets/themes/tokens.css` by `tokens.sync.test.ts` and must never be hand-edited.

Verified in a real browser, not inferred: before the fix `--ground` computed to `#0C1123` under `daylight`; after, `#FBF2E6` with `body` background `rgb(251, 242, 230)` and text `rgb(36, 20, 8)`. Screenshots at 320px confirm the light rendering, with the `--voice-*` brand gradient unchanged as the token file's invariant requires.

⚠️ **Open, needs Lethabo:** mapping "Signal Daylight" onto the `earth` palette is the only reading `tokens.css` supports — it is the sole light palette — but which canonical theme each product-facing name refers to is a **design decision, not a mechanical one**. Flagged rather than treated as settled. The alternative and cleaner long-term fix is to rename the themes in `theme.tsx` to the canonical names, which would change `theme.test.tsx` and the persisted `localStorage` value.

---

## Summary

| Check | Before | After | How verified |
|---|---|---|---|
| Touch targets ≥44×44, 5 routes | **Fail, 19–21px** | Pass | `getBoundingClientRect()` on live DOM |
| Reflow at 200% zoom | **Fail on `/result`** (377 > 320) | Pass | `scrollWidth` vs `clientWidth` after doubling root font |
| No horizontal overflow at viewport | Pass | Pass | Same |
| Keyboard Tab order + focus ring | Not verifiable (blank page) | Pass | Real `Tab` presses; `:focus-visible` + computed outline |
| Enter / Space activation | Not verifiable | Pass | Real key presses in Chromium |
| Labelled `<main>` on every route | **Fail on `/`** | Pass | DOM query for `aria-label`/`aria-labelledby` |
| `aria-live` contract | **Fail on `/verify`** (none present) | Pass | DOM query for `[aria-live]` polite + assertive |
| axe serious/critical, 5 routes × 2 themes | **Fail: `color-contrast` on home, result** | Pass | `@axe-core/playwright`, wcag2a/2aa/21a/21aa |
| Light theme actually light | **Fail — rendered dark** | Pass | Computed `--ground` + screenshot |

**Final run: 195/195 passing** across 5 viewport widths (`npx playwright test`). Unit suite 57/57 (`npm test`); `npx tsc -b --noEmit` clean; `vite build` succeeds.

---

## What this does NOT cover — open, not silently skipped

1. **Chromium only.** No WebKit or Firefox run. Focus-ring and `<audio>` behaviour in particular differ across engines.
2. **No real screen reader.** The `aria-live` regions and landmark labels are verified as *present and correctly attributed in the DOM*. Nobody has listened to NVDA, VoiceOver or TalkBack actually announce them, and announcement order/politeness under real AT is not something a DOM query can prove.
3. **No real device.** All measurements are Chromium viewport emulation, not a physical low-end Android handset. Touch targets are geometrically correct; actual thumb ergonomics are untested.
4. **`prefers-reduced-motion` not live-toggled.** The `!important` reset in `tokens.css`/`signal-flow.css` was read, not observed firing — the same limitation recorded in the mockup evidence.
5. **200% zoom is emulated by doubling the root font size**, which is what text-zoom does to a relative-unit layout. Browser full-page zoom is a related but not identical operation.
6. **Automated axe only.** Reading order, meaningful sequence, error-recovery quality, and whether the isiZulu/Setswana copy is comprehensible to the people it is for are all human judgements no scanner makes.
7. **Only the five routes that exist today.** Coverage Constellation, missions, and the MTN Language Ops route (Plan 03 Tasks 7–10) are not built, so they are not gated. When they land, they must be added to `ROUTES` in `e2e/fixtures.ts` — the gates iterate that list, so a new route is otherwise silently ungated.
8. **Contrast is inherited from the token palettes, not independently re-derived.** Links now use `--text` on `--ground`; axe confirms those specific pairs pass, but the palettes as a whole have not been audited pair-by-pair.
