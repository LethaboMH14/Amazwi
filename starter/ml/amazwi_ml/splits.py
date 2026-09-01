from __future__ import annotations
import hashlib
from .manifest import ManifestRecord
def assign_speaker_splits(records,*,seed:str,train_ratio:float=.8,dev_ratio:float=.1)->tuple[ManifestRecord,...]:
    out=[]
    for row in records:
        if not row.speaker_id and not row.excluded: raise ValueError("speaker_id required for trainable/evaluation record")
        if row.excluded: out.append(row);continue
        h=hashlib.sha256(f"{seed}\0{row.source_id}\0{row.speaker_id}".encode()).digest(); value=int.from_bytes(h[:8],"big")/2**64
        split="train" if value<train_ratio else "dev" if value<train_ratio+dev_ratio else "test"
        out.append(row.model_copy(update={"split":split}))
    return tuple(sorted(out,key=lambda r:(r.source_id,r.record_id)))
