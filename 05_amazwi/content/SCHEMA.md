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
- `campaign_or_deck` — `"hero-8"` for the eight cards that go in front of judges, `"pool-30"` for the rest. This is an **authoring-time label**, not the `campaign_id` FK that `02_TECH.md` §3's `Card` record actually stores. The Gate A seed script maps each label to a real seeded `Campaign` row's `id` on import (`hero-8` → the demo campaign, `pool-30` → the same campaign until a second one exists) — content files never carry a UUID directly.
- `confidence` — not in the production schema; a build-time-only flag so nothing marked DRAFT can reach the pitch. Strip before shipping.

**The eight hero cards need a higher bar than the remaining 22** — they are what a judge sees.

**No placeholder card reaches the pitch.** No illustration appears on a listener screen if it leaks the target.

**Build-gate check (Gate A, before card import):** the loader rejects any card where `confidence` is still `"DRAFT..."`, any `blocked_words`/`distractors` entry is `""`, or `accepted_answers` has fewer than 2 entries (the bare target alone is not exhaustive — see field rule above). This is a hard reject, not a warning, so an under-filled card cannot silently reach a verifier screen.
