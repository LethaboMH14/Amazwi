# Sibusiso — Platform, MoMo and Trust Runbook

Use this alongside `P0.md`, `plan/02_TECH.md` and `plan/05_BUILD.md`. It is a decision checklist, not a timeline. Never place credentials, API keys, MSISDNs or callback URLs in this repository.

## S1 — MoMo readiness

1. Sign into the MoMo developer portal using the team account.
2. Confirm whether **Collections** and **Disbursements** are separately subscribable for the hackathon sandbox.
3. Open the in-portal API reference and testing page. Record only the capability outcome in `BUILD_LOG.md`: available, unavailable, or unknown.
4. If a safe sandbox call is permitted, reserve one clean API user/credential set for the final demo. Do not use automated tests against the sandbox.
5. If Disbursements is unavailable, freeze `DEMO_PROVIDER` for cash-out. If Collections is available, it may be the one real proof; otherwise use labelled seeded funding.
6. Record provider mode, settlement currency and disclosure copy in the receipt contract before frontend integration.

**Exit:** every payment leg is one of `SANDBOX_COLLECTIONS`, `SANDBOX_DISBURSEMENT`, `DEMO_PROVIDER` or seeded funding, and the UI can state which one it is without ambiguity.

## S2 — isiZulu hero cards

Author eight cards in `content/cards_isizulu.json` only after you can validate every field aloud. Each card needs:

- one describable target;
- exactly four natural blocked words;
- at least two native-reviewed accepted answer forms after normalisation;
- exactly three plausible learner distractors;
- a short play-aloud check proving the clue can avoid the target.

The import gate intentionally rejects DRAFT cards, blank fields and a single accepted answer. Do not weaken it to make the deck import.

## S3 — matching and resolver contract

The matching rule is already frozen in `plan/13_IS_CORRECT_SPEC.md`:

- NFC normalise, lowercase, trim and collapse spaces/hyphens;
- exact match against native-curated accepted answers;
- no blanket noun-class stripping;
- no broad edit-distance threshold.

Before coding, add test cases from the completed isiZulu and Setswana hero cards: accepted spelling, accepted alias, rejected near word and rejected empty answer.

## S4–S5 — code boundary

The current `starter/` is generic scaffolding only. Keep product-specific API routes, schema, resolver, ledger and MoMo implementation for Gate A onward, unless the organiser explicitly approves pre-built product code in writing.

At Gate A, your exit conditions are: API health, database migration, deployment, provider configuration and a reproducible reset on both laptops.

## S6 — organiser message

Use `ORGANISER_EMAIL_DRAFT.md`. Copy the answer into `BUILD_LOG.md` and update the relevant canonical plan section; do not rely on memory or an oral reply.

## Non-negotiable truth checks

- Never call a demo-provider credit a real payment.
- Never show a Rand amount beside a sandbox-EUR reference without the disclosure string.
- Never log raw audio URLs, bearer tokens, API keys or phone numbers.
- Never let one verifier or learner MCQ create an eligible contribution.
- Never make an unavailable MoMo leg a reason the whole demo cannot run.
