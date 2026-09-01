import pytest
from amazwi_ml.tabular import QUALITY_FEATURES,train_quality_challengers
def test_protected_fields_never_enter_features():
 assert set(QUALITY_FEATURES).isdisjoint({"user_id","speaker_id","provider_subject","language","province","age","gender","reward_amount_cents"})
def test_challenger_hashes_are_deterministic():
 rows=[{k:1 for k in QUALITY_FEATURES}|{"label":1}]
 a=train_quality_challengers(rows,rows,seed=1);b=train_quality_challengers(rows,rows,seed=1)
 assert [x.prediction_sha256 for x in a]==[x.prediction_sha256 for x in b]
