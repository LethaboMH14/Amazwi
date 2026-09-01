"""CPU-only deterministic LightGBM/XGBoost challengers for synthetic fixtures."""
from __future__ import annotations
import hashlib,json
import numpy as np
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
QUALITY_FEATURES=("duration_ms","silence_ratio","clipping_ratio","snr_db","sample_rate_hz","codec_code","duplicate_score","peer_disagreement")
MISSION_FEATURES=("coverage_count","model_error_rate","completion_rate","sponsor_priority")
FORBIDDEN={"user_id","speaker_id","provider_subject","language","province","age","gender","reward_amount_cents"}
class TabularRun:
 def __init__(self,candidate_id,predictions,metrics,manifest_sha256="0"*64):
  self.candidate_id=candidate_id;self.predictions=tuple(float(x) for x in predictions);self.metrics=metrics;self.manifest_sha256=manifest_sha256;self.prediction_sha256=hashlib.sha256(json.dumps(self.predictions,separators=(",",":")).encode()).hexdigest()
def _matrix(rows,features):
 if not rows:return np.empty((0,len(features))),np.empty(0)
 for row in rows:
  if FORBIDDEN&set(row):raise ValueError("protected/identity fields cannot be features")
  if not set(features)<=set(row):raise ValueError("missing fixed feature")
 return np.array([[float(r[f]) for f in features] for r in rows]),np.array([int(r.get("label",0)) for r in rows])
def _metrics(pred,y):
 return {"brier":float(np.mean((pred-y)**2)) if len(y) else 0.0,"aucpr":0.0,"ece":float(abs(np.mean(pred)-np.mean(y))) if len(y) else 0.0}
def _train(train,dev,features,seed):
 x,y=_matrix(train,features);xd,yd=_matrix(dev,features)
 base=np.full(len(dev),float(np.mean(y)) if len(y) else .5)
 runs=[TabularRun("RULE_BASELINE",base,_metrics(base,yd))]
 if len(x) and len(set(y))>1:
  models=[("LIGHTGBM",LGBMClassifier(n_estimators=25,max_depth=3,learning_rate=.05,random_state=seed,n_jobs=1,verbosity=-1)),("XGBOOST",XGBClassifier(n_estimators=25,max_depth=3,learning_rate=.05,random_state=seed,n_jobs=1,tree_method="hist",verbosity=0))]
  for name,model in models:
   model.fit(x,y);p=model.predict_proba(xd)[:,1] if len(xd) else np.array([]);runs.append(TabularRun(name,p,_metrics(p,yd)))
 else:
  # Honest fallback for a degenerate synthetic fixture: not a trained run.
  runs.extend([TabularRun("LIGHTGBM_UNTRAINED",base,_metrics(base,yd)),TabularRun("XGBOOST_UNTRAINED",base,_metrics(base,yd))])
 return tuple(runs)
def train_quality_challengers(train,dev,*,seed:int):return _train(train,dev,QUALITY_FEATURES,seed)
def train_mission_challengers(train,dev,*,seed:int):return _train(train,dev,MISSION_FEATURES,seed)
