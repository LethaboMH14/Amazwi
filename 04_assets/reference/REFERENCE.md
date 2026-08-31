# Design reference — Lethabo's picks, 31 Aug 2026

**Source:** provided directly by Lethabo, not sourced by Claude. Kept here so Sbu and any mentor sees exactly what the craft bar is aimed at, and so the reasoning for what we take vs. reject is on the record — not just the images.

**Correction, same day:** the file first filed as `dribbble-04-rewards-spin-wheel.png` was moved into this folder without being opened first and was wrongly assumed to be another Dribbble shot. It is actually `amazwi-concept-board-full-app.png` — a full concept board for AMAZWI itself, thirteen screens plus a MoMo-integration mockup and closing tagline. That is a materially different, more important asset than an external reference, so it gets its own full section (00) below, analysed for what to keep vs. what conflicts with decisions already locked in `BUILD_LOG.md`. The real fourth Dribbble example (a food-delivery rewards wheel) is correctly filed as `dribbble-04-rewards-spin-wheel.png` and its analysis (section 04) was accurate all along — only the filename mixup is new.

---

## 00 — `amazwi-concept-board-full-app.png` (the actual AMAZWI vision board, not an external reference)

**What this is:** thirteen numbered screens — onboarding, language select, how-it-works, permissions, ready screen, a "UMLOZI — The Whistle" play mode (describe-without-banned-words, matching our actual mechanic exactly), speak/record, listen & guess, agree/results, wallet, leaderboard, and a public "Archive — Our Living Library" — plus a MoMo-home-screen mockup showing AMAZWI as a Discover tile, and a closing tagline panel with Ndebele beadwork in the corner.

**What's load-bearing and should stay:** the visual identity. The waveform logotype's ember-to-magenta gradient is the same pairing already tokenized as `voice-1-ember`/`voice-2-magenta` in the Figma brand collection — this board and those tokens agree, which means the brand direction has been consistent since before it was formalised, not invented mid-session. The warm-toned portrait photography, dark ground, and the MoMo-Discover-tile integration concept (AMAZWI as a tile inside MoMo's own home screen, not a separate app people have to go find) are all worth carrying forward as-is.

**What conflicts with decisions already made and must NOT be built for P0 — flagged, not silently imported:**
- **Language select lists eight languages** (isiZulu, isiXhosa, Afrikaans, Sesotho, Setswana, Tshivenda, isiNdebele, English). Locked decision: *"Languages: isiZulu + Setswana — one per family, forces the two-model story"* and Slide 9's own "what we did not built" line: *"two quality-assured languages, not twelve."* This board predates that restraint decision; P0 stays at two.
- **The leaderboard shows named individuals next to real rand amounts** ("Nomsa R325.40"). This reads as a public income list, which sits uncomfortably next to the private-by-default posture the project committed to elsewhere, and is a materially different thing from the *"Leagues award points and status only, never prizes"* decision — that decision was about prize money, not about publishing what everyone else earned. If a leaderboard ships at all, it should rank by XP/points, never by rand amount, and never make one contributor's earnings visible to another.
- **The Archive screen is public, with named clips and play counts** ("The Rainmaker · isiXhosa Story Chain · 1.2k plays"). This directly contradicts the recorded decision *"Archive → private-by-default Impact Map, aggregate only"* and Slide 9's *"no public raw-audio archive."* The aggregate Impact Map (Slide 10, still a named placeholder) is the sanctioned version of this idea — anonymous and aggregate, never a named per-person library.

**Why this matters for "avoiding AI slop":** none of the above is an AI-slop problem — the board is genuinely well-produced. The risk here is different and arguably more important: a beautiful concept board is exactly the kind of asset that quietly smuggles pre-restraint scope back into a build if nobody checks it against what was actually decided since. Use it for the identity and the MoMo-integration idea; do not use it as an unstated spec for what screens to build.

---

**Rule these are held to:** professional Dribbble-clean, not "AI slop." AI slop has a recognisable signature — centred hero + soft blob shape, default purple-to-blue gradient, generic rounded-everything with no real hierarchy, Inter at every weight, illustrations that could belong to any product because they belong to none. Every pattern pulled from these four is checked against that signature before it goes anywhere near our components.

---

## 01 — Kuest (gamified learning dashboard)

**What it's doing well:** real information hierarchy — mastery badge and level progress top-left, four colour-blocked mini-game cards each carrying a distinct illustration style (not the same stock character recoloured four times), a leaderboard and daily-quest module that both use progress bars for different things (quest completion vs. rank points) without visually colliding. Sidebar nav is quiet; the colour budget is spent entirely on the game-mode cards.

**What we take, with reason:**
- **One saturated colour per "mode," reserved for that mode only** — matches our own `voice-1-ember` rule (money/CTA-only) but extends it: if we ever surface multiple campaign types (language missions) on one screen, each gets its own accent, not a shared brand gradient repeated four times.
- **Badge-as-status, not badge-as-decoration** — the Master/rank medal sits next to the level number, doing real informational work. Directly applicable to our Wallet-receipt's `UNDERSTOOD — corpus eligible` status dot; a small badge earns its place if it replaces a word, not if it just decorates one.

**What we reject:** the character illustrations. AMAZWI already decided against a mascot-led aesthetic in favour of authentic SA cultural texture (shweshwe pattern, ochre warmth) — copying Kuest's cartoon-avatar language here would be the "any product, no product" AI-slop failure mode, just with better production values.

---

## 02 — Activity/social mobile (fitness challenge app)

**What it's doing well:** the hero activity screen uses a real photo with a dark gradient scrim for text legibility, not a flat colour card — the photo *is* the content, not a background decoration. The segmented pill control (`Going / Not Going / Maybe`) is a single control doing one job clearly. XP and distance are shown as small pill chips near the avatar row, not as competing headline numbers.

**What we take, with reason:**
- **Photo + scrim, not photo + card-on-top-of-photo** — if AMAZWI ever shows a real recorded clip's waveform over a themed background (Theme A ground), the scrim-for-legibility pattern here is the right model, not stacking an opaque card over the art.
- **Segmented pill control for a real three-way state** — directly reusable for the verifier's referee decision (`No violation / Flag / Unsure`, or similar) once Gate E's UI is built. Three genuinely distinct states, one control, no ambiguity about which is selected.

**What we reject:** nothing structurally — this is the strongest reference of the four for restraint. The one caution: its dark-mode contrast is tuned for a lifestyle photo backdrop, not for a text-and-chip-heavy screen like our Card component — don't copy the contrast ratios blind, re-check them against our own actual dark surface tokens.

---

## 03 — Gamified map, 3D isometric ("Los Angeles, CA")

**What it's doing well:** turns a literal geographic map into the game board — XP pins, live-event markers and a floating phone mockup all read as one coherent "world," not a UI screen bolted onto a map widget. The floating pill nav (`Live Now / Social / All Experiences / Events / Challenges`) uses size and colour-weight, not just position, to mark the primary action.

**What we take, with reason — this is the most directly applicable of the four:**
- **AMAZWI already has an aggregate Impact Map planned** (`06_PITCH.md` Slide 10, currently a named placeholder in `plan/14_DECK_SKELETON.md`). This is a legitimate visual precedent: a South African map with per-region pins showing where language contributions are coming from, sized/coloured by contribution volume, is the honest, real version of this pattern — not a fantasy 3D city, an actual outline of SA provinces with real aggregate counts.
- **Pill-shaped filter nav with one visually dominant primary action** — applicable to a future "browse missions by language/region" screen, if that's ever built past P0.

**What we reject:** the 3D isometric rendering style itself. It's expensive to produce authentically (real 3D asset pipeline, not a quick illustration), and a flat, honest SA-outline map with real data communicates the Impact Map's actual point — aggregate, private-by-default, real numbers — better than a stylised fantasy render would. Borrow the *information layout* (map + sized pins + floating stat chip), not the render style.

---

## 04 — Rewards spin-wheel (food delivery app)

**⚠️ Mechanic conflict — flagged, not silently adopted.** This app's core reward mechanic is a spin-to-win wheel. AMAZWI already has a **recorded decision rejecting this** (`BUILD_LOG.md`, 31 Aug: *"No spin-to-win. Fixed-rate credit redemption instead — wagering earned credits supplies the consideration element a free spin lacks, more exposed [to gambling-law risk] not less"*). Nothing here should reopen that decision.

**What we take, with reason — visual craft only, mechanic discarded:**
- **The confetti/celebration state on a win** — genuinely good craft for a moment that matters (a reward becomes real). Our equivalent moment is the Wallet-receipt transitioning from `CORPUS_ELIGIBLE` to a credited state. A brief, tasteful celebration animation on that transition is a legitimate borrow — same emotional beat (something you did just paid off), zero mechanic overlap (no wager, no randomness, the amount was never in doubt).
- **Bold, rounded category icon chips with a solid fill per category** — applicable to a future card-category browser (if/when the 8-card decks expand), not P0.

**What we explicitly do NOT take:** the wheel, the randomised-outcome framing, "Spin Again" as a call to action. Any of these on our reward screen would visually imply chance-based payout, which is exactly the impression the fixed-rate decision was made to avoid.

---

## Where this goes next

These four are referenced, not duplicated — the goal was reasoned extraction, not restyling AMAZWI to look like someone else's app. Concrete follow-ups queued from this pass:
1. A tasteful (non-wheel) celebration micro-interaction on the Wallet-receipt's credited-state transition.
2. The Impact Map, when built, uses a real SA outline + sized pins, not a decorative map.
3. A segmented pill control pattern, reusable for the Gate E referee decision UI.
