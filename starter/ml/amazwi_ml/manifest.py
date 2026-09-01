from __future__ import annotations
import hashlib, json, unicodedata
from pathlib import Path
from pydantic import BaseModel, Field
class ImmutableManifestConflict(Exception): pass
class ManifestRecord(BaseModel):
    source_id:str; record_id:str; speaker_id:str|None=None; language:str; split:str|None=None
    object_sha256:str|None=None; consent_version:str|None=None; excluded:bool=False; exclusion_reason:str|None=None
class DatasetManifest(BaseModel):
    dataset_id:str; version:str; generated_at:str; records:list[ManifestRecord]=Field(default_factory=list)
    export_registry_id:str|None=None; source_revision:str|None=None; license_spdx:str|None=None
def _nfc(value):
    if isinstance(value,str): return unicodedata.normalize("NFC",value)
    if isinstance(value,list): return [_nfc(v) for v in value]
    if isinstance(value,dict): return {str(_nfc(k)):_nfc(v) for k,v in value.items()}
    return value
def canonical_bytes(manifest:DatasetManifest)->bytes:
    value=_nfc(manifest.model_dump(mode="json",exclude_none=False)); value["records"]=sorted(value["records"],key=lambda r:(r["source_id"],r["record_id"]))
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode("utf-8")
def manifest_sha256(manifest:DatasetManifest)->str:return hashlib.sha256(canonical_bytes(manifest)).hexdigest()
def write_immutable_manifest(manifest:DatasetManifest,path:Path)->str:
    raw=canonical_bytes(manifest)
    if path.exists() and path.read_bytes()!=raw: raise ImmutableManifestConflict(str(path))
    path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists(): path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()
