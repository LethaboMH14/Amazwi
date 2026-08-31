# REFINEMENT BRIEF — AMAZWI mockups
### For Sbu · hand this to Codex / GPT with the `.dc.html` sources

**Status: not finished.** Three screens have had a craft pass and set the bar. Seven are wireframes wearing the palette — structurally correct, visually below the reference examples. **Do not put the wireframes in front of a judge as they are.**

| Fidelity | Screens |
|---|---|
| ✅ **Crafted** — use as the reference | `Main` (card reveal) · `Recording` · `Understood` (money moment) |
| ⚠️ **Wireframe** — needs the pass | `Consent` · `Listen` · `Referee` · `Wallet` · `Receipt` · `League` · `Archive` |

---

## 1. THE HONEST DIAGNOSIS

Held against the reference set — kuest, the glassmorphic fitness app, the isometric map, the spin-to-win screens — the first version failed on six things. Every one is fixable in CSS.

| Missing | What the references have | Cost to fix |
|---|---|---|
| **Depth** | Layered cards, real elevation, cast shadows | Trivial |
| **Material** | Grain, noise, translucency, gradient mesh — surfaces that feel like *something* | Trivial |
| **Inner highlight** | A 1px light line on the top edge of every raised surface | Trivial — **and it is the single highest-impact detail in dark UI** |
| **Imagery** | Illustration, avatars, photography, iconography with a point of view | Medium |
| **Type craft** | Real contrast between levels, tight display tracking, optical sizing | Trivial |
| **Composition** | Asymmetry, deliberate density shifts, a focal point | Medium — needs judgement, not code |

---

## 2. THE CRAFT LAYER — lift these verbatim from `Main.dc.html`

**a · Ambient radial glow.** The biggest single win. One warm blob behind the focal element, one cooler counterweight.
```css
position: absolute; width: 460px; height: 460px; left: -110px; top: 88px; border-radius: 999px;
background: radial-gradient(circle, rgba(255,90,54,0.30) 0%, rgba(232,38,127,0.13) 42%, rgba(20,16,14,0) 68%);
filter: blur(8px);
```

**b · Film grain.** Inline SVG turbulence, no asset, ~400 bytes. Turns flat dark fills into material.
```css
.grain { position: absolute; inset: 0; pointer-events: none; opacity: 0.5; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)' opacity='0.55'/%3E%3C/svg%3E"); }
```

**c · Elevation + inner top highlight.** On every raised surface. **This is the detail that separates expensive dark UI from amateur dark UI** — the light line reads as a physical edge catching light.
```css
box-shadow: 0 20px 44px -18px rgba(0,0,0,0.9), inset 0 1px 0 rgba(250,246,241,0.07);
background: linear-gradient(180deg, rgba(42,35,31,0.92), rgba(28,23,20,0.92));
border: 1px solid rgba(250,246,241,0.09);
```

**d · Gradient display type.** Never flat white for a hero word or number.
```css
background: linear-gradient(168deg, #FFF6F0 8%, #FFC9B4 58%, #F08A9E 100%);
-webkit-background-clip: text; background-clip: text; color: transparent;
text-shadow: 0 0 44px rgba(255,90,54,0.22);
```

**e · Type scale with real contrast.** Display 54px / weight 800 / stretch 125% / tracking **-0.035em**. Labels 11px / weight 700 / tracking **+0.22em** / uppercase / 38% opacity. The gap between them is what makes it look designed.

**f · Coloured glow on live indicators.** A recording dot is `box-shadow: 0 0 10px 2px rgba(232,38,127,0.85)`, not a flat circle.

---

## 3. WHAT TO ASK CODEX FOR, SCREEN BY SCREEN

Give it the `.dc.html` source, the craft layer above, and the constraints in §4.

**`Consent`** — the least interesting screen doing the most important job. Ask for: an illustrated header (a waveform becoming a shield, or similar), toggle rows with real depth and a satisfying on-state, and a visual distinction between the three required items and the two optional ones.

**`Listen`** — needs tension. It is the MCQ learner game, not a validation screen. Ask for: a playback control that feels tactile, a waveform that shows played-vs-remaining progress, answer options with real press states, a countdown, and a visible XP-only/non-validation note.

**`Referee`** — the most important screen in the product and currently the flattest. Ask for: a clear two-part composition (the verifier's locked free-text answer on top, reveal and referee question below), and a Yes/No pair that reads as a genuine decision. Do not show the other verifier's answer before this vote.

**`Wallet`** — deliberately restrained, but restraint is not flatness. Ask for: a hero balance card with real material, three genuinely distinct state treatments, and a small sparkline of the week. **Keep it boring. No gradient on the numbers.**

**`Receipt`** — should feel like a *document*. Ask for: a perforated or torn top edge, a subtle paper texture, a monospaced reference number, and a verification seal.

**`League`** — the biggest opportunity. Ask for: tier badge iconography, avatars on every row, a promotion zone that visibly glows, and the user's row raised above the others. **No losing state, no national last place.**

**`Archive`** *(filename retained; screen is now Impact Map)* — should be the most beautiful screen. Ask for: a South Africa aggregate dot field with depth and glow, broad language/campaign totals and funds remaining. No public clip playback, story chains, names or exact locations. This is the closing image.

---

## 4. CONSTRAINTS CODEX MUST NOT BREAK

Paste this block into the prompt.

```
- MTN yellow #FFCB05 appears ONLY where money moves. Nothing decorative is yellow.
- The app's own identity is the ember→magenta gradient: #FF5A36 → #E8267F.
- A missed guess is ochre #8A6A1F, never red. Not being understood is information, not an error.
- Ground #14100E, raised surfaces #2A231F, text #FAF6F1. Warm neutrals, never blue-grey.
- Font: Archivo (Google Fonts, width + weight axes). Not Inter.
- 390×844 phone frame. NO fake status bar — the real one renders on top.
- Hit targets never below 44px.
- Two listeners, never three.
- MCQ is learner gameplay and XP only; two proficient free-text verifiers decide eligibility.
- Listeners/verifiers do not receive cash in the competition build.
- The LISTENER referees the banned-word rule, never the speaker.
- Money screens never say "paid" before the provider confirms.
- The league has no losing state and no national last place.
- No randomised/chance mechanics anywhere — SA regulatory constraint.
- No public raw-audio archive or named attribution. The public map is aggregate.
- Never generate images of South African people. Illustration, type and texture only.
- Target ≤200KB first paint: CSS and inline SVG, no image assets, no libraries.
```

---

## 5. HOW TO GET THE CHANGES BACK ONTO THE CANVAS

The `.dc.html` files are plain HTML — Codex can edit them directly. To rebuild the canvas afterwards:

```bash
node "<design skill base>/seed-canvas.mjs" \
  --template "<design skill base>/payload.template.html" \
  --out amazwi-app-mockups.html --title "AMAZWI App Mockups" \
  --artboard Main.dc.html --artboard Consent.dc.html --artboard Recording.dc.html \
  --artboard Listen.dc.html --artboard Referee.dc.html --artboard Understood.dc.html \
  --artboard Wallet.dc.html --artboard Receipt.dc.html --artboard League.dc.html \
  --artboard Archive.dc.html --canvas canvas.json
```

Then republish to the same URL. Keep the file structure — one artboard per file, `Main.dc.html` is the entry.

---

## 6. THE BAR TO HIT

The reference set is the standard, and each one is strong at something different:

- **kuest** — completeness. A real information architecture, not a hero shot. Steal its rank badges, quest rows and podium.
- **The fitness app** — pure craft. Soft shadows, translucency, micro-typography. The highest finish in the set.
- **The isometric map** — the only structurally *different* one. Depth, atmosphere, a sense of place.
- **Spin-to-win** — joy. The only one that expresses energy, which is what our own board was missing.

**And the three gaps none of them fills, which is where we can actually win:** none of them is funny, none is specifically *South African* (Ndebele geometry, Kaaps, a taxi rank — never generic "Africa"), and none shows a failure state.

Full critique of all thirteen references: [`../../05_amazwi/plan/09_MOCKUP_LIBRARY.md`](../../05_amazwi/plan/09_MOCKUP_LIBRARY.md).
