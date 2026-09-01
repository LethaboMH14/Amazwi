import json
from pathlib import Path

import pytest

from amazwi_ml.manifest import (
    DatasetManifest,
    ImmutableManifestConflict,
    ManifestRecord,
    build_manifest,
    canonical_bytes,
    manifest_sha256,
    write_immutable_manifest,
)


def test_manifest_rebuild_is_byte_identical(fixture_records):
    a = build_manifest(fixture_records, generated_at="2026-09-01T00:00:00Z")
    b = build_manifest(list(reversed(fixture_records)), generated_at="2026-09-01T00:00:00Z")
    assert canonical_bytes(a) == canonical_bytes(b)
    assert manifest_sha256(a) == manifest_sha256(b)
    assert canonical_bytes(a).endswith(b"\n")


def test_manifest_nfc_and_immutable_write(tmp_path):
    record = ManifestRecord(
        record_id="r-1", source_id="synthetic", speaker_id="s-1",
        text="Cafe\u0301", language="zu", source_class="SYNTHETIC_FIXTURE",
        split="train",
    )
    manifest = build_manifest([record], generated_at="2026-09-01T00:00:00Z")
    path = tmp_path / "manifest.json"
    digest = write_immutable_manifest(manifest, path)
    assert digest == manifest_sha256(manifest)
    assert path.read_bytes() == canonical_bytes(manifest)
    assert write_immutable_manifest(manifest, path) == digest

    changed = build_manifest([record.model_copy(update={"text": "different"})], generated_at="2026-09-01T00:00:00Z")
    with pytest.raises(ImmutableManifestConflict):
        write_immutable_manifest(changed, path)


def test_fixture_records_are_valid(fixture_records):
    manifest = build_manifest(fixture_records, generated_at="2026-09-01T00:00:00Z")
    assert isinstance(manifest, DatasetManifest)
    assert [r.record_id for r in manifest.records] == sorted(r.record_id for r in fixture_records)


@pytest.fixture
def fixture_records():
    raw = json.loads((Path(__file__).parent / "fixtures" / "records.json").read_text(encoding="utf-8"))
    return [ManifestRecord.model_validate(row) for row in raw]
