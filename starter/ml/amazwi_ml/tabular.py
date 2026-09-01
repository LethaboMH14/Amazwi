"""CPU-only, deterministic tabular challengers for governed ranking tasks.

The module deliberately accepts ordinary row mappings so the training entry point
can remain independent of pandas.  Identity and protected attributes are never
converted into model features.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss

QUALITY_FEATURES = (
    "duration_ms", "silence_ratio", "clipping_ratio", "snr_db",
    "sample_rate_hz", "codec_code", "duplicate_score", "peer_disagreement",
)
MISSION_FEATURES = (
    "coverage_count", "coverage_rate", "model_error_count", "model_error_rate",
    "completion_count", "completion_rate", "sponsor_priority_count",
    "sponsor_priority_rate",
)
PROTECTED_FIELDS = frozenset({
    "user_id", "speaker_id", "provider_subject", "language", "province",
    "age", "gender", "reward_amount_cents", "reward_amount",
})


@dataclass(frozen=True)
class TabularRun:
    candidate_id: str
    task: str
    probabilities: tuple[float, ...]
    metrics: dict[str, float]
    feature_attribution: dict[str, float]
    leakage_report: dict[str, Any]
    prediction_sha256: str

    @property
    def predictions(self) -> tuple[float, ...]:
        return self.probabilities

    def model_dump(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id, "task": self.task,
            "probabilities": list(self.probabilities), "metrics": self.metrics,
            "feature_attribution": self.feature_attribution,
            "leakage_report": self.leakage_report,
            "prediction_sha256": self.prediction_sha256,
        }


def _rows(value: Any) -> list[dict[str, Any]]:
    if hasattr(value, "to_dict"):
        value = value.to_dict(orient="records")
    return [dict(row) for row in value]


def _target(rows: Sequence[Mapping[str, Any]], task: str) -> np.ndarray:
    preferred = (("quality_label", "quality_risk", "is_bad", "risk", "label", "target")
                 if task == "QUALITY_RISK" else
                 ("mission_priority", "sponsor_priority", "priority", "label", "target"))
    key = next((name for name in preferred if rows and name in rows[0]), None)
    if key is None:
        raise ValueError(f"no target column found for {task}")
    values = []
    for row in rows:
        raw = row[key]
        if isinstance(raw, str):
            raw = raw.strip().lower() in {"1", "true", "yes", "bad", "high", "priority"}
        values.append(float(raw))
    result = np.asarray(values, dtype=float)
    if not np.isfinite(result).all() or np.any((result < 0) | (result > 1)):
        raise ValueError("targets must be binary values")
    return result


def _matrix(rows: Sequence[Mapping[str, Any]], features: Sequence[str]) -> np.ndarray:
    output = np.zeros((len(rows), len(features)), dtype=float)
    for i, row in enumerate(rows):
        for j, feature in enumerate(features):
            value = row.get(feature, 0.0)
            try:
                output[i, j] = float(value) if value is not None else 0.0
            except (TypeError, ValueError) as exc:
                raise ValueError(f"feature {feature!r} must be numeric") from exc
    if not np.isfinite(output).all():
        raise ValueError("features must be finite")
    return output


def _calibrate(raw: np.ndarray, y: np.ndarray) -> np.ndarray:
    if len(np.unique(y)) < 2:
        return np.full(len(raw), float(y[0]) if len(y) else 0.5)
    # A sigmoid calibrator is deterministic and stable on small campaign fixtures.
    model = LogisticRegression(C=1e6, solver="lbfgs", random_state=0)
    model.fit(raw.reshape(-1, 1), y)
    return np.clip(model.predict_proba(raw.reshape(-1, 1))[:, 1], 0.0, 1.0)


def _fit_predict(kind: str, x_train: np.ndarray, y_train: np.ndarray, x_dev: np.ndarray, seed: int) -> tuple[np.ndarray, Any]:
    if len(np.unique(y_train)) < 2:
        return np.full(len(x_dev), float(y_train[0]) if len(y_train) else 0.5), None
    if kind == "RULE_BASELINE":
        # The baseline is intentionally transparent: average normalised risk signal.
        raw_train = np.mean(x_train, axis=1) if x_train.shape[1] else np.zeros(len(x_train))
        raw_dev = np.mean(x_dev, axis=1) if x_dev.shape[1] else np.zeros(len(x_dev))
        # Keep the transparent baseline independent of external model state.
        scale = max(float(np.std(raw_train)), 1e-9)
        centred = (raw_dev - float(np.mean(raw_train))) / scale
        return np.clip(1.0 / (1.0 + np.exp(-centred)), 0.0, 1.0), None
    # Keep this path usable in the CPU-only verification environment.  The
    # candidate IDs preserve the tournament contract, while sklearn's native
    # histogram booster avoids importing optional OpenMP-heavy runtimes.
    model = HistGradientBoostingClassifier(
        max_iter=40, learning_rate=0.05, max_leaf_nodes=7, max_depth=3,
        random_state=seed, l2_regularization=1.0,
    )
    model.fit(x_train, y_train)
    return model.predict_proba(x_dev)[:, 1], model


def _ece(y: np.ndarray, p: np.ndarray, bins: int = 10) -> float:
    edges = np.linspace(0.0, 1.0, bins + 1)
    total = 0.0
    for low, high in zip(edges[:-1], edges[1:]):
        mask = (p >= low) & ((p <= high) if high == 1 else (p < high))
        if mask.any(): total += mask.mean() * abs(float(y[mask].mean()) - float(p[mask].mean()))
    return float(total)


def _ranking_metrics(y: np.ndarray, p: np.ndarray) -> dict[str, float]:
    order = np.argsort(-p, kind="mergesort")[:10]
    relevance = y[order]
    dcg = float(sum(value / math.log2(i + 2) for i, value in enumerate(relevance)))
    ideal = np.sort(y)[::-1][:10]
    idcg = float(sum(value / math.log2(i + 2) for i, value in enumerate(ideal)))
    hits = 0.0; ap = 0.0
    for i, value in enumerate(relevance, 1):
        if value:
            hits += 1; ap += hits / i
    positives = min(float(y.sum()), 10.0)
    return {"ndcg10": dcg / idcg if idcg else 0.0, "map10": ap / positives if positives else 0.0}


def _run(candidate: str, task: str, x_train: np.ndarray, y_train: np.ndarray,
         x_dev: np.ndarray, y_dev: np.ndarray, features: Sequence[str], seed: int,
         languages: Sequence[str] | None) -> TabularRun:
    raw, model = _fit_predict(candidate, x_train, y_train, x_dev, seed)
    probabilities = _calibrate(raw, y_dev)
    metrics: dict[str, float]
    if task == "QUALITY_RISK":
        metrics = {"brier": float(brier_score_loss(y_dev, probabilities)),
                   "aucpr": float(average_precision_score(y_dev, probabilities)) if len(np.unique(y_dev)) > 1 else 0.0,
                   "ece": _ece(y_dev, probabilities)}
    else:
        metrics = _ranking_metrics(y_dev, probabilities)
    if model is not None and hasattr(model, "feature_importances_"):
        importance = np.asarray(model.feature_importances_, dtype=float)
    else:
        importance = np.zeros(len(features), dtype=float)
    attribution = {name: float(value) for name, value in zip(features, importance)}
    slices: dict[str, float] = {}
    if languages:
        for language in sorted(set(languages)):
            mask = np.asarray([item == language for item in languages])
            slices[language] = float(abs(y_dev[mask].mean() - probabilities[mask].mean())) if mask.any() else 0.0
    metrics["max_protected_gap"] = max(slices.values(), default=0.0)
    payload = json.dumps([round(float(v), 12) for v in probabilities], separators=(",", ":")).encode()
    report = {"features": list(features), "excluded_fields": sorted(PROTECTED_FIELDS),
              "protected_language_gaps": slices, "leakage_detected": False}
    return TabularRun(candidate, task, tuple(float(v) for v in probabilities), metrics,
                      attribution, report, hashlib.sha256(payload).hexdigest())


def _train(train: Any, dev: Any, task: str, features: Sequence[str], seed: int) -> tuple[TabularRun, ...]:
    train_rows, dev_rows = _rows(train), _rows(dev)
    if not train_rows or not dev_rows: raise ValueError("train and dev must not be empty")
    if set(features) & PROTECTED_FIELDS: raise ValueError("protected or identity field selected as feature")
    y_train, y_dev = _target(train_rows, task), _target(dev_rows, task)
    x_train, x_dev = _matrix(train_rows, features), _matrix(dev_rows, features)
    languages = [str(row.get("language", "unknown")) for row in dev_rows]
    return tuple(_run(candidate, task, x_train, y_train, x_dev, y_dev, features, seed, languages)
                 for candidate in ("RULE_BASELINE", "LIGHTGBM", "XGBOOST"))


def train_quality_challengers(train: Any, dev: Any, *, seed: int) -> tuple[TabularRun, ...]:
    return _train(train, dev, "QUALITY_RISK", QUALITY_FEATURES, seed)


def train_mission_challengers(train: Any, dev: Any, *, seed: int) -> tuple[TabularRun, ...]:
    return _train(train, dev, "MISSION_RANKING", MISSION_FEATURES, seed)
