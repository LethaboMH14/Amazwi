# AMAZWI — finish the implementation programme: Plans 02, 03, 04, completely

Pull first (`2e0726f` or later — CI confirmed green on that commit). Do not stop until every remaining task in all three plans is done, tested, and pushed, or you hit one of the stop conditions below. This is the full remainder of the programme — work through it in order, don't skip ahead and leave gaps.

Read `CLAUDE.md`, `05_amazwi/P0.md`, and the last ~10 `BUILD_LOG.md` entries first. The pre-event build dispute is resolved — don't reopen it.

## Rules, unchanged

- TDD always: failing test → green → broader suite → focused commit.
- Real PostgreSQL 16 for schema/migration/resolver/consent/outbox/export tests. Never SQLite.
- Verify, don't assume — run the suite, typecheck, build; render UI in a browser and look at it.
- Confirm CI green with `gh run watch --exit-status` (or `gh run list`) after every push. If `gh` can't authenticate in your environment, say so explicitly in the log instead of silently skipping the check — don't let that become a habit for the rest of the programme.
- Every real block of work gets a full `BUILD_LOG.md` DID/HOW/WHY/CHANGED/NEXT/BLOCKED-PING entry.
- Pull before you start, push before you stop, verify sync after pushing (`git fetch` + compare `rev-parse`).
- Commit prefixes: `Consent:` `Audio:` `Peers:` `Council:` `Data:` `ML:` `UI:` `Ops:` `Hardening:` `Docs:`
- **Vercel stays paused.** No deployment path, ever.
- Peer verification is authoritative; AI Council output is advisory only — never touches eligibility, money, consent, audio retention, campaign launch, export approval, or model aliases.
- Tick plan checkboxes in `docs/superpowers/plans/*.md` as you actually finish each task — keep them honest as you go.

## Plan 02 remainder (`docs/superpowers/plans/2026-09-01-amazwi-02-council-data-models.md`)

Task 12's CPU-safe packaging slice is done (`2e0726f`). Still open, per Codex's own remaining-work list plus the original Task 13/14 scope:

- Fixture tests for Task 12's `train_asr.py`/`evaluate_asr.py`/`package_run.py`.
- Enforce phase-specific budget allocation ranges within the 60-GPU-hour aggregate / 30-hour-per-account guard (not just the aggregate cap).
- **Task 13:** deterministic LightGBM and XGBoost tabular challengers, fixed seeds, run through the existing tournament/promotion gate.
- Full ASR metric reports and embedded-span metrics (beyond the basic WER/CER already in `amazwi_ml/metrics.py`).
- Complete the approved-export immutability trigger (flagged as still required back when the provenance firewall was drafted).
- **Task 14:** model cards and evidence hashes — generated evidence only, never hand-written winner claims; a challenger failing its predeclared threshold must be blocked from promotion with no improvement language anywhere in the output.
- Stage 4–6 end-to-end evidence acceptance, written up honestly.

**Hard gate, still in force:** no external dataset download, no Kaggle GPU execution, without explicit licence/terms and budget preflight approval. Code and synthetic fixtures only. If you hit that wall, stop and report rather than proceeding.

## Plan 03 (`docs/superpowers/plans/2026-09-01-amazwi-03-signal-flow-ops.md`)

Themes, primitives, and the `/result/:contributionId` receipt route are built. Everything else:

- Task 0: tooling/fixtures lock.
- Finish Tasks 1/2/5: route lock, typed API contracts with visible failure mapping, home/consent/record/verify/result routes. `src/styles/` doesn't exist yet — the locked file structure expects it.
- Task 7–8: Coverage Constellation backend contract + render. Aggregate dots/counts only — no public raw audio, no names.
- Task 9: mission proposals, human-only MTN authorisation — no agent may launch a campaign.
- Task 10: MTN Language Ops route.
- Task 11: 320–480px, 200% zoom, keyboard, screen-reader gates — actually fix the mockups' fixed-390px reflow limitation, don't just note it.
- Task 12: visual regression + evidence-gated Figma drift check against `JPZuFmbhRh9fhkgBLxRymq`. Do not claim Figma parity from static mockups alone.
- Task 13: verify the visible engagement-to-operations loop.

Both themes (Midnight Shweshwe, Signal Daylight) are equal first-class citizens — every check passes on both.

## Plan 04 (`docs/superpowers/plans/2026-09-01-amazwi-04-hardening-demo.md`)

Task 1 partially done. All of Tasks 2–12:

- Injectable auth with no production impersonation path.
- Rate-limit adapters — document the in-memory limit honestly, don't imply distributed enforcement.
- PII/secret-safe structured logging.
- Deterministic seed/reset, structurally disabled in production (not just flag-guarded).
- Deterministic failure injection and backend safety drills.
- Full Playwright coverage driving the complete governed workflow end to end.
- Browser-visible failure and reduced-motion drills.
- Accessibility, performance, and physical target-device evidence.
- CI expansion — without adding any deployment path.
- Fallback artefacts, and two clean deterministic reset-and-demo cycles proven on target devices.
- Final evidence and honesty review — this is the last task in the entire programme; it should state plainly what actually works end to end and what doesn't.

Run Plan 04 only once Plans 02 and 03 leave an integrated local workflow that actually works.

## Programme acceptance — all must hold when you're done

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
