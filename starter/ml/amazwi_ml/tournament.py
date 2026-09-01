"""Deterministic advisory tournament gates. No deployment state is mutated."""
from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any, Literal, Sequence

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class CandidateEvidence:
    candidate_id: str
    metrics: dict[str, float] = field(default_factory=dict)
    slices: dict[str, dict[str, float]] = field(default_factory=dict)
    artefact_sha256: dict[str, str] = field(default_factory=dict)
    evaluation_manifest_sha256: str = ""
    artefact_hashes: dict[str, str] | None = None
    status: str = "EVALUATED"

    def metric(self, name: str) -> float | None:
        value = self.metrics.get(name)
        return None if value is None else float(value)


@dataclass(frozen=True)
class PromotionPolicy:
    asr_wer_relative_reduction: float = 0.05
    asr_max_cer_regression: float = 0.005
    asr_max_embedded_regression: float = 0.01
    asr_max_slice_wer_regression: float = 0.02
    min_slice_references: int = 30
    tabular_relative_improvement: float = 0.02
    max_calibration_error: float = 0.05
    max_protected_gap_increase: float = 0.02


@dataclass(frozen=True)
class PromotionDecision:
    promoted: bool
    candidate_id: str
    reason_codes: tuple[str, ...] = ()
    policy: PromotionPolicy = field(default_factory=PromotionPolicy)

    def model_dump(self) -> dict[str, Any]:
        return {"candidate_id": self.candidate_id, "promoted": self.promoted, "reason_codes": list(self.reason_codes)}


def rank_candidates(candidates: Sequence[CandidateEvidence], metric: str, lower_is_better: bool) -> tuple[CandidateEvidence, ...]:
    missing = float("inf") if lower_is_better else float("-inf")
    return tuple(sorted(candidates, key=lambda c: (c.metric(metric) if c.metric(metric) is not None else missing, c.candidate_id), reverse=not lower_is_better))


def _relative_improvement(base: float | None, candidate: float | None, threshold: float) -> bool:
    return base is not None and candidate is not None and base > 0 and (base - candidate) / base >= threshold - 1e-12


def _hashes_valid(evidence: CandidateEvidence) -> bool:
    required = ("manifest", "config", "checkpoint", "predictions", "metrics")
    hashes = evidence.artefact_hashes if evidence.artefact_hashes is not None else evidence.artefact_sha256
    return all(_SHA256.fullmatch(hashes.get(key, "")) for key in required)


def evaluate_asr_promotion(baseline: CandidateEvidence, candidate: CandidateEvidence, policy: PromotionPolicy | None = None) -> PromotionDecision:
    policy = policy or PromotionPolicy()
    reasons: list[str] = []
    bw, cw = baseline.metric("wer"), candidate.metric("wer")
    bc, cc = baseline.metric("cer"), candidate.metric("cer")
    be, ce = baseline.metric("embedded_span_error"), candidate.metric("embedded_span_error")
    if not _relative_improvement(bw, cw, policy.asr_wer_relative_reduction): reasons.append("WER_RELATIVE_REDUCTION")
    if bc is None or cc is None or cc - bc > policy.asr_max_cer_regression + 1e-12: reasons.append("CER_REGRESSION")
    if be is None or ce is None or ce - be > policy.asr_max_embedded_regression + 1e-12: reasons.append("EMBEDDED_SPAN_REGRESSION")
    for name, values in sorted(candidate.slices.items()):
        base = baseline.slices.get(name, {})
        refs = values.get("reference_count", values.get("references", 0))
        if refs >= policy.min_slice_references and "wer" in values and "wer" in base and values["wer"] - base["wer"] > policy.asr_max_slice_wer_regression + 1e-12:
            reasons.append("SLICE_WER_REGRESSION"); break
    if not _hashes_valid(candidate): reasons.append("INVALID_ARTEFACT_HASH")
    if not candidate.evaluation_manifest_sha256 or candidate.evaluation_manifest_sha256 != baseline.evaluation_manifest_sha256: reasons.append("EVALUATION_MANIFEST_MISMATCH")
    return PromotionDecision(not reasons, candidate.candidate_id, tuple(sorted(set(reasons))), policy)


def evaluate_tabular_promotion(baseline: CandidateEvidence, candidate: CandidateEvidence, task: Literal["QUALITY_RISK", "MISSION_RANKING"], policy: PromotionPolicy | None = None) -> PromotionDecision:
    policy = policy or PromotionPolicy(); reasons: list[str] = []
    if task == "QUALITY_RISK":
        if not _relative_improvement(baseline.metric("brier"), candidate.metric("brier"), policy.tabular_relative_improvement): reasons.append("BRIER_RELATIVE_IMPROVEMENT")
        if baseline.metric("aucpr") is None or candidate.metric("aucpr") is None or candidate.metric("aucpr") < baseline.metric("aucpr") - 1e-12: reasons.append("AUCPR_REGRESSION")
        if candidate.metric("ece") is None or candidate.metric("ece") > policy.max_calibration_error + 1e-12: reasons.append("ECE_LIMIT")
    elif task == "MISSION_RANKING":
        base, new = baseline.metric("ndcg10"), candidate.metric("ndcg10")
        if base is None or new is None or base <= 0 or (new - base) / base < policy.tabular_relative_improvement - 1e-12: reasons.append("NDCG_RELATIVE_IMPROVEMENT")
        if baseline.metric("map10") is None or candidate.metric("map10") is None or candidate.metric("map10") < baseline.metric("map10") - 1e-12: reasons.append("MAP_REGRESSION")
    else: raise ValueError(f"unknown tabular task: {task}")
    base_gap, new_gap = baseline.metric("max_protected_gap"), candidate.metric("max_protected_gap")
    if base_gap is None or new_gap is None or new_gap > base_gap + policy.max_protected_gap_increase + 1e-12: reasons.append("PROTECTED_GAP_REGRESSION")
    return PromotionDecision(not reasons, candidate.candidate_id, tuple(sorted(set(reasons))), policy)
