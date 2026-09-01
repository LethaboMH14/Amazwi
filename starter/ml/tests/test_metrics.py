import pytest

from amazwi_ml.metrics import (
    AsrCase,
    InvalidReference,
    TokenSpan,
    character_error_rate,
    embedded_span_error,
    evaluate_asr,
    normalise_transcript,
    word_error_rate,
)


def test_wer_cer_and_embedded_span_are_exact():
    ref = "ngicela buy airtime manje"
    hyp = "ngicela bye airtime manje"
    assert word_error_rate(ref, hyp) == pytest.approx(0.25)
    assert character_error_rate(ref, hyp) == pytest.approx(2 / 22)
    assert embedded_span_error(ref, hyp, [TokenSpan(start=1, end=3, language="en")]) == pytest.approx(0.5)


def test_empty_reference_policy_is_explicit():
    assert word_error_rate("", "") == 0.0
    with pytest.raises(InvalidReference):
        word_error_rate("", "speech")


def test_normalisation_is_unicode_and_punctuation_stable():
    assert normalise_transcript("  Café,\u0301!  BUY\t airtime. ") == "café buy airtime"


def test_evaluate_asr_reports_deterministic_slices():
    cases = [
        AsrCase(case_id="b", reference="hello world", hypothesis="hello word", language="zu", speaker_id="s2", domain="general", acoustic_condition="clean"),
        AsrCase(case_id="a", reference="buy airtime", hypothesis="buy airtime", language="tn", speaker_id="s1", domain="commerce", acoustic_condition="noisy"),
    ]
    report = evaluate_asr(cases)
    assert report.case_count == 2
    assert [slice_.name for slice_ in report.slices] == ["aggregate", "commerce", "general", "tn", "zu", "acoustic:clean", "acoustic:noisy"]
    with pytest.raises(ValueError):
        evaluate_asr(cases + [cases[0]])
