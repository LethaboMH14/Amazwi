# AMAZWI — screen mockups

Ten artboards, built from the tokens in [`../../05_amazwi/plan/04_DESIGN.md`](../../05_amazwi/plan/04_DESIGN.md) §2.2.

**Live canvas:** https://claude.ai/code/artifact/889d9d01-823d-4a84-bd00-7d6e88007903

> ⚠️ **NOT FINISHED — three screens are crafted, seven are wireframes.**
> Held against the reference examples these are below the bar: the wireframes have correct structure and content but no depth, material or composition. **Do not put them in front of a judge as they are.**
> **→ [REFINEMENT_BRIEF.md](REFINEMENT_BRIEF.md)** — the diagnosis, the craft layer to copy, per-screen asks, and the constraint block to paste into Codex.

| Fidelity | Screens |
|---|---|
| ✅ **Crafted** — the bar | `Main` · `Recording` · `Understood` |
| ⚠️ **Wireframe** — needs the pass | `Consent` · `Listen` · `Referee` · `Wallet` · `Receipt` · `League` · `Archive` *(source filename retained; screen is now Impact Map)* |

## The screens

| # | File | What it settles |
|---|---|---|
| 1 | `Consent.dc.html` | Five **separately declinable** items — one shown off, to prove they're independent. Not a permissions dialog |
| 2 | `Main.dc.html` | The card reveal. The word dominates; banned words as ochre chips |
| 3 | `Recording.dc.html` | 30s ring, live waveform, ambient level feedback — never a modal mid-take |
| 4 | `Listen.dc.html` | Learner multiple choice, 1 replay left, XP only and explicitly excluded from validation |
| 5 | `Referee.dc.html` | **The fix that matters** — the listener refereeing the banned-word rule |
| 6 | `Understood.dc.html` | The money moment. Two ticks, waveform turning yellow, R2.00 |
| 7 | `Wallet.dc.html` | Pending / available / paid as distinct states + the EUR sandbox label |
| 8 | `Receipt.dc.html` | Voice Value Receipt — semantic label, two verifier events, consent, reward credit and provider mode |
| 9 | `League.dc.html` | Tiered, promotion zone shaded, **no losing state** |
| 10 | `Archive.dc.html` | Aggregate Impact Map; no public raw audio, names or exact location |

## Rules these encode

- **Yellow (`#FFCB05`) appears only where value moves.** It is MTN's colour performing MTN's function; the app's own identity is the ember→magenta voice gradient.
- **A missed guess is ochre, never red.** Not being understood is information, not an error — and red would punish exactly the dialects least represented.
- **Money screens are deliberately boring.** No gradient, tabular numerals, and the wallet never says "paid" before MoMo confirms.
- **Two listeners, not three.** Everywhere.
- **MCQ is learner gameplay only.** Two proficient free-text matches make the governed decision.
- **Listeners/verifiers earn Voice Points, not cash, in the competition build.**
- **The public map is aggregate.** Raw audio and attribution remain private by default.
- **No fake status bar.** The real one renders on top; a painted one looks doubled up.

## Card content status — updated 31 Aug 2026

**`SEFOFANE` is real, not placeholder.** It was a best guess when this README was first written; it is now `sw-001` in `05_amazwi/content/cards_setswana.json`, native-confirmed by Lethabo with the identical target and all four blocked words (`fofa`/`loapi`/`maeto`/`boemafofane`). No change needed on `Main.dc.html`.

**`ISITHUTHUTHU` was a real bug, now fixed.** It appeared in `Listen.dc.html`, `Receipt.dc.html` and `Referee.dc.html` — and `Receipt.dc.html` labelled it `Language: Setswana`, which was simply wrong: `isithuthuthu` carries a Nguni class-7 `isi-` prefix, not a Setswana one, and it was never in either reviewed 8-card deck. Replaced in all three files with `kgomo` (`sw-002`, native-reviewed). If a screen ever needs an isiZulu example instead, pull one of Sbu's eight from `cards_isizulu.json` — never re-guess a word.

**⚠️ `League.dc.html` is not P0.** Per `plan/05_BUILD.md` §6 kill rules, league is the second thing cut if anything must give. It stays in this folder for later, but must not appear in any judge-facing compiled canvas — see the seed command below, which now omits it.

## Editing

Working files are the `.dc.html` sources plus `canvas.json`. The source files reflect the accepted 2026-08-31 product decisions; the bundled `amazwi-app-mockups.html` is stale until re-seeded. Edit the source, re-seed, then republish to the same URL.

```bash
node "<design skill base>/seed-canvas.mjs" \
  --template "<design skill base>/payload.template.html" \
  --out amazwi-app-mockups.html --title "AMAZWI App Mockups" \
  --artboard Main.dc.html --artboard Consent.dc.html --artboard Recording.dc.html \
  --artboard Listen.dc.html --artboard Referee.dc.html --artboard Understood.dc.html \
  --artboard Wallet.dc.html --artboard Receipt.dc.html \
  --artboard Archive.dc.html --canvas canvas.json
```

**`League.dc.html` is deliberately omitted from this command** — see the kill-rule note above. Add it back only if the kill rules are ever revisited, and say so out loud when you do.
