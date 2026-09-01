"""Canonical, immutable dataset manifest primitives for governed ML fixtures."""

from __future__ import annotations

import hashlib
import json
import unicodedata
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any, Iterable


class ImmutableManifestConflict(RuntimeError):
    """Raised when a manifest path already contains different canonical bytes."""


@dataclass(frozen=True)
class ManifestRecord:
    record_id: str
    source_id: str
    speaker_id: str | None = None
    text: str = ""
    language: str = ""
    source_class: str = "SYNTHETIC_FIXTURE"
    split: str | None = None
    domain: str | None = None
    acoustic_condition: str | None = None
    audio_sha256: str | None = None
    source_sha256: str | None = None
    excluded: bool = False
    exclusion_reason: str | None = None
    consent_version: str | None = None

    @classmethod
    def model_validate(cls, value: dict[str, Any]) -> "ManifestRecord":
        fields = {field.name for field in __import__("dataclasses").fields(cls)}
        return cls(**{key: item for key, item in value.items() if key in fields})

    def model_copy(self, *, update: dict[str, Any] | None = None) -> "ManifestRecord":
        return replace(self, **(update or {}))


@dataclass(frozen=True)
class DatasetManifest:
    dataset_id: str = "amazwi-synthetic"
    dataset_version: str = "1"
    source_repository: str = "synthetic://amazwi"
    source_revision: str = "synthetic"
    licence: str = "SYNTHETIC"
    restrictions: tuple[str, ...] = ()
    allowed_tasks: tuple[str, ...] = ()
    language: str | None = None
    domain: str | None = None
    amazwi_consent_version: str | None = None
    transforms: dict[str, str] = field(default_factory=dict)
    tool_versions: dict[str, str] = field(default_factory=dict)
    source_hashes: dict[str, str] = field(default_factory=dict)
    output_hashes: dict[str, str] = field(default_factory=dict)
    exclusions: tuple[str, ...] = ()
    revocations: tuple[str, ...] = ()
    approval_actor: str | None = None
    approved_at: str | None = None
    export_registry_id: str | None = None
    generated_at: str = ""
    records: tuple[ManifestRecord, ...] = ()

    def model_dump(self, *, mode: str = "python", exclude_none: bool = False) -> dict[str, Any]:
        value = asdict(self)
        if mode == "json":
            value["restrictions"] = list(self.restrictions)
            value["allowed_tasks"] = list(self.allowed_tasks)
            value["exclusions"] = list(self.exclusions)
            value["revocations"] = list(self.revocations)
        return value


def _normalise_nfc(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, dict):
        return {key: _normalise_nfc(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalise_nfc(item) for item in value]
    return value


def _record(value: ManifestRecord | dict[str, Any]) -> ManifestRecord:
    return value if isinstance(value, ManifestRecord) else ManifestRecord.model_validate(value)


def build_manifest(records: Iterable[ManifestRecord | dict[str, Any]], *, generated_at: str, **metadata: Any) -> DatasetManifest:
    ordered = tuple(sorted((_record(row) for row in records), key=lambda row: (row.source_id, row.record_id)))
    return DatasetManifest(generated_at=generated_at, records=ordered, **metadata)


def canonical_bytes(manifest: DatasetManifest) -> bytes:
    value = _normalise_nfc(manifest.model_dump(mode="json", exclude_none=False))
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def manifest_sha256(manifest: DatasetManifest) -> str:
    return hashlib.sha256(canonical_bytes(manifest)).hexdigest()


def write_immutable_manifest(manifest: DatasetManifest, path: Path) -> str:
    raw = canonical_bytes(manifest)
    if path.exists():
        if path.read_bytes() != raw:
            raise ImmutableManifestConflict(str(path))
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()
