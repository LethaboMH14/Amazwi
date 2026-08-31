# AMAZWI — Figma design system

**File:** https://www.figma.com/design/JPZuFmbhRh9fhkgBLxRymq
**Owner:** Lethabo · created 2026-08-31

## What is in it

**38 colour variables across five collections**, plus a Foundations sheet documenting the rules.

| Collection | Contents | Why separate |
|---|---|---|
| **AMAZWI Brand (invariant)** | `voice-1-ember` · `voice-2-magenta` · `rand-money-only` · `understood` · `missed-ochre` | **These five never change, whatever the ground is.** Keeping them in their own collection makes that rule structural rather than a note in a document |
| Theme A · Midnight Shweshwe | ground, ground-deep, surface, text-primary, text-secondary, border | **Recommended default** |
| Theme B · Highveld Dusk | same six | Splash and deck only — least legible |
| Theme C · Red Earth (Day) | same six | **Mandatory.** Outdoor legibility |
| Theme D · Ndebele (seasonal) | same six + four accents | September skin |

Every variable is **scope-restricted** — text tokens only offer themselves on text fills, borders only on strokes. Default `ALL_SCOPES` pollutes every picker, so it was set explicitly.

## ⚠️ Plan limitation, and what it costs

The Figma seat is **View on a starter plan**, which allows **one variable mode per collection**. The correct architecture is *one* Theme collection with four modes — switch the whole file between grounds with a dropdown. That needs **Professional or above**.

**The workaround:** each theme is its own collection. It works, but switching themes means rebinding rather than flipping a mode.

**If the plan is upgraded**, collapse Themes A–D into a single collection with four modes. The token names are already identical across all four, so it is a mechanical merge.

## Components — DONE, 31 Aug 2026 (L2/L3)

All four P0-scoped components built directly in Figma (Components page, node `3:2`), every fill/text/border colour bound to a variable — none hardcoded. Screenshotted and visually checked after each build.

| Component | Node ID | Notes |
|---|---|---|
| **Button** | `5:13` (variant set) | `Style=Primary` (`5:11`) fill bound to `voice-1-ember`; `Style=Secondary` (`5:12`) uses `surface`/`border`/`text-primary`. Primary is a **solid**, not the product's ember→magenta gradient — Figma variable binding doesn't reliably bind per-stop gradient colours, so the gradient itself stays defined only in `tokens.css` (`--voice-grad`). Documented on the component, not silently dropped. |
| **Banned-word chip** | `6:5` | One `blocked_words[]` entry as shown to the speaker mid-recording. Border/glyph/text bound to `missed-ochre` (a warning cue — deliberately not red, per brand rule) on `surface`. |
| **Card** | `7:24` | Composes four Banned-word-chip **instances**. Target word + gloss + the four blocked words, sample-populated from `content/cards_setswana.json` (sw-002, kgomo). |
| **Wallet-receipt state** | `10:24` | Composes a Button/`Style=Primary` instance. Status dot + label bound to `understood`; amount bound to `rand-money-only` (used only where real money moves) — copy reads "Sent for payment," never "Paid," matching `content/error_states.json`'s tone rule. |

All bound to Theme A · Midnight Shweshwe as the default rendered theme — the team's actual theme choice is still deferred per `P0.md`, this is just what's visible when opening the file today. Switching which theme a component *shows* is a rebind (see plan limitation above), not a rebuild.

## Skills available

Twelve Figma skills are connected. The two still relevant:

- **`figma-generate-design`** — push whole screens into Figma from the `.dc.html` sources, if we want full-screen composition later.
- **`figma-generate-diagram`** — Mermaid → FigJam. **This is where the architecture diagram for the deck comes from**, not from hand-drawing it at 3am.

## Community reference pass — 31 Aug 2026

Checked Figma Community for genre-appropriate craft references before calling L2/L3 finished: language-learning/gamified-quiz UI kits (Elingo, Coursezy, Learnora AI, the Duolingo recreations). The live embedded canvas previews would not render in the browser tool (Figma's community file viewer needs a WebGL context the sandboxed browser doesn't have) — only static cover thumbnails were inspectable, so this is a directional check, not a pixel-level audit.

**What it confirmed** (no change needed): small-caps label → large bold headline → muted caption stacking (our Card's "YOUR WORD"/"kgomo"/"cow · cattle"), ~24px card radius, a single saturated accent reserved for the primary CTA, oversized bold numerals for the one stat that matters (our "R 2.50"). We were already doing all four.

**One gap found**: this genre consistently pairs a confirmation/achievement line with a small badge glyph, not text alone. Queued as a one-line addition to Wallet-receipt's "Confirmed by 2 verifiers" row (a ✓ bound to `understood`) — the edit was written but the Figma MCP Starter-plan **daily call quota ran out mid-session** before it landed. Component `10:24` is still in its last verified-good state (the text-only version already screenshotted), not broken — this is a queued polish, not a regression. Pick up first thing once the quota resets.

## Deeper Community pass — 31 Aug 2026, with reasoning against AI-slop

Lethabo asked for a more deliberate pass than the earlier directional check, specifically hunting for what makes a theme read as professional vs. as generic AI output, and pushed real Dribbble examples in alongside it — those are analysed in full in `04_assets/reference/REFERENCE.md`. This section is the Figma-Community half.

**The AI-slop signature, named explicitly so it's checkable:** centred hero over a soft blob shape, the default purple-to-blue gradient, rounded-everything with no real hierarchy, Inter at every weight, and illustrations generic enough to belong to any product because they belong to none. Every direction below is checked against that list before it's adopted.

**Search 1 — "dark mode gamified mobile app dashboard":** thin results (3 files), nothing above the AI-slop line worth citing.

**Search 2 — "fintech wallet dark theme UI kit":** 28 results. **Coinpay Fintech Finance Mobile App UI kit** (1.7k likes, 128k uses — by far the strongest signal in this search) is the one worth citing: deep navy/indigo ground, white content cards in a disciplined grid, a single blue accent reserved for actions, near-zero decorative gradient. That's structurally the same discipline our own `voice-1-ember`-only-on-CTA rule already enforces — **this confirms Theme A's restraint is the professional choice, not an accident of not having gotten to decoration yet.** QPay and AiWallet (same search) lean on a heavier neon/violet-on-dark treatment — closer to the AI-slop signature (gradient-heavy, decoration standing in for hierarchy) — deliberately not cited as a direction to follow.

**Search 3 — "african pattern textile app ui":** **zero results.** **Search 4 — "textile pattern background mobile app":** zero file results, one unrelated generative-pattern plugin. **This is an honest, useful finding, not a dead end:** there is no polished mainstream precedent for textile-pattern-as-app-chrome to lean on. Two consequences, stated plainly rather than papered over:
1. The shweshwe/Ndebele pattern direction in our theme system is genuinely differentiated — not generic, which is the opposite of AI-slop by definition.
2. There's no reference for executing it tastefully, which is real execution risk. **The mitigation is restraint**: a pattern belongs in a border, a divider, a splash/loading moment, or a low-opacity watermark — never a bold full-bleed background wash behind body text. Treat pattern-as-accent, not pattern-as-wallpaper, until there's a version of it actually screenshotted and contrast-checked.

## Next steps in Figma (not P0, pick up only if time remains)

1. **Queued from today's rate limit**: the ✓ badge on Wallet-receipt's confirmation line (see above)
2. A type ramp as text styles (Archivo, width + weight axes)
3. Elevation as effect styles — the elevation + inner-highlight pair from the craft pass
4. Architecture diagram into FigJam for the deck (L5 asset)
5. Verifier-flow and consent-screen components, once Gate C settles the real UX
