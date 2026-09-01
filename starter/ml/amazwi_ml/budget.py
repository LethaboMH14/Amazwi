from __future__ import annotations
import json,os
from pathlib import Path
class BudgetExceeded(Exception):pass
class AccountBudgetExceeded(Exception):pass
def _load(path):return json.loads(path.read_text()) if path.exists() else {"entries":[]}
def reserve_gpu_run(path:Path,*,run_id,account_alias,phase,requested_hours,manifest_sha256,config_sha256):
    if account_alias not in {"team-sonar-a","team-sonar-b"} or requested_hours<=0 or len(manifest_sha256)!=64 or len(config_sha256)!=64:raise ValueError("invalid reservation")
    data=_load(path);entries=data["entries"]
    if any(e["run_id"]==run_id for e in entries):raise ValueError("duplicate run")
    active=sum(e.get("actual_gpu_hours",e["requested_hours"]) for e in entries);account=sum(e.get("actual_gpu_hours",e["requested_hours"]) for e in entries if e["account_alias"]==account_alias)
    if active+requested_hours>60:raise BudgetExceeded("aggregate 60-hour budget exceeded")
    if account+requested_hours>30:raise AccountBudgetExceeded("30-hour account budget exceeded")
    entry={"run_id":run_id,"account_alias":account_alias,"phase":phase,"requested_hours":requested_hours,"manifest_sha256":manifest_sha256,"config_sha256":config_sha256,"state":"RESERVED"};entries.append(entry);entries.sort(key=lambda e:e["run_id"]);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(".tmp");tmp.write_text(json.dumps(data,sort_keys=True,separators=(",",":"))+"\n");os.replace(tmp,path);return entry
def complete_gpu_run(path:Path,*,run_id,actual_gpu_hours,artefact_sha256):
 if actual_gpu_hours<0 or len(artefact_sha256)!=64:raise ValueError("invalid completion")
 data=_load(path);entry=next((e for e in data["entries"] if e["run_id"]==run_id),None)
 if not entry or entry["state"]!="RESERVED":raise ValueError("unknown or completed run")
 if actual_gpu_hours>entry["requested_hours"]:raise BudgetExceeded("actual hours exceed reservation")
 entry.update(state="COMPLETED",actual_gpu_hours=actual_gpu_hours,artefact_sha256=artefact_sha256);tmp=path.with_suffix(".tmp");tmp.write_text(json.dumps(data,sort_keys=True,separators=(",",":"))+"\n");os.replace(tmp,path);return entry
