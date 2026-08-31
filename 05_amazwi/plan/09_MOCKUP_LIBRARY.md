# AMAZWI — MOCKUP LIBRARY
### Thirteen references, critiqued · what to take from each · nothing here is settled

**Parent:** `04_DESIGN.md` · **Written:** 2026-08-31

> **Nothing in this document is the brand.** Every item below — including the AMAZWI concept board — is a **reference**, judged on its merits and stripped for parts. The final design is assembled from the best of all of them, not chosen from among them.
>
> Each entry is graded on: **texture · shape · smoothness · colour · professionalism · style · feel · completeness · uniqueness**, then: what is impressive, what is not, what we take, and what we would add.

---

# PART ONE — THE FIVE SUPPLIED REFERENCES

---

## ① KUEST — gamified learning dashboard
*Light, dense, three-column desktop. Quiz platform with duels, leagues and mini-games.*

| | |
|---|---|
| **Texture** | Flat. No grain, no depth, no material. Custom vector illustration doing all the work |
| **Shape** | Soft rectangles, 12–16px radii, circular avatars, pill buttons. Very consistent |
| **Smoothness** | High. Nothing jars. Spacing rhythm is disciplined |
| **Colour** | ⚠️ **Its weakest axis.** Teal brand, then pink/orange/blue/purple game cards with no systematic logic — variety for its own sake |
| **Professionalism** | High. This is a real product, not a portfolio piece |
| **Style** | Friendly corporate SaaS. Duolingo-adjacent but calmer |
| **Feel** | Busy, capable, slightly impersonal |
| **Completeness** | ⭐ **The best in the set.** A real information architecture — nav, main, social rail — not a hero shot |
| **Uniqueness** | Low. Culturally neutral. Could be any country |

**What is impressive**
- **It solves the hardest screen we have not designed.** The right rail — duel invitations with inline Accept/Decline, then a friend list with rank badges and a one-tap challenge — is almost exactly AMAZWI's missing social layer.
- **The rank system is properly built.** Grand Master / Master / Expert / Veteran / Amateur / Beginner, each with a distinct badge. Legible hierarchy without text.
- **The daily-quest row** where the progress bar *is* the row, with Claim Reward inline. No separate screen, no modal.
- **Player counts as social proof** — *"742 Playing"* on each game card. One number that makes a static tile feel alive.
- **The performance radar** (Teamwork / Solving / Discipline / Curiosity / Creative). A genuinely non-obvious way to show ability that isn't another bar chart.

**What is not**
- **Desktop-first.** We are a single column at 480px inside a WebView. Almost none of this layout transfers — only its patterns.
- **Nine modules competing.** No single dominant action. Our home screen needs one.
- **The colour has no argument.** Four game cards, four unrelated hues.
- **The GO PRO upsell** is visually loud and tonally wrong for us.
- **The radar is probably not actionable** — beautiful, but what does a player *do* with it?
- **Avatars look generated.** Same trap as our own board.

**What we take**
Duel invitation → *"Nomsa challenged you to guess"* · the rank badge system for league tiers · the quest row with inline claim · the podium · **player counts** → *"41 people are listening right now"*.
**And the radar, repurposed:** not a personality chart — a **language coverage radar on the Impact Console** (isiZulu / isiXhosa / Sesotho / Tshivenda / Afrikaans by validated hours). That turns a decorative idea into the buyer's most important screen.

**What we would add**
Weight. One dominant action. And a reason for every colour.

---

## ② THE AMAZWI CONCEPT BOARD — our own
*Dark cinematic, ember waveform, 13 phone frames, African portraiture.*

| | |
|---|---|
| **Texture** | Rich — glow, gradient, grain in the photography. The most tactile in the set |
| **Shape** | Uniform rounded phone frames in a grid. ⚠️ Repetitive: 13 identical rectangles |
| **Smoothness** | High within frames. The grid itself is mechanical |
| **Colour** | ⭐ **Best in the set.** Near-black + ember + one magenta. Genuine restraint, and the accent means something |
| **Professionalism** | High. Does not look like a hackathon project |
| **Style** | Cinematic, premium, reverent |
| **Feel** | ⚠️ **Solemn. And that is a real problem** — see below |
| **Completeness** | ⚠️ Low. Thirteen hero states. No empty, loading, error, offline, waiting or revoked states |
| **Uniqueness** | High as a poster. Lower as a product |

**What is impressive**
- **Colour discipline no other reference here matches.** One ground, one accent, one highlight, and the accent earns its use.
- **The waveform as identity** — repeated across screens as the subject, not as ornament.
- **The MoMo integration panel.** Strategically the smartest single frame: it answers *"is this really a mini app?"* before anyone asks.
- **"Built for South Africa"** — <200KB, works offline, real rewards, privacy first. Constraints reframed as promises. That is a design *argument*, not a decoration.
- **The closing line.** *"ONE VOICE. EVERY LANGUAGE. LIMITLESS IMPACT."*

**What is not — and one of these is serious**
- 🔴 **The tone is wrong for the product.** This looks like a documentary about language loss. **AMAZWI is a party game.** Nothing on this board is *fun* — no laughter, no rivalry, no speed, no mess. The tonal gap between "reverent heritage archive" and "describe *ibhasi* in thirty seconds without saying *imoto*" is the single biggest thing to fix. Reverence belongs in the Archive; the game needs to feel like a Friday night.
- 🔴 **The imagery is AI-generated and it reads as such.** The face paint is a generic pan-African pastiche tied to no actual culture; the campfire is a cliché. In a room of South African judges this signals outsider-made. Fine on a concept board — **never in-product, and never on a slide as though it were documentary.**
- **It is a poster, not a product.** Every frame is a best case.
- **Dark-only.** Unusable in South African sun. The Day theme is not optional.
- **Low information density.** Real screens carry more than one idea.
- **The beadwork is trim, not a system** — a decorative strip in a corner rather than structure.
- **No motion is expressed**, in a product whose entire signature is motion.

**What we take**
The palette logic · the waveform as subject · the MoMo panel · the constraints-as-features footer · the premium confidence.

**What we would add**
**Joy.** Faces mid-laugh, not mid-contemplation. Speed, timers, near-misses, someone getting it wrong and finding it funny. And the states that prove it is real software.

---

## ③ FITNESS SOCIAL — light glassmorphic iOS
*Frosted panels, soft blue-white, floating tab bar, activity feed and messages.*

| | |
|---|---|
| **Texture** | Translucent frost, soft diffuse shadow. Airy, physical-adjacent |
| **Shape** | Large radii (20px+), pill controls, floating rounded bars |
| **Smoothness** | ⭐ **Best in the set.** Nothing is sharp. Everything settles |
| **Colour** | Cool blue-white monochrome, one blue accent. Calm but characterless |
| **Professionalism** | ⭐ **Highest craft of the five.** This looks genuinely shipped |
| **Style** | Contemporary iOS, glassmorphic |
| **Feel** | Calm, clean, premium, forgettable |
| **Completeness** | Good — feed, detail and messages form a coherent set |
| **Uniqueness** | ⚠️ **Lowest in the set.** Could be any of four hundred apps |

**What is impressive**
- **The floating tab bar with a raised centre action.** The best navigation pattern here, and directly reusable: centre becomes `[ PLAY ]`.
- **Feed cards with an inline action** — *"Try Challenge"*, *"Join Event"* — plus an engagement row. The card *does* something without navigating.
- **Metadata chips** — `1.2km away · 30–45 mins · +120 XP · Morning Starter`. Dense, scannable, no labels needed.
- **"Challenge a Rival · 10 coins"** — an economy touch that costs one row.
- **Going / Not Going / Maybe** as a three-way segmented control.
- **The messages screen** is textbook: avatar, name, preview, timestamp, read state. Nothing wasted.

**What is not**
- **No identity whatsoever.** Strip the photos and nothing remains.
- **Glassmorphism is a 2021–23 trend and it is dating.** It is also expensive: `backdrop-filter: blur()` is a real cost on mid-range Android.
- **Stock-feeling photography**, and the feed images look artefacted.
- Cool blue is the wrong temperature for South African light (`04_DESIGN.md` §2.2).

**What we take**
Floating tab bar with raised Play · feed card with inline action → Archive entries with *"Guess this"* · metadata chips → `isiXhosa · 30s · R2.00 · coverage bonus` · the three-way segmented control → **the referee tap** · the message-list craft for notifications.

**What we would add**
Character. And **fake the frost with a flat translucent fill** — visually identical at these sizes, and free.

---

## ④ ISOMETRIC MAP — 3D playful world
*Low-poly city, floating clouds, stacked pill filters, XP pinned to the map.*

| | |
|---|---|
| **Texture** | ⭐ **Richest in the set.** Real dimensionality — layered shadow, volume, atmosphere |
| **Shape** | Isometric solids, floating pills, soft organic clouds |
| **Smoothness** | Very high, almost buttery |
| **Colour** | Pastel sky-blue, mint, coral. Cheerful, cohesive, ⚠️ culturally generic |
| **Professionalism** | High craft, but reads as *concept* rather than *shipped* |
| **Style** | Toy-like, playful, game-adjacent |
| **Feel** | Inviting, light, fun — **the most fun in the set** |
| **Completeness** | Low. One screen family, no supporting states |
| **Uniqueness** | ⭐ **Highest in the set.** Nobody at that hackathon will show anything like it |

**What is impressive**
- **It is the only reference here that is genuinely, structurally different.** Everything else is a list, a card or a feed. This is a *place*.
- **The floating stacked pill filter** — All Experiences / Events / Challenges / Social / Live Now — a distinctive nav pattern that costs almost nothing in CSS.
- **XP printed on the map itself** (`2xp`, `5xp`) — geography made rewarding. Directly translatable: **show where South Africa needs voices, as a map.**
- **Depth without literal 3D.** Most of the effect is layered shadow and scale, not geometry.
- **Contextual header** — location, weather, XP, avatar.

**What is not**
- **Expensive.** Real 3D assets and map rendering blow the 200 KB budget many times over.
- **Toy-like risks the fintech argument.** We are asking to be taken seriously about a ledger.
- 🔴 **Location-based, and we deliberately do not collect precise location** (POPIA — `02_TECH.md` §7.1). Any map we build is **province or ward band only.**
- Pastel clouds are Northern-hemisphere-generic.

**What we take**
The **Archive as a place, not a list** — a map of South Africa filling with voices, dots at province level. The floating pill filter. XP-on-map → **coverage need shown geographically**, which makes "where the data gap is" instantly legible.
⚠️ **Build it as animated SVG, not Three.js.** `04_DESIGN.md` §3.3 caps the one WebGL moment at 60 KB with an SVG fallback — and honestly the SVG will read better and load instantly.

**What we would add**
Replace the generic city with **actual South African geography**, and replace clouds with something ours.

---

## ⑤ SPIN TO WIN — bold flat rewards
*Black/green/purple/yellow, confetti, prize wheel, heavy display type.*

| | |
|---|---|
| **Texture** | Flat, hard-edged, zero depth. Poster-like |
| **Shape** | Chunky rounded rectangles, a big circle, thick strokes |
| **Smoothness** | ⚠️ **Lowest in the set.** Deliberately abrupt and loud |
| **Colour** | Black + acid green + purple + yellow. Unusual, memorable, ⚠️ hard to control |
| **Professionalism** | ⚠️ Mixed. Confident, but reads slightly cheap — discount-app energy |
| **Style** | Bold flat, near-brutalist |
| **Feel** | ⭐ **Loudest and most joyful in the set** |
| **Completeness** | Low. Two screens |
| **Uniqueness** | Medium. The palette is distinctive; the wheel is a cliché |

**What is impressive**
- **It is the only reference that expresses joy**, and joy is exactly what our own board is missing. The win state genuinely feels like winning.
- **Big-type numerals.** *"20% off"* at display size. Our reward moment should do this with **R2.00**.
- **Confetti as celebration** — trivially reproducible as a CSS particle burst, no Lottie.
- **The card carousel with the next card peeking** — a good pattern for game-mode selection.
- **Black ground with acid accents** proves a dark UI can be energetic rather than solemn. **This is the direct answer to reference ②'s tone problem.**

**What is not**
- 🔴 **The core mechanic is gambling.** Spin-to-win is chance-based, and `07_TRUTH.md` §4.3 excludes every randomised-prize mechanic deliberately — it is a live question under South Africa's Lotteries and National Gambling Acts, and our reward being **deterministic and skill-based** is a legal position worth protecting. **Take the energy. Never take the wheel.**
- **Visually undisciplined.** Four strong colours fighting.
- **Tonally inconsistent** — home and win screens feel like different products.

**What we take**
The **celebration energy**, transplanted onto our palette · display-size numerals for the reward · CSS confetti · the peeking card carousel · and the proof that *dark can be fun*.

**What we would add**
Restraint, and a reward that is earned rather than spun.

---

# PART TWO — EIGHT MORE, TO COVER WHAT THE FIVE DO NOT

The five above are all **flat, digital and screen-native**. None uses real texture, real photography, real material, or heavy typography. These eight fill the gaps.

---

## ⑥ EDITORIAL DOCUMENTARY — real photography
**Texture** photographic grain · **Shape** full-bleed, hard-cropped · **Colour** whatever the image gives · **Feel** true, weighty, human · **Uniqueness** high, because almost no hackathon entry does it

Full-bleed real photographs of actual South Africans, one line of type, magazine restraint. **This is the direct fix for reference ②'s AI-imagery problem.**
**Use for** Archive story covers, the elder/Imbewu mode, deck openers.
**Reference** Airbnb listings, Apple Fitness+; editorially, South African documentary photography.
🔴 **Never AI-generate South African people.** Licensed photography, or photograph each other. Two people, a phone, an afternoon — and it will be more convincing than anything a model produces.

---

## ⑦ TEXTILE & BEADWORK — pattern as structure
**Texture** ⭐ woven, beaded, material — the only genuinely *tactile* direction here · **Shape** hard geometry, repeating units · **Colour** high-chroma primaries on black · **Uniqueness** ⭐ highest available to us

Ndebele geometry and Zulu beadwork used as **structure** — a divider, a progress bar, a badge frame, a loading state — rather than as a border. Reference ② has beadwork as trim in one corner; this makes it the system.
**Use for** Heritage season, league badges, achievements, empty states, dividers.
Repeatable in pure CSS gradients at near-zero payload. **Highest distinctiveness per kilobyte on the entire list.**
⚠️ If you use Ndebele geometry, **say it is Ndebele.** Attribution is the whole difference between homage and appropriation, and it costs one caption.

---

## ⑧ BRUTALIST TYPE — the card reveal
**Texture** none, deliberately · **Shape** hard rectangles, offset shadows, thick borders · **Smoothness** low, on purpose · **Feel** loud, confident, unmissable

The target word at 56px+, banned words as hard-bordered chips beneath, zero ornament.
**Use for** the card reveal — **the single most important screen in the game**, and the screenshot that goes on the slide.
**Reference** Gumroad's redesign, Duolingo's lesson-complete screens.
Very low effort, highest impact-per-hour on this list. **Use nowhere else** — brutalism across a whole app reads as unfinished.

---

## ⑨ FINANCIAL MINIMAL — the trust surfaces
**Texture** none · **Shape** rules and rows · **Colour** one accent on neutral · **Feel** precise, quiet, credible · **Completeness** ⭐ what this direction is *for*

Tabular numerals, state chips (pending / available / paid), a receipt that reads like a document.
**Use for** wallet, Voice Value Receipt, consent, privacy, transaction history.
**Reference** Revolut statements, Wise, Stripe receipts, Apple Wallet.
**Money screens must be boring.** A celebratory wallet undermines the exact credibility the receipt exists to build — in front of a fintech panel.

---

## ⑩ MOTION-LED WAVEFORM — the signature
**Texture** light and glow · **Shape** organic, amplitude-driven · **Smoothness** ⭐ the whole point · **Uniqueness** ours

The interface is still; the voice is the only living thing. Real amplitude from `AnalyserNode` at 30fps. The recorded waveform **collapses and flies to the wallet**, becoming yellow as it lands.
**Use for** recording, playback, the understanding moment, the Archive bloom.
**Reference** Apple Voice Memos, Otter; for the transformation, Apple Pay's card-to-checkmark.
🔴 **Never fake a waveform with `Math.random()`.** People can tell, and in a product about listening it is self-defeating. **Non-negotiable — this is the brand.** `04_DESIGN.md` §3.2

---

## ⑪ TACTILE CARD GAME — the physical metaphor
**Texture** paper, subtle grain, soft shadow · **Shape** card stacks, slight rotation · **Feel** familiar, physical, playful

Cards that stack, flip and deal. CSS 3D `rotateY`, a stacked-deck affordance, a tilt on press.
**Use for** card reveal, mode selection, the deck of quests.
**Reference** Arc's card switcher, Apple Wallet's stack — and the physical board game the whole mechanic comes from.
Free, GPU-composited, zero dependency. ⚠️ Avoid swipe-to-dismiss as primary input — it fights the MoMo WebView's own gestures.

---

## ⑫ CLAYMORPHIC 3D OBJECTS — soft rendered props
**Texture** ⭐ soft matte clay, rounded volume · **Shape** chunky, friendly, exaggerated · **Feel** warm, approachable, modern-playful

Soft-rendered 3D objects — a whistle, a microphone, a coin, a bead — as icons and empty-state art. **Different texture from ④'s isometric world**: objects, not environments, so each is one small asset instead of a scene.
**Use for** mode icons, achievements, empty states, the reward object.
**Reference** the current Spline/Blender-clay aesthetic; Duolingo's 3D era.
Pre-render to AVIF at ≤12 KB each. **A far cheaper way to get depth than a 3D engine.**

---

## ⑬ CONSOLE / DATA-VIZ — the Impact Console
**Texture** none · **Shape** dense grid, sparklines, heat map · **Feel** instrumented, serious, tool-like

Monospaced numerals, coverage heat map by language × quest type, cost-per-validated-minute as a headline stat, "next recommended language" as the call to action.
**Use for** the MTN-facing console **only**.
**Reference** Vercel, Linear, Stripe dashboards, Grafana.
**This screen should look like a tool, not a product.** The tonal shift *is* the point — it signals we understand there are two audiences. Directly scored under Feasibility & Scalability.

---

# PART THREE — ASSEMBLY

## Which direction for which screen

| Screen | Directions |
|---|---|
| Splash · onboarding · language | ② palette + ⑥ real photography |
| Consent | ⑨ financial minimal |
| Home / Today | ② ground + ① modules + ⑫ icons |
| **Card reveal** | **⑧ brutalist type + ⑪ card flip** |
| **Recording** | **⑩ motion waveform** |
| Listen · guess · referee tap | ③ segmented control + ② ground |
| **Understanding moment** | **⑤ celebration energy + ⑩ waveform-to-wallet** |
| **Wallet · receipt** | **⑨ financial minimal** |
| Leaderboard · friends · quests | ① kuest patterns, single-column |
| **Archive** | **④ map-as-place (SVG) + ⑥ photographic covers** |
| Heritage · badges · empty states | ⑦ beadwork + ⑫ clay objects |
| Notifications | ③ message-list craft |
| **Impact Console** | **⑬ console + ① radar as coverage chart** |
| Errors · empty · offline | ⑨, always |

## The rule that keeps thirteen references producing one app
> **Borrow structure and behaviour. Never borrow colour or typeface.**

Every direction is executed in the tokens from `04_DESIGN.md` §2.2 — same palette, same type, same radii, same motion curves. That single constraint is the difference between a design system and a scrapbook. And the 200 KB budget still binds: anything needing a heavy library gets rebuilt in CSS or dropped.

## The three biggest gaps across all thirteen
1. **None of them is funny.** Our product's best moment is someone failing to describe *ibhasi* and the room laughing. No reference here expresses that, and it is the thing that proves Track 2.
2. **None of them is South African** except ⑦ and our own — and ours is generically African rather than specifically South African. **Ndebele geometry, Kaaps, a Joburg skyline, a taxi rank, a specific place** beats "Africa" every time.
3. **None of them shows a failure state**, and the states are where judges look.

## Priority — you have two days
Design these five, in this order. Everything else needs only to be clean, correct and on-token.

1. **The card reveal** (⑧ + ⑪) — the slide screenshot
2. **Recording** (⑩) — the product's portrait
3. **The understanding moment** (⑤ + ⑩) — the emotional peak
4. **The Voice Value Receipt** (⑨) — the credibility screen
5. **The Archive** (④ + ⑥) — the closing image

## Sourcing real references
**Mobbin** *(45 minutes, highest value)* — search `daily streak` · `leaderboard` · `wallet transaction states` · `voice recording` · `reward claim` · `empty state`. Open **Duolingo**, **Cash App**, **Revolut**, **Strava**, and **Gojek/Grab** (mini apps inside a super app — directly relevant, and almost nobody looks at them).
**Dribbble** *(20 minutes, colour and type only, then close it)* — `dark fintech ui` · `voice app interface` · `african pattern ui`. ⚠️ Dribbble designs have no error states and do not survive a real isiXhosa word at 56px. **Never copy a layout from it.**
**For the deck:** screenshot the **real running app** with realistic seed data. Nothing drawn beats it, and judges can tell.
