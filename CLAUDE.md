# AMAZWI — session orientation (auto-loaded every session in this directory)

**Current entry:** AMAZWI, Track 2 (Entertainment & Lifestyle), Team Sonar (Sbu + Lethabo). `MASTER_CONTEXT.md` at this root is **historical** (UMOYA/Track 1 exploration, superseded) — ignore it for current work.

## ⚠️ Read this before anything else: an unresolved disagreement between the two teammates

Lethabo decided (31 Aug) to start real competition application code before the event, superseding `05_BUILD.md` §1's wait-for-approval rule — see `05_amazwi/BUILD_LOG.md`'s decisions table. **Sbu has since recorded, in the same table and in `P0.md`, that he disputes this** and has not accepted it: his position is that the invitation requires the build to happen on-site by the two-person team, the public terms require hackathon-created work absent organiser approval, and pre-event code/mockups/plans are preparation only, not build-gate progress. Both positions are preserved in `BUILD_LOG.md` — neither was deleted or overwritten, and it is explicitly **not Claude's call to arbitrate by picking a side in a merge.**

**If this is still unresolved when a new session starts:** say so plainly to the user before doing more Gate A / competition-implementation work, and ask whether it's been settled with Sbu since. Continuing to build as if Lethabo's view already won, without checking, would be building on a premise one of the two people who has to submit this doesn't accept. Content work, design-system work, and anything already framed as "preparation/reference, not a build gate" (per Sbu's own framing) is not in dispute and can continue regardless.

## Read in this order, every new session

1. **This file** — the rules below.
2. [`05_amazwi/P0.md`](05_amazwi/P0.md) — current status of every task, gate table, what's done vs. open. The single source of truth for "where are we."
3. [`05_amazwi/BUILD_LOG.md`](05_amazwi/BUILD_LOG.md) — chronological log, **newest entries at the top**. Read at least the last 5–6 entries to see exactly what just happened and why, including mistakes caught and fixed.
4. [`05_amazwi/README.md`](05_amazwi/README.md) — product contract, settled decisions, file map for the full plan corpus (`05_amazwi/plan/00_MASTER_PLAN.md` onward).
5. [`HANDOVER_SBU.md`](HANDOVER_SBU.md) / [`HANDOVER_LETHABO.md`](HANDOVER_LETHABO.md) — the two teammates' reciprocal handover notes. Check both for anything addressed to you that hasn't been actioned yet.

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

As of 31 Aug 2026, the actual work exists regardless of the disagreement above — what's contested is only whether it counts as *competition build-gate progress* yet, not whether it happened: L1 (Setswana cards, one open item — see below), L2/L3 (Figma design system + craft-pass mockups — Sbu's framing: reference/preparation, recreate on-site), L4 (error copy), L5 (deck skeleton + demo script — Sbu's framing: skeleton only, real screenshots needed on-site), all of `05_amazwi/LETHABO_NEXT_WORK.md`'s items 1–6 (content fixes, stale-mockup reconciliation, five hero screens, real tokens.css theme switching, accessibility evidence — including a keyboard-reachability gap found *and fixed*), and Gate A's Lethabo-half start (routing, tokens wired into a real frontend, an honest Mini-App/browser-mode label, all tested) — **this last one is exactly what Sbu's dispute above is about.** Full detail and exact commit-by-commit record in `BUILD_LOG.md`.

**Still open, not disputed by either side:** L1's four replacement distractors (`moraka`/`jusi`/`ting`/`diphaphatha` in `cards_setswana.json`) need Lethabo's own native read-aloud confirmation before the deck is fully signed off — flagged as a warning by `validate_cards.mjs`, not an error.

**L6 (rehearsal) is deliberately deferred** — Lethabo's call: "we will do L6 later after everything is built." Don't restart it until asked.

## Git discipline

Pull before you start. Push before you stop. Never `git checkout`/`reset`/`clean` without checking `git status` first and stashing anything real. Never force-push. Commit messages explain *why*, not just *what* — match the style already in the log (`git log --oneline`).
