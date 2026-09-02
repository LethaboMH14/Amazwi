# Hero-card review — 31 August 2026

> **Superseded review snapshot.** The findings originally recorded here were resolved or replaced later on 31 August. The canonical current state is the structured `review` metadata in `cards_isizulu.json` and `cards_setswana.json`.

## Current outcome

- **isiZulu (`zu`): `REVIEWED`.** Sbu approved all eight targets, blocked words, accepted answers and distractors. There are no pending native-review items.
- **Setswana (`tn`): `REVIEWED`.** Lethabo approved all eight cards, including the later read-aloud confirmation of `moraka` (`sw-004`), `jusi` (`sw-005`), and `ting` plus `diphaphatha` (`sw-007`) on 2 September.
- Both decks now contain eight cards, two or more accepted answers per card, unique IDs, and no accepted-answer overlap with blocked words or distractors.
- Every card carries the same ISO 639-1 language code as its deck: `zu` for isiZulu and `tn` for Setswana.

The Setswana future-target list is intentionally named `future_target_candidates`, not `pool_22_target_candidates`: it currently contains 21 entries, of which 20 are unique beyond the hero deck because `thipa` is already the `sw-003` hero target. No unreviewed Setswana word was invented to make the count look complete.

## Review contract

- `review.status` is either `REVIEWED` or `NEEDS_NATIVE_CONFIRMATION`.
- `review.pending_items` is empty only when the deck is fully reviewed.
- A validator warning for `NEEDS_NATIVE_CONFIRMATION` is an explicit human-review gate; it is not a structural failure and must not be described as native approval.
- Native-language owners retain final authority over words and accepted variants.

## Validation

Run both decks:

```text
node 05_amazwi/content/validate_cards.mjs 05_amazwi/content/cards_isizulu.json
node 05_amazwi/content/validate_cards.mjs 05_amazwi/content/cards_setswana.json
```

The validator checks the structured review state, top-level and per-card language codes, unique card IDs, native-answer minimums, normalised duplicates, and answer overlaps. Errors block import. Warnings name outstanding native confirmation explicitly.
