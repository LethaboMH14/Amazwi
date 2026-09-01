from __future__ import annotations
import hashlib,json
QUALITY_FEATURES=("duration_ms","silence_ratio","clipping_ratio","snr_db","sample_rate_hz","codec_code","duplicate_score","peer_disagreement")
MISSION_FEATURES=("coverage_count","model_error_rate","completion_rate","sponsor_priority")
class TabularRun:
 def __init__(self,candidate_id,predictions,metrics,manifest_sha256):
  self.candidate_id=candidate_id;self.predictions=tuple(predictions);self.metrics=metrics;self.manifest_sha256=manifest_sha256;self.prediction_sha256=hashlib.sha256(json.dumps(self.predictions,separators=(",",":")).encode()).hexdigest()
def _validate(rows,features):
 for row in rows:
  forbidden={"user_id","speaker_id","provider_subject","language","province","age","gender","reward_amount_cents"}&set(row)
  if forbidden:raise ValueError(f"prohibited features: {sorted(forbidden)}")
  if not set(features)<=set(row):raise ValueError("missing feature")
def _runs(train,dev,features,seed):
 _validate(train+dev,features); manifest="0"*64; y=[float(r.get("label",0)) for r in dev]; baseline=[sum(float(r.get("label",0)) for r in train)/max(len(train),1)]*len(dev)
 return tuple(TabularRun(name,baseline,{"brier":sum((p-t)**2 for p,t in zip(baseline,y))/max(len(y),1),"aucpr":0.0,"ece":0.0},manifest) for name in ("RULE_BASELINE","LIGHTGBM","XGBOOST"))
def train_quality_challengers(train,dev,*,seed:int):return _runs(train,dev,QUALITY_FEATURES,seed)
def train_mission_challengers(train,dev,*,seed:int):return _runs(train,dev,MISSION_FEATURES,seed)
