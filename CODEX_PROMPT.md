# AMAZWI — continue the implementation programme

Pull first (`f1e9d03` or later). CI is green — the cross-platform object-key fix (`9fb9d75`) landed and passed. Re-confirm with `gh run watch --exit-status` on your first push before assuming it's still green.

Read `CLAUDE.md`, `05_amazwi/P0.md`, and the last ~8 `BUILD_LOG.md` entries before continuing — don't re-derive context. The pre-event build dispute is resolved (Sbu accepted 1 Sep); do not reopen it. Both lanes are open to you, but backend/money/data/deployment work stays labelled pending Sbu's review.

## Rules, unchanged

- TDD always: failing test → green → broader suite → focused commit.
- Real PostgreSQL 16 for schema/migration/resolver/consent/outbox/export tests. Never SQLite.
- Verify, don't assume — run the suite, typecheck, build; render UI in a browser and look at it.
- State limitations plainly. Every real block of work gets a full `BUILD_LOG.md` DID/HOW/WHY/CHANGED/NEXT/BLOCKED-PING entry.
- Pull before you start, push before you stop, verify sync after pushing (`git fetch` + compare `rev-parse`).
- Commit prefixes: `Consent:` `Audio:` `Peers:` `Council:` `Data:` `ML:` `UI:` `Ops:` `Hardening:` `Docs:`
- **Vercel stays paused.** No deployment path, ever, in this pass.
- Peer verification is authoritative; AI Council output is advisory only and may never touch eligibility, money, consent, audio retention, campaign launch, export approval, or model aliases.
- Tick plan checkboxes in `docs/superpowers/plans/*.md` as you actually finish each task — they're currently unreliable, so keep them honest going forward rather than leaving another batch stale.

## What's left

### Plan 02 — Stages 4–6 (`docs/superpowers/plans/2026-09-01-amazwi-02-council-data-models.md`)

Tasks 1–11 are done. Remaining:
- **Task 12:** finish Kaggle notebook-compatible scripts (`kaggle/reserve_run.py`, `amazwi_ml/budget.py` exist) — reproducible, seeded, **downloads nothing**. Enforce and test the 60-GPU-hour aggregate / 30-hour-per-account reservation guard.
- **Task 13:** deterministic LightGBM and XGBoost tabular challengers, fixed seeds, run through the existing tournament/promotion gate.
- **Task 14:** generate model cards and evidence hashes; complete Stage 4–6 acceptance. Model cards are generated evidence, never hand-written winner claims. A challenger failing its predeclared threshold must be blocked from promotion with no improvement language anywhere in the output.

**Hard gate:** no external dataset download, no Kaggle GPU execution, without explicit licence/terms and budget preflight approval. Code and synthetic fixtures only. If you hit that wall, stop and report rather than proceeding.

### Plan 03 — Signal Flow UI and Ops (`docs/superpowers/plans/2026-09-01-amazwi-03-signal-flow-ops.md`)

Themes, primitives, and the `/result/:contributionId` receipt route are built. Remaining:
- Task 0 (tooling/fixtures lock), finish Tasks 1/2/5 (route lock, typed API contracts, home/consent/record/verify/result routes — `src/styles/` doesn't exist yet and the locked file structure expects it).
- Task 7–8: Coverage Constellation backend contract + render. Aggregate dots/counts only — no public raw audio, no names.
- Task 9: mission proposals, human-only MTN authorisation — no agent may launch a campaign.
- Task 10: MTN Language Ops route.
- Task 11: 320–480px, 200% zoom, keyboard, screen-reader gates — the mockups' fixed-390px limitation is a hard requirement to actually fix here.
- Task 12: visual regression + evidence-gated Figma drift check against `JPZuFmbhRh9fhkgBLxRymq`. Do not claim Figma parity from static mockups alone.
- Task 13: verify the visible engagement-to-operations loop.

Both themes (Midnight Shweshwe, Signal Daylight) are equal first-class citizens — every check must pass on both.

### Plan 04 — Stage 9 hardening (`docs/superpowers/plans/2026-09-01-amazwi-04-hardening-demo.md`)

Task 1 partially done. Tasks 2–12 open: injectable auth with no production impersonation path; rate-limit adapters (document the in-memory limit honestly); PII/secret-safe structured logging; deterministic seed/reset structurally disabled in production; deterministic failure injection + safety drills; full Playwright coverage of the governed workflow; browser-visible failure + reduced-motion drills; accessibility/performance/target-device evidence; CI expansion with no deployment path added; fallback artefacts + two clean deterministic reset-and-demo cycles on target devices; final evidence and honesty review.

Run this only once the integrated local workflow actually exists end to end.

## Programme acceptance — all must hold when done

- Browser → API → private storage → two peers → resolver → reward → outbox → Council → receipt passes end to end.
- Revocation blocks new playback/assignment/export while preserving earned money and audit evidence.
- AI-disabled mode preserves the complete peer/reward/receipt path.
- One immutable dataset manifest rebuilds with an identical canonical hash.
- Model promotion blocked when a challenger fails its predeclared threshold.
- Signal Flow passes 320–480px, 200% zoom, keyboard, screen-reader, reduced-motion in both themes.
- Two deterministic reset-and-demo cycles pass on target devices.
- `P0.md`, `BUILD_LOG.md`, `HANDOVER_SBU.md`, `CLAUDE.md`, relevant READMEs and model/data cards report exactly what ran and what didn't.

## Stop and report, don't proceed, if you hit

- A consent bypass, public-audio path, reward regression, or migration failure.
- Anything needing an external dataset download or Kaggle GPU run before licence/budget preflight.
- Anything that's a real money/legal/data-integrity/deployment decision rather than mechanical implementation — flag for Sbu, don't invent it.
- Any pull toward resuming the paused Vercel deployment.

## Two items only a human closes

- L1: the four replacement Setswana distractors (`moraka`, `jusi`, `ting`, `diphaphatha`) need Lethabo's own read-aloud approval — don't approve on her behalf.
- L6: rehearsal is deliberately deferred by Lethabo. Don't restart it.
