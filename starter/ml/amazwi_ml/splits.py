from __future__ import annotations

import hashlib
from collections.abc import Iterable

from .manifest import ManifestRecord


class MissingSpeakerError(ValueError):
    """A trainable or evaluation row cannot be split without a speaker."""


def assign_speaker_splits(
    records: Iterable[ManifestRecord], *, seed: str, train_ratio: float = 0.8, dev_ratio: float = 0.1
) -> tuple[ManifestRecord, ...]:
    if not 0 < train_ratio < 1 or not 0 <= dev_ratio < 1 or train_ratio + dev_ratio > 1:
        raise ValueError("train_ratio and dev_ratio must define valid proportions")
    rows = list(records)
    groups: dict[tuple[str, str], float] = {}
    for row in rows:
        if not row.speaker_id and not row.excluded:
            raise MissingSpeakerError(f"missing speaker_id for {row.source_id}/{row.record_id}")
        if row.speaker_id:
            key = (row.source_id, row.speaker_id)
            digest = hashlib.sha256(f"{seed}\0{key[0]}\0{key[1]}".encode("utf-8")).digest()
            groups.setdefault(key, int.from_bytes(digest[:8], "big") / 2**64)
    result = []
    for row in rows:
        if not row.speaker_id or row.excluded:
            result.append(row)
            continue
        value = groups[(row.source_id, row.speaker_id)]
        split = "train" if value < train_ratio else "dev" if value < train_ratio + dev_ratio else "test"
        result.append(row.model_copy(update={"split": split}))
    return tuple(sorted(result, key=lambda row: (row.source_id, row.record_id)))
