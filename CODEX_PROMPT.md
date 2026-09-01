# AMAZWI — complete the remaining implementation programme

You are working in the AMAZWI repository (Team Sonar, MTN MoMo Mini App Hackathon, Track 2). Read `CLAUDE.md`, `05_amazwi/P0.md`, and the last ~8 entries of `05_amazwi/BUILD_LOG.md` before touching anything. Then execute everything listed below, in order.

## Governance context you must not re-litigate

- The earlier Sbu/Lethabo dispute about building before the event is **resolved** — `P0.md` records Sbu's acceptance on 1 Sep. Do not reopen it.
- Both lanes are open to you (Lethabo loosened the lane rule 31 Aug ~23:40), but backend/money/data/deployment work stays **labelled pending Sbu's review** in `BUILD_LOG.md` and `HANDOVER_SBU.md`.
- The Vercel deployment **stays paused**. Do not resume it, and do not add a deployment path.
- Peer verification is authoritative. AI Council output is advisory only and may never alter eligibility, money, consent, audio retention, campaign launch, export approval, or model aliases.

## Non-negotiable working rules

- **TDD, always.** Every task starts with a failing test, reaches green, then runs the broader suite, then gets a focused commit.
- **Real PostgreSQL 16** for all schema, migration, resolver, consent, outbox, and export tests. Never substitute SQLite.
- **Verify, don't assume.** Run the actual suite, typecheck, and build. For UI, render it in a browser and look at it. Measure touch targets and keyboard focus with real DOM queries and real Tab presses.
- **State limitations plainly.** If something can't be verified, say so in the same breath as the finding. Never claim more than what was actually checked.
- **Every real block of work gets a `BUILD_LOG.md` entry** in the established DID/HOW/WHY/CHANGED/NEXT/BLOCKED-PING format.
- **Pull before you start, push before you stop**, and verify sync after pushing (`git fetch` + compare `rev-parse`).
- Commit message prefixes: `Consent:` `Audio:` `Peers:` `Council:` `Data:` `ML:` `UI:` `Ops:` `Hardening:` `Docs:`
- **Tick the plan checkboxes as you go.** All 322 boxes across the four plan files are currently unticked even though Stages 1–3 and most of 4–6 are actually built. Reconcile them against reality as your first documentation pass, then keep them current.

---

## 0. FIX CI FIRST — it is currently red

`starter/backend/tests/test_local_storage.py::test_object_key_cannot_escape_storage_root` fails on CI (Linux) while passing locally on Windows. The last three pushes are all red.

**Root cause:** `app/storage/local.py::_relative_key` validates with `Path(object_key).is_absolute()`. On Linux, `Path("C:/secret")` is a *relative* path whose first component is the literal directory name `C:` — so `is_absolute()` returns `False`, there is no `..` part, and `(self.root / candidate).resolve()` lands harmlessly under the root. The guard silently does nothing and `InvalidObjectKey` is never raised.

This is a real portability bug in a security boundary, not just a broken test. Fix the implementation so object-key validation is platform-independent: explicitly reject Windows drive-letter prefixes (`X:`), backslash separators, absolute POSIX paths, `..` traversal, empty keys, and NUL bytes — on every platform, regardless of which OS is running. Add cases covering each rejection class. Confirm the fix on CI with `gh run watch --exit-status`, not just locally.

---

## 1. Plan 02 — finish Stages 4–6 (`docs/superpowers/plans/2026-09-01-amazwi-02-council-data-models.md`)

Tasks 1–11 are built (outbox, resolver emit, SKIP LOCKED leasing, deterministic specialists, worker + read API, provenance schema, export firewall, manifests/splits, external preflight, WER/CER metrics, tournaments and promotion gates). Remaining:

- **Task 12 (finish):** Kaggle notebook-compatible scripts with explicit seeds and artefact output. `kaggle/reserve_run.py` and `amazwi_ml/budget.py` exist; complete the packaging so a run is reproducible and **downloads nothing**. The 60-GPU-hour aggregate / 30-hours-per-account reservation guard must be enforced and tested.
- **Task 13:** deterministic LightGBM and XGBoost tabular challengers, fixed seeds, evaluated through the existing tournament/promotion gate.
- **Task 14:** generate model cards and evidence hashes; complete Stage 4–6 acceptance. Model cards are **generated evidence reports** — never hand-written winner claims. A challenger that fails its predeclared threshold must be blocked from promotion and must not produce improvement language anywhere in the generated output.
- Test fixtures and reports for all of the above, using synthetic fixtures only.

**Hard gate:** no external dataset download and no Kaggle GPU execution without explicit licence/terms and budget preflight approval. Code and synthetic fixtures may proceed; actual downloads may not. If you reach a point that requires one, stop and report it rather than proceeding.

## 2. Plan 03 — Signal Flow UI and Ops (`docs/superpowers/plans/2026-09-01-amazwi-03-signal-flow-ops.md`)

Themes, Signal Flow primitives, the receipt and the `/result/:contributionId` route are built. Remaining:

- **Task 0:** lock frontend tooling, scripts, and deterministic browser fixtures.
- **Tasks 1, 2, 5 (complete them):** finish the shell/route lock, the typed API contract lock with visible failure mapping, and the home/consent/record/verify/result route implementations. Note `src/styles/` does not exist yet — the locked file structure expects it.
- **Task 7:** aggregate Coverage Constellation backend contracts.
- **Task 8:** render the flat South Africa Coverage Constellation. Aggregate dots and counts only — **no public raw audio, no names**.
- **Task 9:** mission proposals with human-only MTN authorisation. No agent may launch a campaign.
- **Task 10:** the MTN Language Ops route.
- **Task 11:** 320–480px, 200% zoom, keyboard, and screen-reader gates. The fixed-390px mockup limitation flagged in `ACCESSIBILITY_EVIDENCE.md` is a hard requirement for the real frontend — it must actually reflow.
- **Task 12:** visual regression and evidence-gated Figma token drift against file `JPZuFmbhRh9fhkgBLxRymq`. **Do not claim Figma parity from static mockups alone.**
- **Task 13:** verify the visible engagement-to-operations loop.

Both themes (Midnight Shweshwe and Signal Daylight) are equal first-class citizens and must pass every check. Ndebele remains seasonal, and if used its attribution is said aloud.

## 3. Plan 04 — Stage 9 hardening and demo (`docs/superpowers/plans/2026-09-01-amazwi-04-hardening-demo.md`)

Task 1 (runtime boundaries and status announcements) is partially built. Remaining, Tasks 2–12:

- Injectable authentication with **no production impersonation path**.
- Rate-limit adapters, documenting the in-memory limit honestly rather than implying distributed enforcement.
- PII- and secret-safe structured logging.
- Deterministic seed/reset, **structurally disabled in production** — not merely flag-guarded.
- Deterministic failure injection and backend safety drills.
- Playwright coverage driving the complete governed workflow end to end.
- Browser-visible failure and reduced-motion drills.
- Accessibility, performance, and physical target-device evidence.
- CI expansion — **without adding any deployment path**.
- Fallback artefacts, and two clean deterministic reset-and-demo cycles proven on target devices.
- Final evidence and honesty review.

Run this plan only after the integrated local workflow actually exists.

---

## Programme acceptance — all of these must hold when you are done

- Browser → API → private storage → two peers → resolver → reward → outbox → Council → receipt passes end to end.
- Revocation blocks new playback, assignment and export while preserving earned money and audit evidence.
- AI-disabled mode preserves the complete peer/reward/receipt path.
- One immutable external-plus-opted-in dataset manifest rebuilds with an identical canonical hash.
- Model promotion is blocked when a challenger fails its predeclared acceptance threshold.
- Signal Flow passes 320–480px, 200% zoom, keyboard, screen-reader and reduced-motion checks in **both** first-class themes.
- Two deterministic reset-and-demo cycles pass on target devices.
- `P0.md`, `BUILD_LOG.md`, `HANDOVER_SBU.md`, `CLAUDE.md`, the relevant READMEs and all model/data cards report **exactly what ran and what did not**.

## Stop and report rather than proceeding, if you hit any of these

- A consent bypass, a public-audio path, a reward regression, or a migration failure.
- Anything requiring an external dataset download or Kaggle GPU execution before licence and budget preflight approval.
- Anything that looks like a genuine money, legal, data-integrity or deployment-safety **decision** rather than mechanical implementation — those remain Sbu's call per `05_BUILD.md` §2. Build to spec and flag it; do not invent the decision.
- Any request or temptation to resume the paused Vercel deployment.

## Two open human items you cannot close yourself

- **L1:** the four replacement Setswana distractors (`moraka`, `jusi`, `ting`, `diphaphatha`) need Lethabo's own native read-aloud approval. `validate_cards.mjs` flags this as a warning, not an error. Do not approve them on her behalf.
- **L6:** rehearsal is deliberately deferred by Lethabo. Do not restart it.
