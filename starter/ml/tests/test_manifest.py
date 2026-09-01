import pytest

from amazwi_ml.manifest import (
    DatasetManifest,
    ImmutableManifestConflict,
    ManifestRecord,
    canonical_bytes,
    manifest_sha256,
    write_immutable_manifest,
)


def _manifest(records=None, **overrides):
    defaults = dict(dataset_id="amazwi-p0", version="1", generated_at="2026-09-01T00:00:00Z")
    defaults.update(overrides)
    return DatasetManifest(records=records or [], **defaults)


def _record(source_id, record_id, **overrides):
    defaults = dict(source_id=source_id, record_id=record_id, language="isizulu")
    defaults.update(overrides)
    return ManifestRecord(**defaults)


def test_canonical_bytes_is_deterministic_regardless_of_record_order():
    a = _record("amazwi", "002")
    b = _record("amazwi", "001")
    manifest_1 = _manifest([a, b])
    manifest_2 = _manifest([b, a])
    assert canonical_bytes(manifest_1) == canonical_bytes(manifest_2)


def test_manifest_sha256_matches_across_rebuilds_with_identical_content():
    records = [_record("amazwi", "001"), _record("amazwi", "002")]
    hash_1 = manifest_sha256(_manifest(list(records)))
    hash_2 = manifest_sha256(_manifest(list(records)))
    assert hash_1 == hash_2


def test_manifest_sha256_changes_when_a_record_changes():
    base = manifest_sha256(_manifest([_record("amazwi", "001")]))
    changed = manifest_sha256(_manifest([_record("amazwi", "001", excluded=True, exclusion_reason="quality")]))
    assert base != changed


def test_canonical_bytes_nfc_normalises_unicode_in_string_fields():
    decomposed = _record("amazwi", "001", exclusion_reason="é")  # e + combining acute
    precomposed = _record("amazwi", "001", exclusion_reason="é")  # é
    assert canonical_bytes(_manifest([decomposed])) == canonical_bytes(_manifest([precomposed]))


def test_write_immutable_manifest_creates_file_and_returns_hash(tmp_path):
    manifest = _manifest([_record("amazwi", "001")])
    path = tmp_path / "manifests" / "v1.json"
    returned_hash = write_immutable_manifest(manifest, path)
    assert path.exists()
    assert returned_hash == manifest_sha256(manifest)


def test_write_immutable_manifest_rebuild_with_identical_content_is_a_no_op(tmp_path):
    manifest = _manifest([_record("amazwi", "001")])
    path = tmp_path / "v1.json"
    hash_1 = write_immutable_manifest(manifest, path)
    written_bytes = path.read_bytes()
    hash_2 = write_immutable_manifest(_manifest([_record("amazwi", "001")]), path)
    assert hash_1 == hash_2
    assert path.read_bytes() == written_bytes


def test_write_immutable_manifest_conflicting_rewrite_raises(tmp_path):
    path = tmp_path / "v1.json"
    write_immutable_manifest(_manifest([_record("amazwi", "001")]), path)
    with pytest.raises(ImmutableManifestConflict):
        write_immutable_manifest(_manifest([_record("amazwi", "002")]), path)
