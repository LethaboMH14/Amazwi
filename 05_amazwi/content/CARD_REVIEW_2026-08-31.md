# Hero-card review — 31 August 2026

## Outcome

The Setswana draft is materially better than the empty worksheet, but it is not import-ready. The isiZulu proposal is useful as a discussion prompt only and remains outside the canonical deck.

## Setswana findings

- All eight cards have a target, four blocked words and three distractors.
- Five cards (`sw-003`, `sw-004`, `sw-006`, `sw-007`, `sw-008`) still have only one accepted answer and therefore fail the canonical minimum of two.
- Four cards reuse a blocked word as a distractor (`sw-003`, `sw-004`, `sw-005`, `sw-007`). Treat this as a review warning: it is not necessarily impossible, but separate options will produce a clearer learner experience.
- Plural accepted answers on `sw-001` and `sw-002` need native confirmation that number-changing answers should count as the same intended semantic label.
- `sw-003` remains ambiguous because *pula* carries weather, currency and motto meanings. Prefer replacing it unless the spoken prompt explicitly establishes the weather sense without leaking the answer.
- `reasoning`, `confidence` and the deck-level `status` are authoring metadata and must be removed or resolved before import.

## isiZulu proposal findings

- Do not convert the proposal into `cards_isizulu.json` without Sbu's native-language pass.
- Most proposed rows have only one accepted answer and therefore do not meet the import gate.
- `ZU-06` and `ZU-07` are explicitly unresolved and must be replaced or disambiguated before play testing.
- Every accepted variant must preserve the intended meaning; grammatical number or a broader/narrower term should not be accepted automatically.

## Validation

Run:

```text
node 05_amazwi/content/validate_cards.mjs 05_amazwi/content/cards_setswana.json
```

The validator checks structure, native-answer minimums, normalised duplicates, answer overlaps and draft status. Warnings require human judgement; errors block import.
