# `is_correct` — matching spec (written before code, per `05_BUILD.md` §1)

Written on paper first per P0 S3. This is the load-bearing correctness function for the resolver in `02_TECH.md` §5. No implementation checked into the starter — application logic is competition scope.

## Signature (intent, not code)

```
is_correct(raw_answer: str, card.accepted_answers: list[str]) -> bool
```

## Pipeline (from `02_TECH.md` §6 — Answer Matching)

1. NFC Unicode normalisation
2. lowercase
3. trim leading/trailing whitespace
4. collapse internal whitespace and hyphens to a single space
5. exact match against the card's `accepted_answers[]` (already normalised the same way at authoring time)

No edit-distance threshold. No generic noun-class stripping. Explicit native-reviewed aliases in `accepted_answers[]` are how known typos/forms are handled for the hero deck — not fuzzy matching at runtime.

## Worked example (structure only — no real card content here)

```
raw:        "  Umoya-Wam "
step 1-4:   "umoya wam"
accepted:   ["umoya wam", "u-moya wam"]  → normalised at authoring to ["umoya wam", "umoya wam"]
match:      true
```

## What this function does NOT decide

- it does not referee the banned-word rule (that's the listener's `violation_vote`, §5 Resolver);
- it does not run without a completed proficient-verifier assignment;
- two independent `is_correct` calls (one per verifier) must both be `true` for `UNDERSTOOD` — see the resolver pseudocode in `02_TECH.md` §5.

## Audit requirement

Store, per assignment: `answer_text` (raw), `answer_normalised`, and the match-rule version. Never overwrite the raw answer.

## Open before implementation

- confirm hyphen-collapse doesn't break isiZulu/Setswana compound forms that are hyphenated in `accepted_answers` on purpose — check against the first 8 hero cards per language when they exist (P0 S2/L1).
