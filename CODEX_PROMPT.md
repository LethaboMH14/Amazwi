# AMAZWI — finish Plans 02, 03, 04 (Postgres/browser/device work)

Pull first (`cb9f655` or later). Since the last handoff, a lot of pure-logic test coverage landed from a non-Postgres environment: every module in `starter/ml/amazwi_ml/` now has real tests (81/81 passing), and `starter/frontend` gained tests for `signalMotion`, `theme`/`isNdebeleSeason`, the API client's failure mapping, `digest()` (SHA-256 upload integrity), and `StatusAnnouncer`'s accessibility contract (57/57 passing). A real shared-infra bug was found and fixed along the way: `vitest.config.ts`'s `globals: false` meant React Testing Library's auto-cleanup never registered — fixed in `test-setup.ts`. Read the last ~8 `BUILD_LOG.md` entries for full detail before continuing.

**What's left is specifically everything that needs Postgres, a real browser render, or a physical device** — none of which were available in the environment that did the above. That's you.

## Rules, unchanged

- TDD always: failing test → green → broader suite → focused commit.
- Real PostgreSQL 16 for schema/migration/resolver/consent/outbox/export tests. Never SQLite.
- Confirm CI green with `gh run watch --exit-status` after every push.
- Every real block of work gets a full `BUILD_LOG.md` DID/HOW/WHY/CHANGED/NEXT/BLOCKED-PING entry.
- Pull before you start, push before you stop, verify sync after pushing.
- Commit prefixes: `Consent:` `Audio:` `Peers:` `Council:` `Data:` `ML:` `UI:` `Ops:` `Hardening:` `Docs:`
- **Vercel stays paused.** No deployment path, ever.
- Peer verification is authoritative; AI Council output is advisory only.

## Plan 02 — the one Postgres-dependent item left

- **Export-trigger migration test:** the approved-export immutability trigger (`1efd1ef`) needs a real-PostgreSQL migration test, not just unit coverage — this is explicitly flagged as still required and is the only thing blocking Plan 02's Stage 4–6 close besides the write-up.
- Task 14: model cards and evidence hashes (the generators — `amazwi_ml/evidence.py` — are now fully tested; wire them to real tournament output), Stage 4–6 acceptance write-up.

## Plan 03 — Signal Flow UI and Ops (`docs/superpowers/plans/2026-09-01-amazwi-03-signal-flow-ops.md`)

Themes, primitives, motion, the receipt route, and now solid unit coverage on the pure-logic seams are all done. What's left needs a real render:

- Task 0: tooling/fixtures lock (if not already covered by what exists).
- Finish Tasks 1/2/5 where they depend on visual verification: `src/styles/` doesn't exist yet and the locked file structure expects it.
- Task 7–8: Coverage Constellation backend contract + actual render. Aggregate dots/counts only — no public raw audio, no names.
- Task 9: mission proposals, human-only MTN authorisation.
- Task 10: MTN Language Ops route.
- Task 11: 320–480px, 200% zoom, keyboard, screen-reader gates — needs a real browser to verify reflow, not just jsdom. The `StatusAnnouncer`/live-region behavior is already unit-tested; this is the visual/interaction layer on top.
- Task 12: visual regression + evidence-gated Figma drift check against `JPZuFmbhRh9fhkgBLxRymq`. Do not claim Figma parity from static mockups alone.
- Task 13: verify the visible engagement-to-operations loop.

## Plan 04 — Stage 9 hardening (`docs/superpowers/plans/2026-09-01-amazwi-04-hardening-demo.md`)

All needs Postgres, real drills, or device evidence:

- Injectable auth with no production impersonation path.
- Rate-limit adapters — document the in-memory limit honestly.
- PII/secret-safe structured logging.
- Deterministic seed/reset, structurally disabled in production.
- Deterministic failure injection and backend safety drills — needs real Postgres.
- Full Playwright coverage of the governed workflow end to end — needs a real browser.
- Browser-visible failure and reduced-motion drills.
- Accessibility, performance, and physical target-device evidence.
- CI expansion — without adding any deployment path.
- Fallback artefacts, and two clean deterministic reset-and-demo cycles on target devices.
- Final evidence and honesty review — the last task in the whole programme; state plainly what actually works end to end and what doesn't.

## Programme acceptance — all must hold when done

- Browser → API → private storage → two peers → resolver → reward → outbox → Council → receipt passes end to end.
- Revocation blocks new playback/assignment/export while preserving earned money and audit evidence.
- AI-disabled mode preserves the complete peer/reward/receipt path.
- One immutable dataset manifest rebuilds with an identical canonical hash. (Unit-verified already; still needs the real end-to-end path.)
- Model promotion blocked when a challenger fails its predeclared threshold. (Unit-verified already.)
- Signal Flow passes 320–480px, 200% zoom, keyboard, screen-reader, reduced-motion in both themes.
- Two deterministic reset-and-demo cycles pass on target devices.
- `P0.md`, `BUILD_LOG.md`, `HANDOVER_SBU.md`, `CLAUDE.md`, relevant READMEs and model/data cards report exactly what ran and what didn't.

## Stop and report, don't proceed, if you hit

- A consent bypass, public-audio path, reward regression, or migration failure.
- Anything needing an external dataset download or Kaggle GPU run before licence/budget preflight (already hard-gated and unit-tested — don't try to route around it).
- A real money/legal/data-integrity/deployment decision rather than mechanical implementation.
- Any pull toward resuming the paused Vercel deployment.

## Two items only a human closes

- L1: the four replacement Setswana distractors (`moraka`, `jusi`, `ting`, `diphaphatha`) need Lethabo's own read-aloud approval.
- L6: rehearsal is deliberately deferred by Lethabo. Don't restart it.
