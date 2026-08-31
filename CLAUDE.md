# AMAZWI — session orientation (auto-loaded every session in this directory)

**Current entry:** AMAZWI, Track 2 (Entertainment & Lifestyle), Team Sonar (Sbu + Lethabo). `MASTER_CONTEXT.md` at this root is **historical** (UMOYA/Track 1 exploration, superseded) — ignore it for current work.

## Read in this order, every new session

1. **This file** — the rules below.
2. [`05_amazwi/P0.md`](05_amazwi/P0.md) — current status of every task, gate table, what's done vs. open. The single source of truth for "where are we."
3. [`05_amazwi/BUILD_LOG.md`](05_amazwi/BUILD_LOG.md) — chronological log, **newest entries at the top**. Read at least the last 5–6 entries to see exactly what just happened and why, including mistakes caught and fixed.
4. [`05_amazwi/README.md`](05_amazwi/README.md) — product contract, settled decisions, file map for the full plan corpus (`05_amazwi/plan/00_MASTER_PLAN.md` onward).
5. [`HANDOVER_SBU.md`](HANDOVER_SBU.md) / [`HANDOVER_LETHABO.md`](HANDOVER_LETHABO.md) — the two teammates' reciprocal handover notes. Check both for anything addressed to you that hasn't been actioned yet.

Do not re-derive product decisions from scratch — they are settled in the files above. Do not re-litigate a decision recorded in `BUILD_LOG.md`'s append-only decisions table without a new dated row.

## The lane rule (set 31 Aug 2026, binding)

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

As of 31 Aug 2026: L1 (Setswana cards), L2/L3 (Figma design system + craft-pass mockups), L4 (error copy), L5 (deck skeleton + demo script), all of `05_amazwi/LETHABO_NEXT_WORK.md`'s items 1–6 (content fixes, stale-mockup reconciliation, five hero screens, real tokens.css theme switching, accessibility evidence — including a keyboard-reachability gap found *and fixed*), and Gate A's Lethabo-half start (routing, tokens wired into the real frontend, an honest Mini-App/browser-mode label, all tested). Full detail and exact commit-by-commit record in `BUILD_LOG.md`.

**L6 (rehearsal) is deliberately deferred** — Lethabo's call: "we will do L6 later after everything is built." Don't restart it until asked.

## Git discipline

Pull before you start. Push before you stop. Never `git checkout`/`reset`/`clean` without checking `git status` first and stashing anything real. Never force-push. Commit messages explain *why*, not just *what* — match the style already in the log (`git log --oneline`).
