import pytest

from amazwi_ml.metrics import (
    InvalidReference,
    TokenSpan,
    character_error_rate,
    embedded_span_error,
    normalise_transcript,
    word_error_rate,
)


def test_normalise_transcript_folds_case_and_punctuation():
    assert normalise_transcript("  Sefofane, sefofane!  ") == "sefofane sefofane"


def test_normalise_transcript_nfc_normalises_unicode():
    decomposed = "é"  # "e" + combining acute accent
    precomposed = "é"  # "é"
    assert normalise_transcript(decomposed) == normalise_transcript(precomposed)


def test_wer_zero_for_identical_transcripts():
    assert word_error_rate("the cat sat on the mat", "the cat sat on the mat") == 0.0


def test_wer_one_substitution_over_three_words():
    # "sat" -> "sit" is one substitution out of three reference words
    assert word_error_rate("the cat sat", "the cat sit") == pytest.approx(1 / 3)


def test_wer_one_deletion_over_three_words():
    assert word_error_rate("the cat sat", "the cat") == pytest.approx(1 / 3)


def test_wer_one_insertion_over_three_words():
    assert word_error_rate("the cat sat", "the cat sat now") == pytest.approx(1 / 3)


def test_wer_empty_reference_and_empty_hypothesis_is_zero():
    assert word_error_rate("", "") == 0.0


def test_wer_empty_reference_nonempty_hypothesis_raises():
    with pytest.raises(InvalidReference):
        word_error_rate("", "sefofane")


def test_cer_zero_for_identical_transcripts():
    assert character_error_rate("kgomo", "kgomo") == 0.0


def test_cer_one_substitution_over_five_chars():
    # "kgomo" -> "kgono": one character substitution over five reference chars
    assert character_error_rate("kgomo", "kgono") == pytest.approx(1 / 5)


def test_cer_empty_reference_and_empty_hypothesis_is_zero():
    assert character_error_rate("", "") == 0.0


def test_cer_empty_reference_nonempty_hypothesis_raises():
    with pytest.raises(InvalidReference):
        character_error_rate("", "kgomo")


def test_embedded_span_error_zero_when_span_matches():
    reference = "the target word is sefofane in this sentence"
    hypothesis = "the target word is sefofane in this sentence"
    # "sefofane" is reference token index 4 (0-based), a single-token span
    span = TokenSpan(start=4, end=5, language="setswana")
    assert embedded_span_error(reference, hypothesis, [span]) == 0.0


def test_embedded_span_error_counts_only_errors_inside_the_span():
    reference = "the target word is sefofane in this sentence"
    # error outside the span ("the" -> "a") must not affect the span-only score,
    # error inside the span ("sefofane" -> "kgomo") must be counted
    hypothesis = "a target word is kgomo in this sentence"
    span = TokenSpan(start=4, end=5, language="setswana")
    assert embedded_span_error(reference, hypothesis, [span]) == pytest.approx(1.0)


def test_embedded_span_error_averages_across_multiple_spans():
    reference = "sefofane and kgomo are both target words"
    hypothesis = "sefofane and pere are both target words"
    span_a = TokenSpan(start=0, end=1, language="setswana")  # "sefofane" -> matches
    span_b = TokenSpan(start=2, end=3, language="setswana")  # "kgomo" -> "pere", wrong
    # 0 errors / 1 expected token (span_a) + 1 error / 1 expected token (span_b) = 1 / 2
    assert embedded_span_error(reference, hypothesis, [span_a, span_b]) == pytest.approx(0.5)


def test_embedded_span_error_no_spans_is_zero():
    assert embedded_span_error("the cat sat", "the cat sat", []) == 0.0


def test_embedded_span_error_empty_reference_and_empty_hypothesis_is_zero():
    assert embedded_span_error("", "", []) == 0.0


def test_embedded_span_error_empty_reference_nonempty_hypothesis_raises():
    with pytest.raises(InvalidReference):
        embedded_span_error("", "sefofane", [])
