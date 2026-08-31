"""Unit tests for is_correct() against `plan/13_IS_CORRECT_SPEC.md`.

Covers: accepted answers (incl. case/whitespace/hyphen variation), rejected
answers (distractors and blocked_words from the real hero decks -- a
distractor or banned word must never accidentally match), and the spec's
own open item (hyphen-collapse safety against real hyphenated/compound
accepted_answers, checked against both hero-8 decks per its own
instruction: "check against the first 8 hero cards per language when they
exist (P0 S2/L1)").
"""
from __future__ import annotations

import json
from pathlib import Path

from app.matching import is_correct, normalise_answer

REPO_ROOT = Path(__file__).resolve().parents[3]
ZULU_CARDS = REPO_ROOT / "05_amazwi" / "content" / "cards_isizulu.json"
SETSWANA_CARDS = REPO_ROOT / "05_amazwi" / "content" / "cards_setswana.json"


def _load_hero_8(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["hero_8"]


# --- normalise_answer() pipeline steps in isolation ---


def test_nfc_normalises_unicode_forms():
    # combining-acute vs precomposed acute -- same visible char, different bytes
    decomposed = "e\u0301"  # e + combining acute
    precomposed = "\u00e9"  # é
    assert normalise_answer(decomposed) == normalise_answer(precomposed)


def test_lowercases():
    assert normalise_answer("SEFOFANE") == "sefofane"


def test_trims_outer_whitespace():
    assert normalise_answer("  kgomo  ") == "kgomo"


def test_collapses_internal_whitespace():
    assert normalise_answer("ingubo   yokulala") == "ingubo yokulala"


def test_collapses_hyphens_to_space():
    assert normalise_answer("u-moya wam") == "u moya wam"


def test_collapses_mixed_hyphen_and_whitespace_runs():
    assert normalise_answer("a -- b") == "a b"


# --- is_correct(): accepted answers ---


def test_exact_match_accepted():
    assert is_correct("sefofane", ["sefofane", "difofane"]) is True


def test_case_insensitive_match():
    assert is_correct("Sefofane", ["sefofane"]) is True


def test_whitespace_insensitive_match():
    assert is_correct("  sefofane ", ["sefofane"]) is True


def test_reviewed_alias_answer_matches():
    # a second, explicitly authored accepted form (e.g. plural/alt) matches
    assert is_correct("difofane", ["sefofane", "difofane"]) is True


def test_multiword_accepted_answer_matches_with_extra_spacing():
    assert is_correct("ingubo    yokulala", ["ingubo yokulala"]) is True


# --- is_correct(): rejected answers ---


def test_unrelated_word_rejected():
    assert is_correct("koloi", ["sefofane", "difofane"]) is False


def test_empty_answer_rejected():
    assert is_correct("", ["sefofane"]) is False


def test_partial_prefix_not_matched_no_blanket_stripping():
    # is_correct must NOT do generic prefix stripping -- a bare stem must
    # not match a noun-class-prefixed accepted answer or vice versa
    assert is_correct("fofane", ["sefofane", "difofane"]) is False


def test_near_miss_typo_not_matched_no_fuzzy():
    # one-character edit distance -- explicitly out of scope per spec
    # ("No edit-distance threshold")
    assert is_correct("sefofani", ["sefofane", "difofane"]) is False


# --- against the real hero-8 decks: accepted answers all match themselves ---


def test_every_isizulu_hero_card_accepted_answer_matches_itself():
    for card in _load_hero_8(ZULU_CARDS):
        for answer in card["accepted_answers"]:
            assert is_correct(answer, card["accepted_answers"]) is True, card["id"]


def test_every_setswana_hero_card_accepted_answer_matches_itself():
    for card in _load_hero_8(SETSWANA_CARDS):
        for answer in card["accepted_answers"]:
            assert is_correct(answer, card["accepted_answers"]) is True, card["id"]


# --- against the real hero-8 decks: distractors/blocked_words never match ---


def test_no_isizulu_distractor_or_blocked_word_matches_its_own_card():
    for card in _load_hero_8(ZULU_CARDS):
        for word in card["distractors"] + card["blocked_words"]:
            assert is_correct(word, card["accepted_answers"]) is False, (
                card["id"], word
            )


def test_no_setswana_distractor_or_blocked_word_matches_its_own_card():
    for card in _load_hero_8(SETSWANA_CARDS):
        for word in card["distractors"] + card["blocked_words"]:
            assert is_correct(word, card["accepted_answers"]) is False, (
                card["id"], word
            )


# --- spec's own open item: hyphen-collapse safety on the real hero decks ---


def test_no_hero_card_accepted_answer_contains_a_hyphen_today():
    """Spec's open item: 'confirm hyphen-collapse doesn't break isiZulu/
    Setswana compound forms that are hyphenated in accepted_answers on
    purpose -- check against the first 8 hero cards per language when they
    exist.' As of this check, neither hero-8 deck uses a hyphenated
    accepted_answers form (compounds like 'ingubo yokulala' are
    space-separated, not hyphenated), so hyphen-collapsing is safe against
    real content today. If a future card deliberately hyphenates an
    accepted answer, this test will fail and the open item must be
    re-resolved, not silently left green."""
    for path in (ZULU_CARDS, SETSWANA_CARDS):
        for card in _load_hero_8(path):
            for answer in card["accepted_answers"]:
                assert "-" not in answer, (path.name, card["id"], answer)
