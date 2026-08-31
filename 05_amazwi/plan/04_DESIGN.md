# AMAZWI — DESIGN SYSTEM
### Visual identity · motion · sound · 3D · the mockup pipeline

**Parent:** `00_MASTER_PLAN.md` · **Written:** 2026-08-30 · **Owner:** the EXPERIENCE role (see `05_BUILD.md` §3)

---

## 1. THE DESIGN THESIS

Two constraints define everything, and they point the same way.

**Constraint one — it lives inside someone else's app.** AMAZWI renders inside the MoMo shell. A mini app that fights the host looks broken. A mini app that dissolves into the host has no identity. The resolution is a deliberate division of colour: **MTN Sunshine Yellow is reserved for money.** It is not the app's brand colour; it is the colour that appears the moment value moves. The host's colour performs the host's function.

**Constraint two — data costs money, and this is an income product.** An app that costs R5 of data to earn R4 is not an income product; it is a con. So:

> ### The whole app must be beautiful at 200 KB.

This is not a technical compromise dressed as a principle. It is the strongest design story in the entry, and it is a sentence for the stage:

> *"Our entire interface is smaller than one photograph. In a country where a gigabyte costs what it costs, that is a design decision, not a technical one."*

Everything below follows from that. No web fonts over 40 KB. No Lottie library. No Three.js as a dependency. **One** hero moment in WebGL, or none. Beauty from typography, colour, timing and restraint — which is how good design worked before bundles got fat.

---

## 2. VISUAL IDENTITY

### 2.1 The idea
**Make the voice and trust visible.** The live waveform remains AMAZWI's brand signature: it is drawn from *real amplitude data* via the Web Audio API `AnalyserNode`, so what the user sees is literally their own voice. The second, product-specific device is the overlap of two listener circles. It appears only where two independent listeners are waiting or agreeing, so it explains the trust mechanic rather than decorating the interface. When a clip is understood, the waveform resolves into the reward while the two circles lock. Meaning is carried by motion and state, not by extra copy.

### 2.2 Palette

Warm neutrals, not blue-greys — South African light is warm and blue-grey reads as European SaaS.

```
━━ CORE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
--ink            #14100E   near-black, warm      text, dark ground
--ink-2          #2A231F   raised surfaces
--sand           #FAF6F1   warm off-white        light ground
--sand-2         #EFE7DC   cards on light

━━ VOICE (the app's own identity) ━━━━━━━━━━━━━━━━━━━━━━━━━━━
--voice-1        #FF5A36   ember orange          waveform low
--voice-2        #E8267F   magenta               waveform high
   gradient: linear-gradient(96deg, #FF5A36, #E8267F)
   Used for live voice and the single primary action that advances that voice flow.
   Never use it as passive chrome or decoration.

━━ MONEY (borrowed, never repurposed) ━━━━━━━━━━━━━━━━━━━━━━━
--rand           #FFCB05   MTN Sunshine Yellow
   Used ONLY where value moves: reward chips, the payout moment,
   the wallet's Available state. Nothing decorative is yellow.

━━ SIGNAL ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
--understood     #1F8A54   aloe green            "they got it"
--missed         #8A6A1F   ochre, not red        "they didn't"
--danger         #C0341A   destructive only
--calm           #4C6FA5   info, consent, privacy
```

**One decision worth defending out loud:** a failed guess is **ochre, not red**. Not being understood is not an error and must never look like one — it is information about a hard word or a new listener. Red here would punish exactly the speakers whose dialects are least represented, which is the opposite of the product's purpose.

### 2.3 Themes
Three, all built from the same tokens:
- **Night** (default) — `--ink` ground. OLED-cheap, makes the waveform glow, reads as premium.
- **Day** — `--sand` ground. Mandatory: this app is used outdoors in hard South African sunlight where dark UI is unreadable. Contrast targets are set for direct sun, not for a desk.
- **Heritage** (seasonal, September) — Night with beadwork-derived accents. Seasonal skins are a retention mechanic that costs nothing but CSS.

Implement as CSS custom properties on `:root`, with `prefers-color-scheme` honoured and an explicit user override that wins in both directions.

### 2.4 Typography

| Role | Face | Why |
|---|---|---|
| Display | **Archivo Expanded** or **Anton** | Wide, confident, poster-like. Carries the card word at 56px+ with no decoration needed. |
| Body / UI | **Inter** (variable, subset) | Excellent at small sizes, complete Latin Extended coverage. |
| Numerals | Inter **tabular** figures | Money and timers must not shift width while counting. Non-negotiable. |

**Subset ruthlessly.** Latin + the specific diacritics South African orthographies use. Self-host WOFF2. Budget: **≤ 40 KB total for all faces.** If that cannot be met, drop the display face and set the card word in Inter at heavy weight — a missing typeface is invisible; a 300 KB font is not.

**Orthographic correctness is a hard requirement.** Test every language's characters before shipping: Tshivenda (ḓ ṱ ṋ ḽ), Sepedi/Northern Sotho (š ê ô), Afrikaans (ê ë ï ô û á é í ó ú), and the Khoisan click letters (ǀ ǁ ǂ ǃ) which are **not** apostrophes or exclamation marks and will render as tofu in most fonts. Getting a click character wrong in a language-preservation app is the kind of detail a South African judge will spot and never forget.

### 2.5 Layout
4px base grid, 8px rhythm. Single column, max 480px, centred. Thumb-zone rule: the primary action lives in the bottom third — the recording button, the answer field, and `[ PLAY ]` are all reachable one-handed on a 6.5" phone. Corner radius 16px on cards, 999px on pills. Use a restrained three-step elevation system (ground, raised decision surface, focal/reward surface); shadows communicate hierarchy and must never become decoration.

---

## 3. MOTION

### 3.1 Principles
1. **Motion explains state; it never entertains.** Every animation answers *what just changed* or *where did that go*.
2. **Fast in, slow out.** Entrances 180–220ms, exits 120ms, `cubic-bezier(0.2, 0, 0, 1)`.
3. **The voice is the only thing that moves continuously.** Everything else is still until it changes.
4. **Honour `prefers-reduced-motion`.** Every animation has a static equivalent.
5. **60fps on a mid-range Android, or it does not ship.** Transform and opacity only. Never animate layout.

### 3.2 The five animations that matter

**① THE TIMER RING** — the hero
A 30-second SVG ring depleting via `stroke-dashoffset`. It shifts from `--voice-1` toward `--voice-2` as time runs out, and at 5 seconds begins a slow breathing pulse. No numbers, no beeping. The whole state of the round is legible peripherally while the player concentrates on talking.

**② THE LIVE WAVEFORM**
Real amplitude from `AnalyserNode`, drawn to a single canvas at 30fps (not 60 — halves the battery cost and is visually identical for this). Bars mirror around a centre line. Too quiet: bars desaturate and a soft *"speak up"* appears. Clipping: the peaks flash `--danger` briefly. **The feedback must be ambient, never modal** — a dialog mid-recording destroys the take.

**③ THE CARD FLIP** — the reveal
CSS 3D `rotateY` on the card, 320ms. Used at card reveal and at answer reveal. Pure CSS, zero payload, and it reads as tactile in a way nothing else this cheap does.

**④ THE UNDERSTANDING MOMENT** — the emotional peak
When results land: the two proficient-verifier avatars resolve one at a time, 120ms apart. Each matched answer lights `--understood`. Then the player's own waveform — *the actual shape of what they said* — collapses inward and travels to the wallet chip, where it becomes `--rand` yellow and the credited balance counts up.

That is the entire product in one 900ms sequence: **your voice became money because people understood you.** Build this one properly; it is what the judges will remember and it is what gets screenshotted.

**⑤ THE IMPACT BLOOM**
When a contribution becomes eligible, an aggregate point appears on the South Africa map and ripples outward once. It represents a non-identifying count, never a public raw recording or named person. The counter increments. This is the only animation allowed to feel ceremonial.

### 3.3 3D — spend it once
Heavy 3D contradicts the 200 KB principle and is a trap at this scale. Two decisions:

- **CSS 3D everywhere** — card flips, tilts, depth. Free, GPU-composited, no dependency.
- **One optional WebGL moment: the Impact Map.** A slowly rotating point-cloud of South Africa built from coarse aggregate counts, hand-written WebGL or a Three.js subset, **lazy-loaded only when the Impact Map is opened**, hard-capped at 60 KB gzipped, with a static SVG map fallback.

If time is short, **cut the WebGL and keep the SVG.** A beautiful flat map that loads instantly beats a 3D globe that stutters, and it is more consistent with what the product says about itself.

---

## 4. SOUND

This is a voice product. Sound is the medium, not the garnish — and it is the most under-used differentiator available. Almost no hackathon entry has considered audio at all.

### 4.1 Rules
- **Everything must work with sound off.** People play on taxis and in queues. Every audio cue has a visual twin.
- **Sounds are human and acoustic, never synthetic UI blips.** This is an app about human voices; a generic notification chime would undercut it.
- **Total audio budget ≤ 60 KB**, all assets Opus-encoded, lazy-loaded after first interaction.
- Respect the OS silent switch and duck under any active media.

### 4.2 The palette
| Event | Sound | Note |
|---|---|---|
| **Sonic logo** | Three sung notes, real human voices, ~800ms | Plays once at first open. Recorded by the team, not licensed. |
| **Countdown 3·2·1** | Single soft marimba note, rising in pitch | Marimba is Southern African without being a cliché, and cuts through phone speakers |
| **Recording starts** | Low warm thud | Physical, like a mic being switched on |
| **Time warning (5s)** | Same marimba, quieter, slow pulse | Never alarming |
| **Understood** | Rising pentatonic three-note figure | Pentatonic = culturally broad and universally consonant |
| **Not understood** | One low, warm, *neutral* note | Must not sound like failure. This is the single most important sound in the app. |
| **Money lands** | Soft mbira pluck + a physical coin-settle | The only sound tied to `--rand` |
| **Impact-map increment** | Distant single voice hum, reverberant | Ceremonial. Used sparingly. |

**Record these yourselves.** Two people, a phone, a quiet room, forty minutes. A product about South African voices whose interface sounds like a stock library has a hole in the middle of it — and "we recorded our own sound design" is a line worth having.

### 4.3 Accessibility
Full captioning of every spoken instruction. Haptics mirror the audio cues (`navigator.vibrate`) for the recording start, the 5-second warning and the result. Never rely on colour alone for understood/missed — pair with an icon and a word.

---

## 5. THE MOCKUP AND BUILD PIPELINE

You asked about Figma, Lovable, GPT/nano-banana, Dribbble and Mobbin. Here is what each is genuinely good for, in the order to use them, with the traps.

### 5.1 The governing decision
> **Do not design in Figma and then rebuild in code. You have three days. Design *in* code, and use Figma only for the deck.**

Pixel-perfect Figma files are for teams handing off to other teams. You are two people who will build the thing you draw. Every hour spent making a Figma file match a React component is an hour not spent on the React component. **The screenshots in your pitch deck should be photographs of the real running app** — nothing looks as convincing, and judges can tell.

### 5.2 The pipeline

**STEP 1 · Mobbin — 45 minutes, flows only**
Real screenshots of real shipped apps, organised by flow. Study specifically:
- **Duolingo** — the lesson loop, streak screen, league table. The most-studied gamified learning UI in existence.
- **Cash App / Revolut** — money-state clarity. Steal how they distinguish pending from settled.
- **Gojek / Grab / Alipay mini programs** — how a mini app behaves inside a super-app shell. Directly relevant and almost nobody looks at it.
- **HQ Trivia / Kahoot** — timed-round pressure UI.

Take patterns, not pixels. Output: a one-page flow sketch.

**STEP 2 · Dribbble — 20 minutes, colour and type only, then close it**
⚠️ **The trap:** Dribbble rewards images, not interfaces. Dribbble designs have no empty states, no errors, no long strings, no bad connections, and they do not survive a real isiXhosa word at 56px. Use it for palette and typographic confidence. Never copy a layout from it.

**STEP 3 · Tokens in code — 1 hour**
Write `tokens.css` with §2's custom properties before drawing a single screen. Colour, type scale, spacing, radii, motion curves, and the three themes. Every component consumes tokens. This single file is what makes the app look designed rather than assembled, and it is what lets you re-skin for Heritage Season in ten minutes.

**STEP 4 · Lovable / v0 — scaffolding only, 2 hours**
Generate the static component skeletons: card, timer ring, waveform canvas, wallet row, league table, receipt. Then **take ownership of the code** and hand-tune against your tokens. Do not let generated code define your architecture; it will produce a plausible-looking app with no state model, and you will spend longer untangling it than writing it. Generate leaves, not the trunk.

**STEP 5 · Image models (Nano Banana / GPT Image) — assets, not UI**
Use them for what they are actually good at:
- Card illustrations for concrete nouns — a taxi, a kettle, a soccer ball, a spaza shop — in one consistent flat style, generated as a batch with a locked style prompt
- Impact Map and future-mode artwork
- Empty-state illustration
- Textures and pattern fills for the Heritage theme
- Deck backgrounds

⚠️ **Two hard rules.** Never generate UI layouts — you get uncanny non-functional interfaces. And **never generate images of South African people**: image models render an averaged, subtly wrong idea of who South Africans are, and a room of South African judges will feel it before they can articulate it. Use illustration, typography and real photography you have rights to.

**STEP 6 · Figma — the deck, and only the deck**
Build the pitch slides and the architecture diagram. Import real screenshots. Two hours, near the end, not the beginning.

**STEP 7 · The screenshot pass — 45 minutes before the deadline**
Seed the database with realistic data — real language names, plausible ward names, sensible numbers — and capture every hero screen at 2× on a real device frame. An app screenshotted with `test user 1` and `R0.00` looks unfinished no matter how good the code is.

### 5.3 Asset budget
| Asset | Budget |
|---|---|
| Fonts (subset WOFF2) | 40 KB |
| CSS (tokens + all components) | 25 KB |
| JS (app, gzipped) | 110 KB |
| SVG icons (inline sprite) | 8 KB |
| Card illustrations | lazy, ≤ 12 KB each, AVIF |
| Audio | 60 KB, lazy after first interaction |
| **First meaningful paint** | **≤ 200 KB** |

Put a size badge in your CI output and show it on the architecture slide. *"Our bundle is 187 KB"* is a claim you can prove in ten seconds, and it says more about engineering discipline than any list of technologies.

---

## 5.4 → SEE ALSO: `09_MOCKUP_LIBRARY.md`

Twelve reference directions, mapped screen by screen, plus a **review of the existing AMAZWI concept board with six corrections it needs** before it goes in front of judges — including the two-listener change and the referee tap, neither of which the board currently shows.

---

## 6. THE FIVE SCREENS THAT MUST BE PERFECT

Judges will remember five screens. Everything else needs only to be clean and correct.

1. **The card reveal** — the word huge, banned words beneath, reward chip in yellow, timer poised. This is the screenshot that goes on the slide.
2. **Recording in progress** — the ring depleting, the waveform alive in ember-to-magenta. This is the product's portrait.
3. **The understanding moment** — two avatars resolving, the waveform flying to the credited wallet balance. This is the emotional peak.
4. **The Voice Value Receipt** — dense, honest, legible. This is the credibility screen: entertainment, payment traceability, data value and consent, all provable on one surface.
5. **The Impact Map** — the country filling with aggregate, non-identifying contribution signals. This is the closing image.

---

## 7. COPY AND TONE

- **Short, warm, direct, second person.** *"Waiting for two proficient listeners."* Not *"Your submission has been queued for validation."*
- **Never say "data", "corpus", "annotation", "task", or "submission" in the player-facing interface.** Say *voice*, *clip*, *round*, *your turn*. The Impact Console may use technical language; the game may not.
- **Localise the UI, not just the content.** The competition build ships isiZulu and Setswana content/copy owned by Sbu and Lethabo respectively, with neutral functional shell labels where needed. Do not claim four launch languages without first-language review.
- **Never lie about money.** *"Sent for payment"* is not *"Paid."* The wallet's honesty is the product's credibility, and a judge who catches one optimistic label will discount everything else.
