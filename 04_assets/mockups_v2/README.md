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

## Status

| | |
|---|---|
| ✅ V2 | Card reveal · Recording · The money moment |
| ⚠️ Still v1 | Consent · Listen · Referee · Wallet · Receipt · League · Impact Map |

**Do not mix v1 and v2 in front of a judge.** Either bring the remaining seven up, or present these three only.

✅ **`SEFOFANE` is real, not placeholder** — it's `sw-001` in `05_amazwi/content/cards_setswana.json`, native-confirmed 31 Aug with the identical target and all four blocked words. No change needed here.
⚠️ Only `Main.dc.html` carries the theme tweak so far.
⚠️ League and Impact Map are v1 wireframes; League is additionally cut per `plan/05_BUILD.md` §6 kill rules and must not appear in any judge-facing compiled canvas regardless of fidelity.
