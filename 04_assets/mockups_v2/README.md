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

## Theme proof — LETHABO_NEXT_WORK item 5, partial 31 Aug 2026

`ThemeDemo.dc.html` is an isolated source proof that mirrors the three shortlisted token sets and switches them with `data-theme`. Its controls are real semantic buttons and update `aria-pressed` when the source is opened directly.

**Important limit:** the compiled design-canvas wrapper does not execute this interaction reliably, and the proof mirrors values instead of importing the canonical `04_assets/themes/tokens.css`. Item 5 therefore remains partial until the running app imports `tokens.css`, switches themes on a target phone and passes contrast/layout checks. Do not call artboard 7 “LIVE” in front of judges.

Earth and Ink were chosen for the demo because they're the two most divergent grounds (light vs. dark-neutral) — the hardest contrast case, not the easiest. Dusk and Ndebele are not wired into this demo file; per `P0.md`, the final three-theme shortlist is still Sbu's and Lethabo's call after a target-device contrast check, not something to preempt here.

✅ **`SEFOFANE` is real, not placeholder** — it's `sw-001` in `05_amazwi/content/cards_setswana.json`, native-confirmed 31 Aug with the identical target and all four blocked words. No change needed here.
⚠️ The six v2 surfaces still carry local visual values; they are not yet wired to the runtime theme source.
⚠️ The Impact Map is deliberately labelled as seeded demo data, not traction. League is cut and absent.

The compiled canvas is a working board with annotations, not a presentation surface. Use individual verified exports in the deck; never show the overview to judges.

After editing a `.dc.html` source or `canvas.json`, regenerate the checked-in bundle from the local sources:

```bash
node reseed_compiled.mjs
node reseed_compiled.mjs --check
```
