from __future__ import annotations
import hashlib,json
from dataclasses import dataclass
from pathlib import Path
import yaml
class PreflightRequired(Exception):pass
class TaskProhibited(Exception):pass
@dataclass(frozen=True)
class PreflightEvidence: dataset_id:str; exact_revision:str; intended_task:str; reviewer:str; decision:str; registry_sha256:str
def load_registry(path:Path)->dict:return yaml.safe_load(path.read_text(encoding="utf-8"))
def _hash(registry):return hashlib.sha256(json.dumps(registry,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def approve_preflight(registry,*,dataset_id,exact_revision,intended_task,reviewer,reviewed_at,terms_accepted):
    spec=registry["datasets"].get(dataset_id)
    if not spec or not terms_accepted or not exact_revision or intended_task in spec.get("prohibited_tasks",[]) or intended_task not in spec.get("allowed_tasks",[]):raise TaskProhibited("TASK_PROHIBITED")
    if spec.get("acquisition_blocked"):raise TaskProhibited("ACQUISITION_BLOCKED")
    return PreflightEvidence(dataset_id,exact_revision,intended_task,reviewer,"APPROVED",_hash(registry))
def require_download_preflight(registry,evidence,*,dataset_id,intended_task):
    if evidence is None or evidence.decision!="APPROVED" or evidence.dataset_id!=dataset_id or evidence.intended_task!=intended_task or evidence.registry_sha256!=_hash(registry):raise PreflightRequired("PREFLIGHT_REQUIRED")
    return registry["datasets"][dataset_id]
