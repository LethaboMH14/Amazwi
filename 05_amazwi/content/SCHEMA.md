# Card content schema — shared by both languages

Canonical fields, from `plan/02_TECH.md` §3 and `plan/05_BUILD.md` §3. Do not diverge from this shape — Lethabo's Setswana file and Sbu's isiZulu file must match exactly so the loader doesn't need per-language branches.

```json
{
  "id": "sw-001",
  "language": "setswana",
  "target": "sefofane",
  "blocked_words": ["fofa", "loapi", "maeto", "boemafofane"],
  "accepted_answers": ["sefofane"],
  "distractors": ["teksi", "koloi", "pere"],
  "campaign_or_deck": "hero-8",
  "active": true,
  "confidence": "DRAFT — needs native verification"
}
```

**Field rules, exactly as specified:**
- `blocked_words` — exactly 4. The four most obvious spoken routes to the target, not a dictionary synonym dump.
- `accepted_answers` — matching is **exact** (NFC normalise, lowercase, trim, collapse whitespace/hyphens). No fuzzy/edit-distance, no noun-class stripping. This means the list must be **exhaustive** — every real variant a verifier might type, or a correct answer gets rejected.
- `distractors` — exactly 3, for the learner MCQ. Plausible wrong answers, not absurd ones.
- `campaign_or_deck` — `"hero-8"` for the eight cards that go in front of judges, `"pool-30"` for the rest.
- `confidence` — not in the production schema; a build-time-only flag so nothing marked DRAFT can reach the pitch. Strip before shipping.

**The eight hero cards need a higher bar than the remaining 22** — they are what a judge sees.

**No placeholder card reaches the pitch.** No illustration appears on a listener screen if it leaks the target.
