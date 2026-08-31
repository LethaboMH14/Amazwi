# AMAZWI — PRODUCT CONTRACT
### The game, user roles, validation rule, rewards and screens

**Parent:** `00_MASTER_PLAN.md`
**Product owner:** Lethabo
**Platform counterpart:** Sbu

---

## 1. ONE LOOP, THREE SEATS

### Speaker

Receives a target and four blocked words, records a short clue and earns a published honorarium only when the contribution becomes `CORPUS_ELIGIBLE`.

### Proficient verifier

Listens privately, types the intended concept before reveal, then reports whether the speaker used the target or a blocked word. Two independent verifiers are required. Verifiers earn Voice Points in the competition build, not cash.

### Learner/player

Plays the accessible four-option guessing version for XP, feedback, streak and league status. MCQ answers are game telemetry only and cannot make a recording corpus-eligible.

The UI must never call these three evidence levels the same thing.

---

## 2. CORE MODE — DESCRIBE & GUESS

The competition builds one mode.

1. The speaker sees a native-authored target and four blocked words.
2. They receive a 30-second recording window.
3. The client checks duration, silence and clipping before upload.
4. Two proficient verifiers receive the clip independently.
5. Each types the intended concept.
6. Only after submitting does each see the target and blocked list.
7. Each answers: **“Did the speaker say the answer or one of these blocked words?”**
8. Two accepted free-text answers and fewer than two violation flags produce `UNDERSTOOD`.
9. Audio quality plus active purpose consent produces `CORPUS_ELIGIBLE`.
10. Exactly one reward event is credited and a Voice Value Receipt is created.

Two violation votes produce `VOIDED`. A split referee vote produces `REVIEW_REQUIRED`; the contribution does not silently pay or enter the eligible set.

---

## 3. WHAT A GUESS PROVES

A matched free-text guess proves that two assigned proficient listeners independently recovered the card's intended semantic concept.

It does not prove:

- the words spoken verbatim;
- the declared language;
- speaker identity or uniqueness;
- dialect or place authenticity;
- ASR training readiness;
- proficiency of the speaker or listener.

Player-facing copy may say **“two people understood you.”** Buyer-facing copy says **“peer-verified semantic label.”** Neither says “transcript.”

---

## 4. ANSWER MATCHING

Every card stores:

```text
target
blocked_words[]
accepted_answers[]
distractors[]
language
difficulty_tag
campaign_or_deck
```

Competition matching is intentionally conservative:

1. Unicode-normalise, lowercase, trim and collapse spaces/hyphens.
2. Compare with the first-language-authored `accepted_answers` list.
3. Add explicit typo aliases only for the eight hero cards when native reviewers agree.
4. Do not strip noun-class prefixes generically.
5. Do not use blanket Levenshtein distance on short words.
6. An unmatched answer is false for automatic resolution and is logged for later curation.

This is not a general isiZulu or Setswana morphology engine. It is a safe matcher for a small native-curated deck.

---

## 5. PAYMENT AND POINTS

### Cash

- Speakers receive the published contribution honorarium.
- Cash is credited after `CORPUS_ELIGIBLE`, once per contribution.
- The amount is displayed before recording and never reduced retroactively.
- The app credits its internal ledger immediately.
- Cash-out to MoMo happens at the provider's viable threshold; it is not promised per R2 clip.
- No leaderboard, streak, random event or popularity vote awards cash.

### Voice Points

- Learners and verifiers receive Voice Points for completed eligible play.
- Points unlock tier movement and streak feedback only.
- Points are not convertible to cash.
- Gold checks may suspend point earning when a verifier repeatedly fails attention checks.

The competition does not pay R0.50 per listener judgement. That policy and its economics are removed from the build.

---

## 6. GAMEPLAY VERSUS GOVERNED VALIDATION

| Input | Player result | Data result |
|---|---|---|
| Four-option MCQ | XP, reveal and popularity signal | `PLAYED` only |
| One proficient free-text match | XP and partial evidence | still `OPEN` |
| Two proficient free-text matches | understanding result | `UNDERSTOOD` |
| Two matches + quality + consent + no joint violation | reward and receipt | `CORPUS_ELIGIBLE` |

If fewer than two proficient verifiers respond, the clip expires as `UNVALIDATED` and is excluded from export. Any goodwill payment policy belongs to a later pilot and must be modelled before it is promised.

---

## 7. LANGUAGE AND CONTENT

The launch languages are:

- **isiZulu — Sbu owns the content and in-language copy**;
- **Setswana — Lethabo owns the content and in-language copy**.

Each language has eight hero cards for the demo. Additional cards are useful only after those sixteen are tested aloud.

Card rules:

- culturally authored, not mechanically translated from English;
- concrete enough to explain in 30 seconds;
- blocked words are the obvious routes to the answer;
- accepted answers are curated by the first-language owner;
- illustrations appear only for the speaker if they do not reveal the answer;
- no listener illustration may leak the target;
- the competition demo uses a reviewed English functional shell for reliability; first-language cards and error copy remain language-specific. A declared-language shell is a post-P0 improvement once both language packs are complete.

Future **MoMo Moments** cards elicit domain-specific intent labels such as buy airtime, send money or check a balance. They are roadmap, not required for the core demo.

---

## 8. SCREENS

### 1. Entry

Mini App identity when available; otherwise a clearly labelled browser-demo identity. Adult confirmation and language selection.

### 2. Consent

Required scopes for recording, assigned-verifier playback and stated retention purpose. Public audio/attribution is not requested in the competition build.

### 3. Home

One dominant **PLAY** action, today's contribution allowance, Voice Points, wallet credit and current mission. No feature catalogue.

### 4. Card

Target dominates. Four blocked words. Reward rule and mission are visible before recording.

### 5. Recording

Real waveform, timer, quiet/clipping guidance and retry. No model claims.

### 6. Submitted

“Waiting for two proficient listeners.” The UI never says three.

### 7. Verifier

Playback, free-text answer, then reveal and referee tap. The answer cannot be changed after reveal.

### 8. Learner guest round

Four options, XP and reveal. A plain note says the round does not decide corpus eligibility.

### 9. Result

“Two people understood you” or an honest voided/unvalidated state. Reward is **credited**, not “paid,” until provider confirmation.

### 10. Wallet and Voice Value Receipt

Pending credit, available balance, cash-out submitted, paid and failed states remain distinct. Receipt includes contribution ID, semantic label, validation evidence, reward rule, consent version and provider reference/state.

### 11. Impact Map

Aggregate counts and dots by broad geography/language only. No public raw audio, name or precise location.

### 12. Compact mission view

Funds remaining, eligible contributions, eligible seconds and acceptance rate. No WER chart.

---

## 9. CONSENT AND REVOCATION

Consent scopes:

1. record/process this round;
2. private playback to assigned verifiers;
3. retain for the stated governed purpose;
4. public audio or named attribution.

Scope 4 is off by default and not implemented.

The receipt may offer the contributor a private replay of their own clip only while recording consent remains active. It is not public playback, does not create an archive, and disappears when consent is revoked.

Revocation:

- blocks new contributions until fresh consent;
- removes the audio from future playback and export;
- leaves an audit tombstone and financial record;
- does not claw back earned money;
- does not promise instant unlearning from a model.

---

## 10. GAMIFICATION

Competition gamification stays light:

- one daily quest;
- Voice Points;
- a forgiving streak with one freeze;
- a tiered language/place league only if P0 is complete;
- no national last place;
- no “you lost” state;
- no cash or prizes attached to ranking;
- no chance mechanics, loot boxes, spin or paid entry.
- learner MCQ earns XP only. Do not show learner-guess counts to speakers in P0; they add a gameability surface without proving eligibility.

IRT, Elo, adaptive difficulty and proficiency credentials are roadmap research, not competition features. The complete evidence remains in `../research/F_GAMIFICATION.md`.

---

## 11. COMPETITION ACCEPTANCE CRITERIA

The product is demo-ready when:

- one device records a real clip;
- a second and third device independently verify it;
- one rule violation path can be demonstrated;
- retries cannot create a second reward;
- the wallet shows the correct provider state;
- the receipt renders from real stored events;
- reset returns the demo to a known state;
- MCQ guest play cannot change corpus eligibility;
- revoked audio cannot be assigned or exported;
- all user-facing isiZulu and Setswana hero-card copy is first-language checked.

Everything else is optional.
