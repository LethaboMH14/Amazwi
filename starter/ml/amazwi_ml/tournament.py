from __future__ import annotations
from dataclasses import dataclass,field
@dataclass(frozen=True)
class CandidateEvidence:
 candidate_id:str; metrics:dict[str,float]; manifest_sha256:str; artefact_hashes:dict[str,str]=field(default_factory=dict); slice_metrics:dict[str,tuple[float,int]]=field(default_factory=dict)
@dataclass(frozen=True)
class PromotionDecision: promoted:bool; reason_codes:tuple[str,...]
def rank_candidates(candidates,metric:str,lower_is_better:bool)->tuple:
 def key(c):
  value=c.metrics.get(metric,float("inf") if lower_is_better else float("-inf"))
  return (value if lower_is_better else -value,c.candidate_id)
 return tuple(sorted(candidates,key=key))
def _valid(c):return len(c.manifest_sha256)==64 and all(len(v)==64 for v in c.artefact_hashes.values()) and {"config","checkpoint","predictions","metric_report"}.issubset(c.artefact_hashes)
def evaluate_asr_promotion(baseline:CandidateEvidence,candidate:CandidateEvidence)->PromotionDecision:
 reasons=[]; b=baseline.metrics;c=candidate.metrics
 if candidate.manifest_sha256!=baseline.manifest_sha256:reasons.append("MANIFEST_MISMATCH")
 if not _valid(candidate):reasons.append("MISSING_EVIDENCE")
 if (b["wer"]-c["wer"])/b["wer"]<.05:reasons.append("WER_INSUFFICIENT")
 if c["cer"]-b["cer"]>.005:reasons.append("CER_REGRESSION")
 if c.get("embedded",0)-b.get("embedded",0)>.01:reasons.append("EMBEDDED_REGRESSION")
 for name,(value,count) in candidate.slice_metrics.items():
  old=baseline.slice_metrics.get(name,(value,count))[0]
  if count>=30 and value-old>.02:reasons.append("SLICE_REGRESSION")
 return PromotionDecision(not reasons,tuple(sorted(set(reasons))))
def evaluate_tabular_promotion(baseline,candidate,task:str)->PromotionDecision:
 b=baseline.metrics;c=candidate.metrics;reasons=[]
 if candidate.manifest_sha256!=baseline.manifest_sha256 or not _valid(candidate):reasons.append("EVIDENCE_INVALID")
 if task=="QUALITY_RISK":
  if (b["brier"]-c["brier"])/b["brier"]<.02:reasons.append("BRIER_INSUFFICIENT")
  if c["aucpr"]<b["aucpr"]:reasons.append("AUCPR_REGRESSION")
  if c["ece"]>.05:reasons.append("ECE_TOO_HIGH")
 else:
  if (c["ndcg10"]-b["ndcg10"])/b["ndcg10"]<.02:reasons.append("NDCG_INSUFFICIENT")
  if c["map10"]<b["map10"]:reasons.append("MAP_REGRESSION")
 return PromotionDecision(not reasons,tuple(sorted(set(reasons))))
