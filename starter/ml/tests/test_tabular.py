import hashlib

from amazwi_ml.tabular import QUALITY_FEATURES, train_quality_challengers


def _rows():
    return [
        {**dict.fromkeys(QUALITY_FEATURES, 0.0), "duration_ms": 100 + i,
         "silence_ratio": i / 10, "language": "zu" if i % 2 else "en",
         "user_id": f"u{i}", "quality_label": i % 2}
        for i in range(8)
    ]


def test_quality_challengers_are_deterministic():
    rows = _rows()
    first = train_quality_challengers(rows[:6], rows[6:], seed=20260901)
    second = train_quality_challengers(rows[:6], rows[6:], seed=20260901)
    assert [run.prediction_sha256 for run in first] == [run.prediction_sha256 for run in second]
    assert [run.candidate_id for run in first] == ["RULE_BASELINE", "LIGHTGBM", "XGBOOST"]


def test_protected_and_identity_fields_are_not_features():
    assert set(QUALITY_FEATURES).isdisjoint({"user_id", "speaker_id", "provider_subject",
                                             "language", "province", "age", "gender",
                                             "reward_amount_cents"})
    run = train_quality_challengers(_rows()[:6], _rows()[6:], seed=1)[0]
    assert run.leakage_report["leakage_detected"] is False
    assert "user_id" not in run.leakage_report["features"]


def test_prediction_hash_matches_canonical_predictions():
    run = train_quality_challengers(_rows()[:6], _rows()[6:], seed=1)[0]
    payload = str([round(value, 12) for value in run.probabilities]).replace("'", '"').replace(" ", "")
    assert run.prediction_sha256 == hashlib.sha256(payload.encode()).hexdigest()


def test_challengers_report_calibration_and_protected_language_slices():
    """Plan 02's tabular acceptance item requires *calibration* and a
    protected-language leakage audit as recorded evidence, not merely a
    deterministic prediction hash. brier/ece/aucpr and the per-language
    gap are computed in amazwi_ml/tabular.py but nothing asserted them,
    so a regression that silently dropped them would still have passed.
    """
    runs = train_quality_challengers(_rows()[:6], _rows()[6:], seed=20260901)
    assert [run.candidate_id for run in runs] == ["RULE_BASELINE", "LIGHTGBM", "XGBOOST"]
    for run in runs:
        for key in ("brier", "ece", "aucpr", "max_protected_gap"):
            assert key in run.metrics, f"{run.candidate_id} is missing {key}"
            assert 0.0 <= run.metrics[key] <= 1.0, f"{run.candidate_id}.{key} out of range"
        assert all(0.0 <= p <= 1.0 for p in run.probabilities), "probabilities must be calibrated"
        gaps = run.leakage_report["protected_language_gaps"]
        assert set(gaps) == {"en", "zu"}, "both dev languages must be audited"
        assert run.metrics["max_protected_gap"] == max(gaps.values())
        # Attribution must name exactly the features actually used --
        # never a protected or identity field.
        assert set(run.feature_attribution) == set(QUALITY_FEATURES)


def test_challenger_attribution_and_metrics_are_deterministic():
    first = train_quality_challengers(_rows()[:6], _rows()[6:], seed=20260901)
    second = train_quality_challengers(_rows()[:6], _rows()[6:], seed=20260901)
    assert [run.feature_attribution for run in first] == [run.feature_attribution for run in second]
    assert [run.metrics for run in first] == [run.metrics for run in second]
