from __future__ import annotations
import hashlib,json
from dataclasses import dataclass
from pathlib import Path
class IncompleteEvidence(Exception):pass
def sha256_file(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
@dataclass(frozen=True)
class EvidenceRun:
 candidate_id:str; promoted:bool; reasons:tuple[str,...]; manifest_sha256:str; metrics:dict[str,float]; intended_use:str="ASR evaluation"; prohibited_use:str="eligibility, rewards, voice cloning"
def generate_model_card(run:EvidenceRun)->str:
 if len(run.manifest_sha256)!=64:raise IncompleteEvidence("immutable manifest hash required")
 decision="PROMOTED" if run.promoted else "NOT PROMOTED"; honesty="" if run.promoted else "\nNo held-out improvement claim is made."
 return f"# Model card: {run.candidate_id}\n\nPromotion decision: {decision}\n\nManifest: `{run.manifest_sha256}`\n\nMetrics: `{json.dumps(run.metrics,sort_keys=True)}`\n\nIntended use: {run.intended_use}\n\nProhibited use: {run.prohibited_use}\n\nReasons: {', '.join(run.reasons) or 'all gates passed'}{honesty}\n"
def write_evidence_index(paths,output:Path)->str:
 artefacts={str(p):sha256_file(p) for p in sorted(paths,key=str)};output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps({"artefacts":artefacts},sort_keys=True,separators=(",",":"))+"\n");return sha256_file(output)
