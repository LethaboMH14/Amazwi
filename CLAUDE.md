# AMAZWI — session orientation (auto-loaded every session in this directory)

**Current entry:** AMAZWI, Track 2 (Entertainment & Lifestyle), Team Sonar (Sbu + Lethabo). `MASTER_CONTEXT.md` at this root is **historical** (UMOYA/Track 1 exploration, superseded) — ignore it for current work.

## ✅ Settled 1 Sep 2026: the pre-event build question is resolved — do not reopen it

Lethabo decided (31 Aug) to start real competition application code before the event, superseding `05_BUILD.md` §1's wait-for-approval rule. Sbu disputed it at the time. **Sbu accepted it on 1 September** — recorded in `05_amazwi/P0.md`: *"Sbu/Sibusiso accepts Lethabo's decision to proceed with AMAZWI-specific implementation before the event. The earlier dispute is superseded; historical rows remain for audit history only."*

Pre-event code is a legitimate working baseline. The team still follows the invitation's in-person / no-outside-assistance rule during the hackathon, and still discloses the actual build history honestly if asked. Both original positions stay in `BUILD_LOG.md` as audit history — do not delete them, and do not re-litigate the decision without a new dated row.

⚠️ **`05_BUILD.md` §1 still contains the older wait-for-approval wording.** `P0.md` and this file supersede it. That paragraph is stale and should be reconciled the next time anyone edits that document.

## Read in this order, every new session

1. **This file** — the rules below.
2. [`05_amazwi/P0.md`](05_amazwi/P0.md) — current status of every task, gate table, what's done vs. open. The single source of truth for "where are we."
3. [`05_amazwi/BUILD_LOG.md`](05_amazwi/BUILD_LOG.md) — chronological log, **newest entries at the top**. Read at least the last 5–6 entries to see exactly what just happened and why, including mistakes caught and fixed.
4. [`05_amazwi/README.md`](05_amazwi/README.md) — product contract, settled decisions, file map for the full plan corpus (`05_amazwi/plan/00_MASTER_PLAN.md` onward).
5. [`HANDOVER_SBU.md`](HANDOVER_SBU.md) / [`HANDOVER_LETHABO.md`](HANDOVER_LETHABO.md) — the two teammates' reciprocal handover notes. Check both for anything addressed to you that hasn't been actioned yet.

**Approved design and executable programme; autonomous implementation authorised:**
[`05_amazwi/plan/16_GOVERNED_INTELLIGENCE_DESIGN.md`](05_amazwi/plan/16_GOVERNED_INTELLIGENCE_DESIGN.md)
records Lethabo's approved maximum-scope expansion: Gate C consent, Gate D
private audio, Gate E real peers, then an advisory AI Council, governed data
refinery, external-dataset/Kaggle model campaign, MTN Language Ops and the
Figma-first Signal Flow UI. It does not claim those stages are built. The
paused Vercel deployment remains paused, peer truth remains authoritative, and
cross-lane implementation remains pending Sbu's review. Lethabo subsequently
approved moving into implementation and instructed uninterrupted autonomous
execution with frequent commits and pushes. The execution contract is
[`docs/superpowers/plans/2026-09-01-amazwi-governed-intelligence-program.md`](docs/superpowers/plans/2026-09-01-amazwi-governed-intelligence-program.md),
with subsystem plans for
[Stages 1–3](docs/superpowers/plans/2026-09-01-amazwi-01-governance-audio-peers.md),
[Stages 4–6](docs/superpowers/plans/2026-09-01-amazwi-02-council-data-models.md),
[Stages 7–8](docs/superpowers/plans/2026-09-01-amazwi-03-signal-flow-ops.md) and
[Stage 9](docs/superpowers/plans/2026-09-01-amazwi-04-hardening-demo.md).
Do not infer stage completion from plan approval; only fresh acceptance evidence
changes build status.

Do not re-derive product decisions from scratch — they are settled in the files above. Do not re-litigate a decision recorded in `BUILD_LOG.md`'s append-only decisions table without a new dated row.

## The lane rule — UPDATED 31 Aug 2026 ~23:40

Lethabo explicitly loosened this: **"work on the backend as well, it doesn't matter as long as we update on what we did — we all work on the same areas."** Both lanes may now be worked in this session. The discipline that made the original rule matter still applies, just without the lane restriction:
- **Document everything, always** — every real block of work still gets a full `BUILD_LOG.md` entry, same as before.
- **Never invent a money/legal/deployment-safety decision** that's supposed to be Sbu's final call per `05_BUILD.md` §2 — build to spec, flag anything that looks like a real decision rather than mechanical implementation, for his review.
- **Say what's provisional.** Backend work done in this session is real work, tested to the same bar as everything else, but Sbu should still review it — frame it that way in the log and in `HANDOVER_SBU.md`, not as if it's beyond question just because it's done.

Original rule text, kept for context on why the discipline exists:

**Lethabo owns Product, Experience and Demo** (`05_BUILD.md` §2): React/frontend, design tokens and screens, recorder/verifier/learner UX, wallet/receipt/Impact Map UI, accessibility, demo runbook, Setswana content, narrative/pitch.

**Sbu owns Platform, MoMo and Trust**: backend/API, database/states, resolver, ledger, campaign funding, payment adapters, consent enforcement, deployment, isiZulu content, technical/business proof.

**Default: work only in Lethabo's lane.** Do not start Sbu's tasks (S1–S6, or his half of any Gate) speculatively.

**Exception — real stoppers only:** if Lethabo's-lane progress is genuinely blocked on something only Sbu's lane can unblock (e.g., no backend running to test an API client against, no schema to build a real screen's data against), it is fine to do the minimum needed in Sbu's lane to keep moving. When that happens:
- Say explicitly in `BUILD_LOG.md` that this is a cross-lane exception and why it was necessary, not optional.
- Do the work to the same standard as everything else here (tested, verified, documented) — it is a real contribution, not a placeholder.
- Flag it clearly as **pending Sbu's review** — in the log entry, in `HANDOVER_SBU.md`, and (if it touches a canonical plan doc) in the doc itself. Never silently treat a provisional cross-lane fix as final.
- Do not invent business/legal/money decisions while doing this — those stay Sbu's call per `05_BUILD.md` §2 ("Sbu has final say on money, data integrity and deployment safety") regardless of who wrote the code.

## The standard, carried forward from the session that wrote this file

This is not a lower-effort resumption — match what was already happening:
- **Verify, don't assume.** Run the actual test suite, typecheck, build. For UI, actually render it in a browser and look — a screenshot caught a real "smudge" earlier in this project that looked fine in code. Measure touch targets and keyboard focus with real DOM queries and real Tab presses, not by inspecting markup and guessing.
- **Catch your own mistakes and say so.** This session caught and fixed, in the open: a CSS cascade error that would have silently broken a button's styling, a mislabeled reference file, a real content bug (a Nguni word wrongly shown on a screen labelled "Setswana"), and a security CVE in a package version about to be installed. Each is logged in `BUILD_LOG.md` as what it was, not smoothed over.
- **State limitations plainly.** If something can't be verified (e.g., a browser tool couldn't emulate a feature, a fallback recording can't honestly be made yet because the real thing doesn't exist), say so in the same breath as the finding — don't claim more than what was actually checked.
- **Every real block of work gets a `BUILD_LOG.md` entry** in the established format (DID/HOW/WHY/CHANGED/NEXT/BLOCKED-PING). Pull before starting, push before stopping, verify sync after pushing (`git fetch` + compare `rev-parse`).
- **Model/effort routing** — `05_amazwi/plan/12_MODEL_ROUTING.md`: judgment work (design direction, claims, content authorship, anything unverifiable) goes to the top tier; mechanical work against a settled spec goes to build tier. Say out loud when switching.

## What's already done — don't redo it

Pre-event content/design work: L1 (Setswana cards, one open item — see below), L2/L3 (Figma design system + craft-pass mockups), L4 (error copy), L5 (deck skeleton + demo script), and all of `05_amazwi/LETHABO_NEXT_WORK.md`'s items 1–6 (content fixes, stale-mockup reconciliation, five hero screens, real tokens.css theme switching, accessibility evidence including a keyboard-reachability gap found *and fixed*).

**Governed Intelligence programme, as of 1 Sep** (the checkboxes inside the four plan files under `docs/superpowers/plans/` are **not reliable** — 322 of them are unticked even though most of Plan 01 and much of Plan 02 is actually built and tested; go by `BUILD_LOG.md` commits and `HANDOVER_SBU.md`, not the checkbox state):

- **Plan 01, Stages 1–3 — done.** Consent, private audio storage, real peer API, and the matching frontend flows (consent, recording, verification).
- **Plan 02, Stages 4–6 — mostly done.** Tasks 1–11 shipped: transactional outbox with `SKIP LOCKED` leasing, resolver-transaction event emission, deterministic advisory Council specialists, the recoverable worker + read-only status API, dataset provenance/export-firewall schema, immutable manifests/speaker-safe splits, external-dataset preflight gate, WER/CER/tabular metrics, deterministic tournament and promotion gates. **Remaining:** Task 12 (Kaggle packaging, no downloads), Task 13 (LightGBM/XGBoost challengers), Task 14 (model cards, evidence hashes, Stage acceptance).
- **Plan 03, Stages 7–8 — partial.** Themes, Signal Flow primitives, and the peer-truth-first `/result/:contributionId` receipt route are built. **Remaining:** Task 0 (tooling lock), finishing Tasks 1/2/5, Coverage Constellation (7–8), missions/MTN authorisation (9), the MTN Language Ops route (10), the 320–480px/zoom/keyboard/screen-reader gates (11), visual regression + Figma drift check against `JPZuFmbhRh9fhkgBLxRymq` (12), and the engagement-to-operations loop verification (13).
- **Plan 04, Stage 9 — barely started.** Only Task 1 (runtime boundaries) is partially in. Tasks 2–12 (auth, rate limits, PII-safe logging, deterministic reset disabled in production, failure drills, Playwright e2e, accessibility/perf/device evidence, CI expansion, fallback artefacts, final honesty review) are all open.

⚠️ **CI was red as of the last check (commits `d4026bf`, `72cc3fb`, `6f9505c`)** — `test_object_key_cannot_escape_storage_root` fails on Linux CI while passing on Windows: `app/storage/local.py`'s traversal guard uses `Path(...).is_absolute()`, which doesn't reject a Windows-style `C:/...` key on POSIX. If this hasn't been fixed since, fix it first — it's a real security-boundary portability bug, not a flaky test. Confirm green with `gh run watch --exit-status`, not just locally.

**Still open, not disputed by either side:** L1's four replacement distractors (`moraka`/`jusi`/`ting`/`diphaphatha` in `cards_setswana.json`) need Lethabo's own native read-aloud confirmation before the deck is fully signed off — flagged as a warning by `validate_cards.mjs`, not an error.

**L6 (rehearsal) is deliberately deferred** — Lethabo's call: "we will do L6 later after everything is built." Don't restart it until asked.

## Git discipline

Pull before you start. Push before you stop. Never `git checkout`/`reset`/`clean` without checking `git status` first and stashing anything real. Never force-push. Commit messages explain *why*, not just *what* — match the style already in the log (`git log --oneline`).
