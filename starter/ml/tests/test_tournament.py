from amazwi_ml.tournament import CandidateEvidence, evaluate_asr_promotion, rank_candidates


def asr(candidate_id, wer, cer, embedded, worst_slice, **kwargs):
    return CandidateEvidence(candidate_id=candidate_id, metrics={"wer": wer, "cer": cer, "embedded_span_error": embedded, "worst_slice_wer": worst_slice}, **kwargs)


def test_asr_candidate_is_blocked_when_only_wer_passes():
    decision = evaluate_asr_promotion(
        baseline=asr("baseline", .40, .20, .30, .45),
        candidate=asr("candidate", .36, .206, .30, .45),
    )
    assert decision.promoted is False
    assert "CER_REGRESSION" in decision.reason_codes


def test_equal_candidates_use_candidate_id_tie_break():
    ranked = rank_candidates([asr("b", .2, .2, .2, .2), asr("a", .2, .2, .2, .2)], "wer", True)
    assert [x.candidate_id for x in ranked] == ["a", "b"]


def test_asr_pass_requires_evaluation_manifest_and_hashes():
    common = {"evaluation_manifest_sha256": "a" * 64, "artefact_sha256": {name: "b" * 64 for name in ("manifest", "config", "checkpoint", "predictions", "metrics")}}
    decision = evaluate_asr_promotion(asr("base", .4, .2, .3, .4, **common), asr("cand", .36, .2, .3, .4, **common))
    assert decision.promoted is True
