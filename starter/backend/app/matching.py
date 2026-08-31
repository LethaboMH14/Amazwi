"""Answer-matching for the resolver (`plan/02_TECH.md` §6, `plan/13_IS_CORRECT_SPEC.md`).

Cross-lane note: written in Sbu's backend lane per S3 ("write and test
is_correct before implementation") while both lanes are fair game this
session (BUILD_LOG.md, 31 Aug ~23:40). Flagged pending Sbu's review in
BUILD_LOG.md and HANDOVER_SBU.md -- not a money/legal/deployment call, a
mechanical implementation of an already-written spec.

Pipeline is exactly `13_IS_CORRECT_SPEC.md`'s five steps, nothing added:
  1. NFC Unicode normalisation
  2. lowercase
  3. trim leading/trailing whitespace
  4. collapse internal whitespace and hyphens to a single space
  5. exact match against the card's accepted_answers[] (already normalised
     the same way at authoring time)

No edit-distance threshold. No generic noun-class stripping. Explicit
native-reviewed aliases in accepted_answers[] are how known typos/forms
are handled -- not fuzzy matching at runtime.
"""
from __future__ import annotations

import re
import unicodedata

_WS_OR_HYPHEN = re.compile(r"[\s\-]+")


def normalise_answer(raw: str) -> str:
    """Steps 1-4 of the spec pipeline, exposed separately so authoring-time
    normalisation of accepted_answers[] can reuse the identical logic
    is_correct() uses at match time -- one implementation, not two that can
    drift apart."""
    nfc = unicodedata.normalize("NFC", raw)
    lowered = nfc.lower()
    trimmed = lowered.strip()
    collapsed = _WS_OR_HYPHEN.sub(" ", trimmed).strip()
    return collapsed


def is_correct(raw_answer: str, accepted_answers: list[str]) -> bool:
    """Step 5: exact match of the normalised raw answer against the card's
    accepted_answers[], each normalised the same way (accepted_answers are
    meant to already be normalised at authoring time, but re-normalising
    here is cheap and makes the function correct even if a caller passes
    un-normalised content -- it does not add any fuzzy matching)."""
    normalised = normalise_answer(raw_answer)
    return any(normalised == normalise_answer(a) for a in accepted_answers)
