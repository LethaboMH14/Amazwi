from collections import defaultdict

import pytest

from amazwi_ml.manifest import ManifestRecord
from amazwi_ml.splits import MissingSpeakerError, assign_speaker_splits


def test_no_speaker_crosses_splits(fixture_records):
    rows = assign_speaker_splits(fixture_records, seed="amazwi-split-v1")
    memberships = defaultdict(set)
    for row in rows:
        memberships[(row.source_id, row.speaker_id)].add(row.split)
    assert all(len(splits) == 1 for splits in memberships.values())
    assert rows == tuple(sorted(rows, key=lambda r: (r.source_id, r.record_id)))


def test_missing_speaker_is_rejected():
    row = ManifestRecord(record_id="r", source_id="synthetic", speaker_id=None, text="x", language="zu", source_class="SYNTHETIC_FIXTURE")
    with pytest.raises(MissingSpeakerError):
        assign_speaker_splits([row], seed="seed")


def test_split_assignment_is_deterministic(fixture_records):
    assert assign_speaker_splits(fixture_records, seed="same") == assign_speaker_splits(fixture_records, seed="same")
    assert assign_speaker_splits(fixture_records, seed="same") != assign_speaker_splits(fixture_records, seed="different")


@pytest.fixture
def fixture_records():
    return tuple(
        ManifestRecord(record_id=f"r-{i}", source_id="synthetic", speaker_id=f"speaker-{i}", text="hello", language="zu", source_class="SYNTHETIC_FIXTURE")
        for i in range(12)
    )
