# AMAZWI — screen mockups

Ten artboards, built from the tokens in [`../../05_amazwi/plan/04_DESIGN.md`](../../05_amazwi/plan/04_DESIGN.md) §2.2.

**Live canvas:** https://claude.ai/code/artifact/889d9d01-823d-4a84-bd00-7d6e88007903

> ⚠️ **NOT FINISHED — three screens are crafted, seven are wireframes.**
> Held against the reference examples these are below the bar: the wireframes have correct structure and content but no depth, material or composition. **Do not put them in front of a judge as they are.**
> **→ [REFINEMENT_BRIEF.md](REFINEMENT_BRIEF.md)** — the diagnosis, the craft layer to copy, per-screen asks, and the constraint block to paste into Codex.

| Fidelity | Screens |
|---|---|
| ✅ **Crafted** — the bar | `Main` · `Recording` · `Understood` |
| ⚠️ **Wireframe** — needs the pass | `Consent` · `Listen` · `Referee` · `Wallet` · `Receipt` · `League` · `Archive` |

## The screens

| # | File | What it settles |
|---|---|---|
| 1 | `Consent.dc.html` | Five **separately declinable** items — one shown off, to prove they're independent. Not a permissions dialog |
| 2 | `Main.dc.html` | The card reveal. The word dominates; banned words as ochre chips |
| 3 | `Recording.dc.html` | 30s ring, live waveform, ambient level feedback — never a modal mid-take |
| 4 | `Listen.dc.html` | Multiple choice (the demo-safe path), 1 replay left, "paid for judging, right or wrong" |
| 5 | `Referee.dc.html` | **The fix that matters** — the listener refereeing the banned-word rule |
| 6 | `Understood.dc.html` | The money moment. Two ticks, waveform turning yellow, R2.00 |
| 7 | `Wallet.dc.html` | Pending / available / paid as distinct states + the EUR sandbox label |
| 8 | `Receipt.dc.html` | Voice Value Receipt — contribution, clarity, coverage, consent, provider ref |
| 9 | `League.dc.html` | Tiered, promotion zone shaded, **no losing state** |
| 10 | `Archive.dc.html` | South Africa as a dot field filling with voices |

## Rules these encode

- **Yellow (`#FFCB05`) appears only where value moves.** It is MTN's colour performing MTN's function; the app's own identity is the ember→magenta voice gradient.
- **A missed guess is ochre, never red.** Not being understood is information, not an error — and red would punish exactly the dialects least represented.
- **Money screens are deliberately boring.** No gradient, tabular numerals, and the wallet never says "paid" before MoMo confirms.
- **Two listeners, not three.** Everywhere.
- **No fake status bar.** The real one renders on top; a painted one looks doubled up.

## ⚠️ Before this goes near a judge

**The card content is placeholder.** `SEFOFANE` / `ISITHUTHUTHU` and their banned words are a best guess and are **not native-checked**. Replace every one — Lethabo on Setswana, Sbu on isiZulu. A wrong word in a language-preservation app is the single most damaging detail available.

## Editing

Working files are the `.dc.html` sources plus `canvas.json`. To change anything: edit the source, re-seed, republish to the same URL.

```bash
node "<design skill base>/seed-canvas.mjs" \
  --template "<design skill base>/payload.template.html" \
  --out amazwi-app-mockups.html --title "AMAZWI App Mockups" \
  --artboard Main.dc.html --artboard Consent.dc.html --artboard Recording.dc.html \
  --artboard Listen.dc.html --artboard Referee.dc.html --artboard Understood.dc.html \
  --artboard Wallet.dc.html --artboard Receipt.dc.html --artboard League.dc.html \
  --artboard Archive.dc.html --canvas canvas.json
```
