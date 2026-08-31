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

## Skills available

Twelve Figma skills are connected. The three that matter for us:

- **`figma-generate-library`** — components with variant sets and token bindings. The next step: build the card, chip, wallet row, league row and button as real components.
- **`figma-generate-design`** — push whole screens into Figma from the `.dc.html` sources.
- **`figma-generate-diagram`** — Mermaid → FigJam. **This is where the architecture diagram for the deck comes from**, not from hand-drawing it at 3am.

## Next steps in Figma

1. Components: card, banned-word chip, wallet state row, league row, primary button — with variants
2. A type ramp as text styles (Archivo, width + weight axes)
3. Elevation as effect styles — the elevation + inner-highlight pair from the craft pass
4. Architecture diagram into FigJam for the deck
