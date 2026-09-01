import pytest

from amazwi_ml.tournament import (
    CandidateEvidence,
    evaluate_asr_promotion,
    evaluate_tabular_promotion,
    rank_candidates,
)

MANIFEST = "a" * 64
OTHER_MANIFEST = "b" * 64
COMPLETE_ARTEFACTS = {
    "config": "1" * 64,
    "checkpoint": "2" * 64,
    "predictions": "3" * 64,
    "metric_report": "4" * 64,
}


def _asr(manifest=MANIFEST, artefacts=None, wer=0.20, cer=0.10, embedded=0.05, slice_metrics=None):
    return CandidateEvidence(
        candidate_id="c",
        metrics={"wer": wer, "cer": cer, "embedded": embedded},
        manifest_sha256=manifest,
        artefact_hashes=COMPLETE_ARTEFACTS if artefacts is None else artefacts,
        slice_metrics=slice_metrics or {},
    )


# ---------------------------------------------------------------------------
# rank_candidates
# ---------------------------------------------------------------------------


def test_rank_candidates_lower_is_better_orders_ascending():
    a = CandidateEvidence("a", {"wer": 0.30}, MANIFEST)
    b = CandidateEvidence("b", {"wer": 0.10}, MANIFEST)
    c = CandidateEvidence("c", {"wer": 0.20}, MANIFEST)
    ranked = rank_candidates([a, b, c], "wer", lower_is_better=True)
    assert [x.candidate_id for x in ranked] == ["b", "c", "a"]


def test_rank_candidates_higher_is_better_orders_descending():
    a = CandidateEvidence("a", {"aucpr": 0.30}, MANIFEST)
    b = CandidateEvidence("b", {"aucpr": 0.90}, MANIFEST)
    c = CandidateEvidence("c", {"aucpr": 0.60}, MANIFEST)
    ranked = rank_candidates([a, b, c], "aucpr", lower_is_better=False)
    assert [x.candidate_id for x in ranked] == ["b", "c", "a"]


def test_rank_candidates_ties_break_on_candidate_id():
    a = CandidateEvidence("zebra", {"wer": 0.10}, MANIFEST)
    b = CandidateEvidence("alpha", {"wer": 0.10}, MANIFEST)
    ranked = rank_candidates([a, b], "wer", lower_is_better=True)
    assert [x.candidate_id for x in ranked] == ["alpha", "zebra"]


def test_rank_candidates_missing_metric_sorts_last_when_lower_is_better():
    has_metric = CandidateEvidence("has", {"wer": 0.10}, MANIFEST)
    missing_metric = CandidateEvidence("missing", {}, MANIFEST)
    ranked = rank_candidates([missing_metric, has_metric], "wer", lower_is_better=True)
    assert [x.candidate_id for x in ranked] == ["has", "missing"]


# ---------------------------------------------------------------------------
# evaluate_asr_promotion
# ---------------------------------------------------------------------------


def test_asr_promotion_passes_with_sufficient_improvement_and_no_regression():
    baseline = _asr(wer=0.20, cer=0.10, embedded=0.05)
    candidate = _asr(wer=0.18, cer=0.10, embedded=0.05)  # 10% relative WER improvement
    decision = evaluate_asr_promotion(baseline, candidate)
    assert decision.promoted is True
    assert decision.reason_codes == ()


def test_asr_promotion_blocks_on_manifest_mismatch():
    baseline = _asr(manifest=MANIFEST, wer=0.20)
    candidate = _asr(manifest=OTHER_MANIFEST, wer=0.10)
    decision = evaluate_asr_promotion(baseline, candidate)
    assert decision.promoted is False
    assert "MANIFEST_MISMATCH" in decision.reason_codes


def test_asr_promotion_blocks_on_missing_evidence():
    baseline = _asr(wer=0.20)
    candidate = _asr(wer=0.10, artefacts={"config": "1" * 64})  # missing 3 required artefacts
    decision = evaluate_asr_promotion(baseline, candidate)
    assert decision.promoted is False
    assert "MISSING_EVIDENCE" in decision.reason_codes


def test_asr_promotion_blocks_on_insufficient_wer_improvement():
    baseline = _asr(wer=0.20, cer=0.10, embedded=0.05)
    candidate = _asr(wer=0.196, cer=0.10, embedded=0.05)  # 2% relative improvement, under 5% bar
    decision = evaluate_asr_promotion(baseline, candidate)
    assert decision.promoted is False
    assert "WER_INSUFFICIENT" in decision.reason_codes


def test_asr_promotion_blocks_on_cer_regression():
    baseline = _asr(wer=0.20, cer=0.10, embedded=0.05)
    candidate = _asr(wer=0.10, cer=0.12, embedded=0.05)  # CER worsens by .02 > .005 threshold
    decision = evaluate_asr_promotion(baseline, candidate)
    assert decision.promoted is False
    assert "CER_REGRESSION" in decision.reason_codes


def test_asr_promotion_blocks_on_embedded_span_regression():
    baseline = _asr(wer=0.20, cer=0.10, embedded=0.05)
    candidate = _asr(wer=0.10, cer=0.10, embedded=0.08)  # embedded worsens by .03 > .01 threshold
    decision = evaluate_asr_promotion(baseline, candidate)
    assert decision.promoted is False
    assert "EMBEDDED_REGRESSION" in decision.reason_codes


def test_asr_promotion_blocks_on_slice_regression_at_sufficient_sample_size():
    baseline = _asr(wer=0.20, cer=0.10, embedded=0.05, slice_metrics={"isizulu": (0.10, 50)})
    candidate = _asr(
        wer=0.10, cer=0.10, embedded=0.05,
        slice_metrics={"isizulu": (0.15, 50)},  # +.05 regression, count >= 30
    )
    decision = evaluate_asr_promotion(baseline, candidate)
    assert decision.promoted is False
    assert "SLICE_REGRESSION" in decision.reason_codes


def test_asr_promotion_ignores_slice_regression_below_sample_threshold():
    baseline = _asr(wer=0.20, cer=0.10, embedded=0.05, slice_metrics={"isizulu": (0.10, 10)})
    candidate = _asr(
        wer=0.10, cer=0.10, embedded=0.05,
        slice_metrics={"isizulu": (0.30, 10)},  # large regression but count < 30
    )
    decision = evaluate_asr_promotion(baseline, candidate)
    assert decision.promoted is True
    assert decision.reason_codes == ()


def test_asr_promotion_can_accumulate_multiple_reasons():
    baseline = _asr(manifest=MANIFEST, wer=0.20, cer=0.10, embedded=0.05)
    candidate = _asr(manifest=OTHER_MANIFEST, wer=0.196, cer=0.12, embedded=0.05)
    decision = evaluate_asr_promotion(baseline, candidate)
    assert decision.promoted is False
    assert set(decision.reason_codes) == {"MANIFEST_MISMATCH", "WER_INSUFFICIENT", "CER_REGRESSION"}


# ---------------------------------------------------------------------------
# evaluate_tabular_promotion
# ---------------------------------------------------------------------------


def _tabular(metrics, manifest=MANIFEST, artefacts=COMPLETE_ARTEFACTS):
    return CandidateEvidence("c", metrics, manifest, artefacts)


def test_tabular_quality_risk_promotion_passes():
    baseline = _tabular({"brier": 0.20, "aucpr": 0.70, "ece": 0.02})
    candidate = _tabular({"brier": 0.15, "aucpr": 0.75, "ece": 0.02})  # 25% brier improvement
    decision = evaluate_tabular_promotion(baseline, candidate, task="QUALITY_RISK")
    assert decision.promoted is True
    assert decision.reason_codes == ()


def test_tabular_quality_risk_blocks_on_insufficient_brier_improvement():
    baseline = _tabular({"brier": 0.20, "aucpr": 0.70, "ece": 0.02})
    candidate = _tabular({"brier": 0.199, "aucpr": 0.70, "ece": 0.02})  # ~0.5% improvement
    decision = evaluate_tabular_promotion(baseline, candidate, task="QUALITY_RISK")
    assert decision.promoted is False
    assert "BRIER_INSUFFICIENT" in decision.reason_codes


def test_tabular_quality_risk_blocks_on_aucpr_regression():
    baseline = _tabular({"brier": 0.20, "aucpr": 0.70, "ece": 0.02})
    candidate = _tabular({"brier": 0.15, "aucpr": 0.60, "ece": 0.02})
    decision = evaluate_tabular_promotion(baseline, candidate, task="QUALITY_RISK")
    assert decision.promoted is False
    assert "AUCPR_REGRESSION" in decision.reason_codes


def test_tabular_quality_risk_blocks_on_ece_too_high():
    baseline = _tabular({"brier": 0.20, "aucpr": 0.70, "ece": 0.02})
    candidate = _tabular({"brier": 0.15, "aucpr": 0.75, "ece": 0.10})
    decision = evaluate_tabular_promotion(baseline, candidate, task="QUALITY_RISK")
    assert decision.promoted is False
    assert "ECE_TOO_HIGH" in decision.reason_codes


def test_tabular_mission_ranking_promotion_passes():
    baseline = _tabular({"ndcg10": 0.50, "map10": 0.40})
    candidate = _tabular({"ndcg10": 0.55, "map10": 0.45})  # 10% relative ndcg improvement
    decision = evaluate_tabular_promotion(baseline, candidate, task="MISSION_RANKING")
    assert decision.promoted is True
    assert decision.reason_codes == ()


def test_tabular_mission_ranking_blocks_on_insufficient_ndcg_improvement():
    baseline = _tabular({"ndcg10": 0.50, "map10": 0.40})
    candidate = _tabular({"ndcg10": 0.505, "map10": 0.40})  # 1% relative improvement
    decision = evaluate_tabular_promotion(baseline, candidate, task="MISSION_RANKING")
    assert decision.promoted is False
    assert "NDCG_INSUFFICIENT" in decision.reason_codes


def test_tabular_mission_ranking_blocks_on_map_regression():
    baseline = _tabular({"ndcg10": 0.50, "map10": 0.40})
    candidate = _tabular({"ndcg10": 0.55, "map10": 0.30})
    decision = evaluate_tabular_promotion(baseline, candidate, task="MISSION_RANKING")
    assert decision.promoted is False
    assert "MAP_REGRESSION" in decision.reason_codes


def test_tabular_promotion_blocks_on_invalid_evidence():
    baseline = _tabular({"brier": 0.20, "aucpr": 0.70, "ece": 0.02})
    candidate = _tabular({"brier": 0.15, "aucpr": 0.75, "ece": 0.02}, artefacts={})
    decision = evaluate_tabular_promotion(baseline, candidate, task="QUALITY_RISK")
    assert decision.promoted is False
    assert "EVIDENCE_INVALID" in decision.reason_codes
