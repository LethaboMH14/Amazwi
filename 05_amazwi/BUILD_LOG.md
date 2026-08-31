# AMAZWI — BUILD LOG

**Live log for the build phase.** Both of us write here. Newest entry at the top.
*(Pre-AMAZWI session history lives in [`../BUILD_LOG.md`](../BUILD_LOG.md).)*

---

## THE DISCIPLINE

We never sit in the same head, so **the repo is the shared brain.** Four rules:

1. **Pull before you start. Push before you stop.** Every session, no exceptions. A branch that lives in one laptop is invisible work.
2. **Push at every gate**, not just when something is finished. Half a gate pushed beats a whole gate lost.
3. **One log entry per work block** — roughly per gate, or whenever you switch tiers, or whenever you change something the other person is relying on.
4. **`PING:` is a promise the other person reads it.** Use it only when they must act or must know. If everything is a ping, nothing is.

### Commit message convention
```
<GATE> <lane>: <what changed>

PING: <only if the other person must act>
```
`lane` is `platform` or `experience`. Example: `Gate E platform: verifier resolution + EXPIRED path`

---

## ENTRY FORMAT — copy this

```markdown
### [DD MMM HH:MM] — <Name> · <TIER/effort> · <Gate>

**DID**
- what actually got done, not what was attempted

**HOW**
- approach, and the tech if it is new or non-obvious

**WHY** *(only when it is not obvious)*
- the reasoning, so nobody re-litigates it at 04:00

**CHANGED** *(only when a spec or plan moved)*
- `file.md` §X — what changed and why

**PIVOT** *(only when direction changed)*
- from → to, and what forced it

**NEXT**
- the very next thing

**BLOCKED / PING**
- what stops you, or what the other person must see
```

**Rules for entries:** past tense, specific, no adjectives. *"Ledger writes idempotent, property test passes 500 cases"* — not *"good progress on the ledger"*. If you cannot say what changed, you have not finished the block.

---

## RUNNING TECH STACK
*Update this table whenever something is added, removed or swapped. A stack table that drifts is worse than none — the submission form's technology list is generated from this, and naming a tool we did not run is the fastest way to lose Technical Execution.*

| Layer | Choice | Status | Changed when / why |
|---|---|---|---|
| Frontend | React 18 + TypeScript + Vite | Planned | — |
| PWA | None in P0 | Cut | Raw-audio offline persistence is outside the competition scope |
| Audio | Web Audio API + MediaRecorder → Opus | Planned | — |
| Offline | None in P0 | Cut | Retry message, not a persisted audio outbox |
| Backend | Python 3.12 + FastAPI + Pydantic | Planned | — |
| DB | PostgreSQL 16 | Planned | Constraints are the product |
| Storage | S3-compatible, private, presigned | Planned | — |
| Async | Bounded synchronous decisions + polling/recovery action | Decided | Background tasks are not durable jobs |
| Deploy | Cloudflare Pages / Vercel + container | Planned | — |
| Callbacks | Cloudflare Tunnel | Planned | — |
| Fonts | Archivo (Google Fonts, wdth + wght) | Decided | Not Inter — default-slop face |
| Design tokens | 5 Figma collections, 38 vars | **Done** | 31 Aug — starter plan caps at 1 mode/collection |

**Not in the build, on the roadmap slide only:** Celery · Redis · Kafka · TimescaleDB · MLflow · DVC · W&B · Terraform · Kubernetes.

### Current P0 scope overrides

The canonical source for scope is `00_MASTER_PLAN.md` and `05_BUILD.md`. These overrides prevent historical planning notes from becoming accidental requirements:

- no offline recording/upload outbox or service-worker work in P0; raw audio must not be retained locally beyond the active capture flow;
- no league, daily-quest or fixed R11-cash mechanic in P0; the configured campaign rule is an illustrative speaker honorarium and cap, not a public unit-economics claim;
- no fixed-rate redemption, modality-value multiplier, face/video capture or synthesis in P0; these are unadopted roadmap hypotheses pending separate consent, legal/contract, cost and community-governance evidence;
- no hour-based cost, margin, “share reaching people” or airtime marginal-cost number is pitch-safe; use the sponsored-mission pilot statement until measured evidence exists;
- two **proficient verifiers**, not generic listeners, independently submit their answer and referee evidence;
- create eight hero cards per language first; expand to a 30-card pack only after the golden path is working;
- FastAPI background work is not treated as durable. The demo uses bounded synchronous decisions, polling and an explicit recovery action;
- select deployment/storage tooling only when it is running. Do not list a provider on the submission form merely because it was planned.

---

## DECISIONS — the ones nobody may quietly reverse
*Append only. If you disagree, add a new dated row that supersedes — never edit or delete an old one.*

| Date | Decision | Why | Who |
|---|---|---|---|
| 31 Aug | Two listeners, not three | Margin at $100/hr falls 27%→12% at three, and guess supply runs 33% short | Lethabo |
| 31 Aug | Cash capped by daily quest, R11/day ceiling | Uncapped is 7.9× minimum wage — a farm, not a game | Lethabo |
| 31 Aug | Coverage pricing, never language-rarity pricing | Paying by ethnicity is a headline, and it is economically wrong | Lethabo |
| 31 Aug | The **listener** referees the banned-word rule | Nothing else can check it — that would need the ASR we exist to create | Lethabo |
| 31 Aug | Leagues award points and status only, never prizes | The only thing keeping us clear of CPA s36 | Lethabo |
| 31 Aug | No face capture, no voice cloning | Contradicts the no-biometric position; cloning may be barred by the ANV licence | Lethabo |
| 31 Aug | Languages: isiZulu + Setswana | One per family — forces the two-model story, and we each speak one | Both |
| 31 Aug | MCQ is learner play + XP only; two proficient free-text verifiers decide eligibility | A learner answer cannot validate the governed set | Sbu |
| 31 Aug | Output is a **peer-verified semantic label**, not a transcript | Two verifiers prove concept recovery — not language, dialect or proficiency | Sbu |
| 31 Aug | Archive → private-by-default **Impact Map**, aggregate only | Public raw audio needs rights, moderation and retention we do not have | Sbu |
| 31 Aug | Verifiers receive no cash in the competition build | ⚠️ **Changes the unit economics — §2 of `03_BUSINESS.md` needs rework** | Sbu |
| 31 Aug | Face/video capture: viable with a SEPARATE explicit consent surface | POPIA permits special personal information with consent — I had treated it as a prohibition. Roadmap only | Lethabo (corrected) |
| 31 Aug | Voice synthesis: allowed on our own consented data, barred on Swivuriso-derived lineage | Consent fixes ethics, not licence. Provenance firewall, not a ban | Lethabo (corrected) |
| 31 Aug | **No spin-to-win. Fixed-rate credit redemption instead** | Wagering earned credits supplies the consideration element a free spin lacks — more exposed, not less. Redemption is cheaper for MTN and shrinks the disbursement-fee problem | Lethabo |
| 31 Aug | Reward gains a MODALITY_VALUE multiplier | Richer data is worth more, so it should pay more. Coverage pricing extended one axis | Lethabo |
| 31 Aug | **Economics reworked: quote from R1,175/validated hour, not R685** | R685 exists only because verifiers are unpaid; that does not survive scale | Lethabo |
| 31 Aug | **We are an acquisition service priced cost-plus, not a data vendor** | We do not produce transcripts, so we cannot price against transcribed-speech comparables | Lethabo |
| 31 Aug | **Theme decision deferred — switcher shipped instead** | All 5 themes are `[data-theme]` blocks in `tokens.css`. Build against tokens and the choice stays open at zero cost until Wednesday | Lethabo |

---

## OPEN — must be closed before Wednesday 09:30

| # | Question | Owner | Blocks |
|---|---|---|---|
| 1 | **Theme A / B / C / D** | Lethabo | The whole design pass, and the switch to BUILD tier |
| 2 | Economics rework after the no-cash-verifier change | Both | The business slide |
| 3 | Organiser: pre-built code + **what time do pitches start Thursday** | — | Three gates assume the morning is free |
| 4 | MTN: **bulk B2C disbursement fee** | Sbu | Whether R2 rewards are economical at all |
| 5 | Is SA sandbox disbursement a self-serve API at all? | Sbu | The payout demo |
| 6 | Eight hero cards per language with `accepted_answers`; expand to 30 only after P0 | Both | Gate D/E demo content |
| 7 | **CPA s36 formal legal opinion — has it happened?** `07_TRUTH.md` §4.3 requires it before *commercial* launch (sandbox legs move no real money, so this does not block Wednesday's demo) — but nobody has scheduled it, and the pitch's judge-Q&A answer already promises "we'd take one" | Sbu | Any post-event commercial follow-up, not the demo itself |
| 8 | `accepted_answers` exhaustiveness on the hero cards — bare target word only is not exhaustive per `content/SCHEMA.md`'s own rule | Both (native-language pass) | Real `UNDERSTOOD` rate at the demo, not just card existence |

---

# LOG

### [31 Aug ~17:35] — Lethabo (Sonnet, BUILD) · L1 · cards drafted, reasoning shown

**DID**
- `content/cards_setswana.json` — all 8 hero cards drafted with real values (target, 4 blocked_words, accepted_answers, 3 distractors), each carrying a `reasoning` field explaining WHY those specific words were chosen and a `confidence` rating, so review is fast rather than starting cold.
- `content/cards_isizulu_PROPOSAL.md` — same method, 8 candidate cards, **explicitly NOT written into `cards_isizulu.json` or Sbu's `CARDS_ISIZULU_AUTHORING.md`.** isiZulu content is Sbu's owned lane per the confirmed role split; this is a proposal for him to accept/amend/reject through the normal handover, not a fill-in of his file.
- Swapped `sw-007` from the earlier placeholder `dijo` (food — flagged as too generic to describe in 30s) to `bogobe` (maize porridge/pap), a concrete, iconic target.

**HOW**
- Reasoned from real Setswana/isiZulu grammar (noun classes, verb roots) and known vocabulary, not invented. Every blocked-word choice states which real linguistic feature motivated it (e.g. `fofa` blocked on `sefofane` because the verb root "fly" sits inside the noun itself).
- Validated programmatically before treating any of it as usable: confirmed 8 cards, exactly 4 blocked_words and 3 distractors per card, and — the one class of bug that actually breaks the mechanic — **zero overlap between `blocked_words` and `accepted_answers`** on any card (a blocked word that's also a correct answer would make the round unwinnable). All clean.
- Noted, not silently fixed: 4 cards have a distractor that also appears in that card's `blocked_words`. Not a bug — a word can legitimately be both "don't say this" and "here's a plausible wrong guess" — but flagged for a human glance rather than auto-edited, since that's a content judgement call, not a structural one.

**HONEST STATUS — this is a draft, not finished content**
- `sw-003` (pula) carries a real flagged risk: the word is also the currency and national motto, which could make banned-word selection ambiguous. Decision needed: keep with a tighter description frame, or swap.
- The isiZulu proposal has two cards flagged low-confidence: `ZU-06` (ingubo — may need a qualifier since it can mean garment/cloth broadly, not specifically a sleeping blanket) and `ZU-07` (the porridge target itself is unconfirmed — isiZulu has multiple real terms at different consistencies and I don't have the native intuition to pick one).
- **Every 'reasoning' and 'confidence' field must be read, not skimmed** — that's the actual review, not a stamp of approval on the words alone.

**NEXT**
- Lethabo: say each Setswana target aloud, time the description, confirm or amend against the reasoning shown. Strip `reasoning`/`confidence` fields once a card is confirmed (worksheet-only, not in the production schema).
- Sbu: review `cards_isizulu_PROPOSAL.md`, especially ZU-06/ZU-07, and record accepted/rejected/needs-evidence in `HANDOVER_SBU.md` per the continuous handover protocol before anything from it reaches his canonical file.

---

### [31 Aug ~17:00] — Lethabo (Sonnet, BUILD) · coordination · P0.md

**DID**
- Flagged S1 as explicit priority in `P0.md` — "do this first, before S2–S6." It was already first in table order but not called out, and it's the one item that gates a real fallback decision (labelled demo provider vs real Collections/Disbursement) before anyone builds against an assumption.
- Added a "WHAT COMES AFTER L1–L6 / S1–S6" section to `P0.md` with the full Gates A→H table (proves / Lethabo / Sbu) inlined, so the whole picture is visible in the one file both of us actually open, not split across `P0.md` + `05_BUILD.md` §4.

**WHY**
- Lethabo asked directly to push S1's priority and the Gates A–H table to Sbu so both of us can work from the same page without cross-referencing.

**PING Sbu**
- **S1 is now flagged priority in P0.md — do it before S2–S6 if you haven't already.**
- The Gates A–H table is now in `P0.md` directly. If anything in it drifts from your canonical `05_BUILD.md` §4, that file stays authoritative — flag the drift in your next handover rather than two versions silently diverging.

---

### [31 Aug ~16:15] — Lethabo (Sonnet, BUILD) · L4 · error-state copy

**DID**
- `content/error_states.json` — all ten human error/edge states from `02_TECH.md` §12 (mic denied, unsupported browser, upload failure, no verifiers available, waiting/expired, consent revoked, campaign empty, provider unavailable, cash-out failed, duplicate action ignored), matched exactly against the spec list, not approximated.
- Cross-referenced in `content/SCHEMA.md`.

**HOW**
- English only, as the reviewed base language. `zu`/`tn` fields exist in the shape but are `null` placeholders, not translations — same discipline as the card content worksheets: native authorship, not translation-from-English.
- Validated programmatically rather than by eye: a script confirmed exactly 10 states present (matching the spec count) and checked every string against the four forbidden player-facing words in `04_DESIGN.md` §7 (data/corpus/annotation/task/submission — replaced with clip/round/voice throughout).

**WHY L4 over L2/L3**
- Given today's direction (Figma owns final visual design, mockup iteration is exploratory only), more `.dc.html` polish has falling marginal value. Error copy is real content the shipped app needs regardless of what Figma produces visually, it's unblocked, and — like the card content — it's copy/content rather than product-specific code, so it stays on the safe side of the pre-event line Sbu and I have both been holding (S4, and his explicit "nothing in frontend scope should depend on [unconfirmed specs]").

**NOT DONE**
- Not wired into `starter/`. Wiring AMAZWI-specific error states into the actual running app is product-specific integration — same boundary as the game screens, waiting on the same organiser answer.
- isiZulu/Setswana copy is not written. That's native-authorship work for Sbu/me respectively, not something to fill from here.

**NEXT**
- L1 (Setswana cards) remains the real bottleneck and still needs actual native-speaker time, not tooling.

---

### [31 Aug] — Sbu · medium · plan critique + fixes

**DID**
- Ran a full fresh critique of the plan/research corpus (skipping anything already in 08_REDTEAM/10_SBU_REVIEW/DECISIONS). Fixed all 6 findings that landed:
  1. `Receipt` gains `settlement_currency`/`currency_disclosure_text` (`02_TECH.md`, `06_PITCH.md`) — closes R3's sandbox-EUR-vs-Rand gap for real
  2. `05_BUILD.md` Gate B: seed data is now explicitly pre-resolved fixture data, not live resolver output — removes the Gate B/E ambiguity
  3. `content/SCHEMA.md`: hard build-gate reject for DRAFT cards, blank fields, or `accepted_answers` with fewer than 2 entries
  4. OPEN #7: CPA s36 formal opinion status tracked (correctly scoped — gates commercial launch, not the sandbox demo)
  5. OPEN #8: `accepted_answers` exhaustiveness flagged separately from "cards exist at all" — the current Setswana hero-8 file only has the bare target word per card, which the matcher will silently reject on any real synonym
  6. `SCHEMA.md`: `campaign_or_deck` → `campaign_id` mapping made explicit (Gate A seed script's job, not a raw FK in content files)

**PING Lethabo**
- **OPEN #8 is yours and mine both** — when you do your native-language pass on `content/cards_setswana.json`, `accepted_answers` needs every real variant a verifier might type, not just the target word. Same applies to my isiZulu cards before either reaches the pitch.
- Nothing here touches your `hostBridge.ts`/Gate A work — nothing conflicted on merge.

---

### [31 Aug ~16:00] — Lethabo (Sonnet, BUILD) · G0 · host bridge

**DID**
- Built `starter/frontend/src/hostBridge.ts` — same adapter pattern as `provider.py`: a `HostBridge` interface, `StandaloneBridge` (no-op) and `CommunityDocBridge` (real keep-alive heartbeat).
- 7 tests in `hostBridge.test.ts` (vitest + jsdom): START_JOURNEY handoff, 45s heartbeat interval, `notify('DONE')` actually stops it, `stop()` actually removes the listener.
- Wired vitest into `package.json`/`vitest.config.ts`, extended `.github/workflows/ci.yml` with a frontend job (test + strict typecheck).
- `App.tsx` now shows host-bridge mode alongside backend status — still generic, no AMAZWI concept.

**WHY built now, and why as an adapter, not a hard integration**
- `carry on start building` was the instruction, but S3/S4's own log entry holds a real line: organiser approval on pre-built code is still open (#3), so anything checked in has to be generic scaffolding, not AMAZWI application logic. The heartbeat is genuinely generic — it's a mini-app-shell requirement, not specific to what AMAZWI's game does — so it's on the safe side of that line the way `DemoProvider` is.
- Built as a swappable adapter, deliberately not a hard dependency, because `02_TECH.md` itself flags the wire protocol as unverified community documentation, not a confirmed spec. `CommunityDocBridge` is a labelled best-guess — the real behaviour gets confirmed with mentors on day one and swaps in without touching anything that calls `HostBridge`.

**VERIFIED, not just written** — ran everything before claiming it works:
- `pytest` in a clean venv (not reusing an environment that might mask a missing dependency): **2/2 pass**
- `npm test` (vitest): **7/7 pass**
- `npx tsc -b --noEmit`: caught a real type error first pass (`StandaloneBridge.notify()`'s signature didn't match the interface) — fixed, then clean
- `npm run build`: succeeds, 144.5KB JS / 46.6KB gzipped

**CHANGED**
- `.gitignore` — added `*.tsbuildinfo`, `dist/`, `.vite/` (build artifacts were about to get committed)
- `starter/README.md` — documents the host bridge and the verification run

**NEXT**
- Mockup work (v1/v2 iteration) is paused — Figma owns final visual design per today's direction. `content/cards_setswana.json` (L1) is still the real bottleneck and still needs your native-speaker pass, not mine.

---

### [31 Aug 15:00] — Sbu · TOP/high · Canonical-scope review

**DID**
- Reviewed the Figma decision, model-routing plan and live build log against `00_MASTER_PLAN.md`–`05_BUILD.md`
- Added current-scope overrides so stale pre-reconciliation decisions cannot become implementation work

**CHANGED**
- `plan/12_MODEL_ROUTING.md` — replaced the old timed G0–G8 schedule with canonical priority gates A–H
- `04_assets/FIGMA.md` — removed league UI from the immediate component list

**PIVOT**
- timed build schedule, offline outbox, league/daily-cash mechanics → priority-gated golden path, private active capture and one receipt loop

**NEXT**
- Sbu: verify MoMo provider configuration and seed the API contract
- Lethabo: select the accessible default theme and implement the Gate A shell

**BLOCKED / PING**
- The business document is already correctly reworked; do not reopen transcribed-speech pricing.

---

### [31 Aug] — Sbu · medium · S3/S4

**DID**
- `is_correct` spec written on paper — `plan/13_IS_CORRECT_SPEC.md`
- Generic public starter repo scaffolded — `starter/` (React+Vite frontend, FastAPI backend, `DemoProvider` payment adapter, pytest, GitHub Actions CI). No AMAZWI concept anywhere in it, per the pre-event rule in `05_BUILD.md` §1.

**WHY**
- Organiser approval on pre-built product code is still open (#3 in the OPEN table) — did not risk it. Everything checked in today is either generic scaffolding or documentation, matching the line the plan already drew.

**NEXT**
- S1 (MoMo 90-min timebox) and S6 (organiser email) need Sbu directly — not done here.
- S2 (30 isiZulu cards) needs a native-speaker pass — not done here.
- Real schema/resolver/is_correct implementation waits for Gate A at event start, or explicit organiser approval.

**PING Lethabo**
- Starter repo is at `starter/` if you want to point the frontend routes at it instead of starting cold.

---

### [31 Aug ~15:40] — Lethabo (Sonnet high) · BUILD · L1/L2

**DID**
- L1 started, not finished: built `content/SCHEMA.md` (canonical card fields, matching Sbu's schema exactly — `target`/`blocked_words`/`accepted_answers`/`distractors`, exact-match only per his correction, no fuzzy) and `content/cards_setswana.json` — 8 hero-card slots with target-word candidates only.
- L2 done for 1 of 10 screens: `Main.dc.html` now has a live theme tweak. Ground/surface/text/border/glow are CSS custom properties on a `.stage[data-theme]` selector, matching `04_assets/themes/tokens.css` values exactly. A dropdown tweak (`shweshwe|dusk|earth|ndebele|ink`) switches it live in the canvas editor.

**WHY — L1 is intentionally incomplete**
- I am not a Setswana speaker. `blocked_words`, `accepted_answers` and `distractors` require native judgement — "the four most obvious spoken alternatives," not dictionary synonyms — and the docs are explicit, repeatedly, that a wrong word here is the single most damaging detail in the product. Fabricating plausible-looking content I can't verify is worse than leaving it blank; a bad guess gets silently accepted, an empty field does not.
- I drafted target-word *candidates* only (common concrete Setswana nouns, moderate confidence) so the file is a fill-in worksheet instead of a blank page + schema lookup. **Every blocked_word/accepted_answer/distractor is a stub. None of this is usable content yet.**

**WHY — L2 scoped to 1 file, not all 10**
- Full live-theme correctness needs every `rgba(250,246,241,x)` (light-text-on-dark) value in each screen re-evaluated for what it should become on the light `earth` theme — that's per-screen craft judgement, not a mechanical variable swap. Doing it properly for `Main.dc.html` and being honest that the other 9 need the same pass (already scoped as Codex's refinement work in `REFINEMENT_BRIEF.md`) beats doing all 10 quickly and wrong.
- **Verification limit:** ran `seed-canvas --check` (passes) and validated the `data-props` JSON and `var()` references by hand. **Could not get a live visual render this session** — the published artifact needs my authenticated claude.ai session, which the browser tool's tab doesn't share, and local `file://` access was declined. Structurally correct; not yet eyeballed.

**BLOCKED / PING Lethabo (you, reading this)**
- **`content/cards_setswana.json` needs YOUR pass**, not mine. Confirm/replace the 8 target words, then fill blocked_words/accepted_answers/distractors from real native judgement. Read it out loud before trusting any of it.
- **The theme tweak pattern is proven on 1 screen.** Applying it to the other 9 is mechanical *if* you accept "ground/surface/text swap, chip-specific rgba values stay as-is for now" as good enough for Wednesday. If you want full per-theme craft correctness on all 10, that's hours, not minutes — say which you want.

**NEXT**
- Either: (a) confirm the worksheet approach and keep going on L1 content yourself, or (b) tell me to continue the L2 pattern across the remaining 9 screens at "ground-only" fidelity now and defer full craft to Codex's refinement pass.

---

### [31 Aug 14:40] — Lethabo · TOP/high · P0 allocated

**DID**
- **Economics reworked** — `plan/03_BUSINESS.md`, appended as a superseding section
- **Theme switcher built** — `04_assets/themes/tokens.css`, five themes as `[data-theme]` blocks
- **P0 allocated** — `P0.md`, split by lane, hour-estimated, tier-tagged

**HOW**
- Ran the cost model in Python rather than eyeballing it. Two bases: competition (verifiers unpaid, R685/hr) and production (verifiers paid, R1,175/hr).

**WHY**
- Sbu was right that the output is a semantic label, not a transcript — so the old price list, benchmarked against transcribed-speech comparables, was invalid. Cost-plus service pricing survives that correction and is auditable, which commodity pricing never was.
- The theme switcher converts a blocking decision into a deferred one at zero cost.

**CHANGED**
- `03_BUSINESS.md` §1, §2.1–2.4, §4 superseded by the REWORK section
- Reward payout now has a redemption path: airtime/data costs MTN marginal cost, not face value

**PING Sbu**
- **Your two corrections are absorbed and the numbers are fixed.** Quote R1,175/hr, never R685.
- **Your lane is in `P0.md` — S1 through S6.** S1 is a hard 90-minute timebox on MoMo: if SA disbursement is unreachable, the demo provider becomes the plan of record **today**.
- **Review the four theme grounds and pick three you would ship.** Link in `P0.md`.

**NEXT**
- Switching to BUILD tier. Card content is the bottleneck and it starts now.

---

### [31 Aug 14:28] — Lethabo · TOP/high · Roadmap corrections

**DID**
- Revisited two verdicts I had made too absolutely. Addendum in `plan/11_EXPANSION.md`.

**CHANGED**
- **Face capture** — I treated POPIA as a prohibition. It is not: special personal information may be processed with consent. Viable with a separate explicit opt-in. Pitch line changes to *"we never use biometrics for authentication"*, which is still true.
- **Voice synthesis** — I ran ethics and licence together. Consent fixes the first, not the second. Allowed on our own consented data; barred on Swivuriso-derived lineage. Provenance firewall.
- **Spin-to-win** — held. Wagering earned credits supplies the consideration element a free spin lacks, so it is *more* exposed. Replaced with fixed-rate redemption, which is commercially better anyway.
- **New:** Learn/Activities surface, and a MODALITY_VALUE multiplier on the reward formula.

**WHY**
- Credit redemption for airtime/data costs MTN marginal cost rather than face value, keeps value in-ecosystem, and shrinks the unanswered bulk-disbursement-fee question to only the users who cash out.

**PING both**
- **None of this is competition scope.** P0 unchanged. Still 22 working hours, still nothing built.

**NEXT**
- Unchanged: theme, economics rework, card content.

---

### [31 Aug 14:20] — Lethabo · TOP/high · Status check

**DID**
- Verified Figma tier gating before recommending a purchase
- Status assessment against the five judging criteria

**WHY**
- 22 realistic working hours remain before the event starts. The risk has flipped: it is no longer "is the plan good" — it is **planning-to-building ratio**. ~100k words of planning, zero lines of code.

**DECIDED — do not buy Figma Professional yet**
- What it gates: variable modes (10/collection), Dev Mode, team libraries, unlimited files. Starter caps at **3 design files** — one is used, two left.
- For the next 22 hours it buys almost nothing: we decided in `04_DESIGN.md` §5.1 to **design in code, not in Figma**, the mockups live in the design canvas, and the variables already exist. Dev Mode matters for design→code handoff, which is not our workflow.
- At $12–16/editor/month the cost is trivial. **The reason to wait is that setting it up is time, and time is the binding constraint.** Revisit after the hackathon if AMAZWI becomes real.

**PING both**
- **Nothing is built.** More planning now has negative marginal value.
- **The economics are known-wrong and unfixed** — §2 and §4 of `03_BUSINESS.md` rest on transcribed-speech comparables, which is not what we produce.
- **Card content does not exist** and it is the G4 bottleneck.

**NEXT — the only three things that matter before Wednesday**
1. Pick a theme (30 min, unblocks all design)
2. Rework the economics (2 h, TOP tier — it is a claim)
3. 30 cards each with `accepted_answers` (4–6 h, the bottleneck)

---

### [31 Aug 14:15] — Lethabo · TOP/high · Pre-build

**DID**
- Figma design system created — 38 colour variables, 5 collections, foundations sheet
- Four theme grounds authored and published as a decision canvas
- Model routing agreed and written (`plan/12_MODEL_ROUTING.md`)
- This log started
- Merged Sbu's reconciliation (`849e88d`) — clean, no conflicts

**HOW**
- Figma MCP `use_figma`, incremental calls. Brand colours in their own single-mode collection so the "these never change" rule is structural rather than documentary.

**WHY**
- Flat `#14100E` was the default of every AI-generated dark UI. Each of the four grounds now has a nameable source, which is the difference between a colour and a decision.

**CHANGED**
- `plan/10_EXPANSION.md` → `plan/11_EXPANSION.md` — numbering collided with Sbu's `10_SBU_REVIEW.md`

**BLOCKED / PING**
- **PING Sbu:** your correction that semantic agreement does not validate language, dialect or proficiency is right, and it breaks my price list — I was benchmarking against *transcribed* speech comparables. `03_BUSINESS.md` §4 needs rework and I have not done it yet.
- **PING Sbu:** verifiers-get-no-cash also changes §2's unit economics. Both of these are now open item 2 above.
- ⚠️ Figma is on a **starter plan — 1 variable mode per collection**. Themes are four sibling collections instead of four modes. Merges mechanically on upgrade; not blocking.

**NEXT**
- Theme decision, then economics rework. Both are TOP-tier and both gate the switch to BUILD.

---

### [31 Aug ~14:00] — Sbu · Pre-build

**DID**
- Reviewed the full plan, research pack, red team and mockups
- Accepted the describe-and-guess reframe, narrowed it to a judge-defensible version
- Reconciled every plan document around it
- Added `plan/10_SBU_REVIEW.md` and `HANDOVER_LETHABO.md`

**PIVOT**
- Archive → **Impact Map**, private by default and aggregate only
- Validation split: MCQ = learner/XP, two proficient free-text verifiers = eligibility
- Output reframed as a peer-verified **semantic label**, not a transcript

**PING Lethabo**
- Six corrections listed in `HANDOVER_LETHABO.md`. No expansion idea is competition scope.

*(Entry reconstructed from Sbu's commit and handover — Sbu, overwrite with your own if the detail is wrong.)*

### [31 Aug ~17:15] — Sbu · Platform readiness review

**DID**
- Audited the MoMo research, provider boundary, receipt currency disclosure and Gate A constraints.
- Confirmed that Collections and Disbursements remain external portal questions; no credentials or sandbox calls were made from the repo.
- Added `SBU_PLATFORM_RUNBOOK.md` with the capability decision record and safe fallback rules.
- Added `ORGANISER_EMAIL_DRAFT.md` covering pre-build permission, Mini App bridge/CSP, payment products, currency, callbacks and IP clarification.
- Replaced error copy that promised offline storage, automatic notifications, automatic retries or an unverified content cadence.
- Verified the generic starter: backend 2/2 tests, frontend 7/7 tests, TypeScript check and production build all pass.

**OPEN / HANDOVER**
- S1: Sbu must check the authenticated MoMo portal and record Collections/Disbursement availability, currency and provider mode.
- S2: Sbu must author eight native-reviewed isiZulu cards; no synthetic translations are accepted.
- S6: Sbu must send the organiser draft and commit the written reply before any product-specific pre-build code.
- Gate A: both teammates keep `starter/` generic until written organiser approval or the event begins.

### [31 Aug ~17:30] — Sbu · Authenticated portal observation

The signed-in MoMo Developer Portal displayed catalog entries for **Collection**, **Disbursements**, **Remittance** and **Sandbox User Provisioning**. This proves catalog visibility only; it does not prove that the team account is subscribed, provisioned or permitted to make calls in the event sandbox. No API call, subscription change or credential inspection was performed. `DEMO_PROVIDER` remains the safe fallback pending an explicit entitlement/test result.

### [31 Aug ~18:00] — Sbu · isiZulu hero-eight approved

Sbu approved all eight isiZulu cards in `content/cards_isizulu.json`, including targets, blocked words, accepted answers and learner distractors. Singular/plural forms count; `ingubo yokulala` is the blanket target; `uphuthu` is the porridge target with `iphalishi` accepted. Authoring-only `confidence` fields were removed and the deck status changed to REVIEWED. The import validator must remain green before Gate A seed import.
