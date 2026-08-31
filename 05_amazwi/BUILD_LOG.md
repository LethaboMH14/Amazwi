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
`lane` is `platform` or `experience`. Example: `G4 platform: verifier resolution + EXPIRED path`

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
| PWA | Hand-written service worker | Planned | Workbox is more than we need |
| Audio | Web Audio API + MediaRecorder → Opus | Planned | — |
| Offline | IndexedDB outbox | Planned | — |
| Backend | Python 3.12 + FastAPI + Pydantic | Planned | — |
| DB | PostgreSQL 16 | Planned | Constraints are the product |
| Storage | S3-compatible, private, presigned | Planned | — |
| Async | FastAPI background tasks + `pending_jobs` | Planned | No broker to fail |
| Deploy | Cloudflare Pages / Vercel + container | Planned | — |
| Callbacks | Cloudflare Tunnel | Planned | — |
| Fonts | Archivo (Google Fonts, wdth + wght) | Decided | Not Inter — default-slop face |
| Design tokens | 5 Figma collections, 38 vars | **Done** | 31 Aug — starter plan caps at 1 mode/collection |

**Not in the build, on the roadmap slide only:** Celery · Redis · Kafka · TimescaleDB · MLflow · DVC · W&B · Terraform · Kubernetes.

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
| 6 | 30 cards each, with `accepted_answers` | Both | **G4 — the real bottleneck** |

---

# LOG

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
