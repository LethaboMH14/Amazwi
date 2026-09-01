from pathlib import Path
import json
import pytest
from amazwi_ml.budget import reserve_gpu_run, AccountBudgetExceeded, PhaseBudgetExceeded
def test_phase_and_account_caps(tmp_path: Path):
 path=tmp_path/"budget.json";h="a"*64;c="b"*64
 reserve_gpu_run(path,run_id="one",account_alias="team-sonar-a",phase="PREFLIGHT",requested_hours=6,manifest_sha256=h,config_sha256=c)
 with pytest.raises(PhaseBudgetExceeded): reserve_gpu_run(path,run_id="two",account_alias="team-sonar-a",phase="PREFLIGHT",requested_hours=1,manifest_sha256=h,config_sha256=c)
 assert json.loads(path.read_text())["entries"][0]["state"]=="RESERVED"
def test_account_cap(tmp_path: Path):
 path=tmp_path/"budget.json";h="a"*64;c="b"*64
 reserve_gpu_run(path,run_id="one",account_alias="team-sonar-a",phase="ISIZULU_ADAPTATION",requested_hours=16,manifest_sha256=h,config_sha256=c)
 with pytest.raises(AccountBudgetExceeded): reserve_gpu_run(path,run_id="two",account_alias="team-sonar-a",phase="SETSWANA_ADAPTATION",requested_hours=15,manifest_sha256=h,config_sha256=c)
