import pytest

from amazwi_ml.manifest import ManifestRecord
from amazwi_ml.splits import assign_speaker_splits


def _record(source_id, record_id, speaker_id, **overrides):
    defaults = dict(source_id=source_id, record_id=record_id, speaker_id=speaker_id, language="isizulu")
    defaults.update(overrides)
    return ManifestRecord(**defaults)


def test_missing_speaker_id_on_non_excluded_record_raises():
    with pytest.raises(ValueError):
        assign_speaker_splits([_record("amazwi", "001", None)], seed="s")


def test_excluded_record_without_speaker_id_is_allowed_through_unassigned():
    records = [_record("amazwi", "001", None, excluded=True)]
    out = assign_speaker_splits(records, seed="s")
    assert out[0].split is None


def test_assignment_is_deterministic_for_the_same_seed():
    records = [_record("amazwi", "001", "speaker-a"), _record("amazwi", "002", "speaker-b")]
    out_1 = assign_speaker_splits(list(records), seed="fixed-seed")
    out_2 = assign_speaker_splits(list(records), seed="fixed-seed")
    assert [r.split for r in out_1] == [r.split for r in out_2]


def test_assignment_can_differ_across_seeds():
    records = [_record("amazwi", str(i), f"speaker-{i}") for i in range(20)]
    out_a = assign_speaker_splits(list(records), seed="seed-a")
    out_b = assign_speaker_splits(list(records), seed="seed-b")
    assert [r.split for r in out_a] != [r.split for r in out_b]


def test_every_record_from_the_same_speaker_lands_in_the_same_split():
    # speaker-safe: no speaker should straddle train/dev/test, since assignment
    # keys on (seed, source_id, speaker_id), not per-record identity
    records = [_record("amazwi", str(i), "speaker-x") for i in range(15)]
    out = assign_speaker_splits(records, seed="fixed-seed")
    assert len({r.split for r in out}) == 1


def test_split_ratios_are_respected_within_tolerance_over_many_speakers():
    records = [_record("amazwi", str(i), f"speaker-{i}") for i in range(2000)]
    out = assign_speaker_splits(records, seed="fixed-seed", train_ratio=0.8, dev_ratio=0.1)
    counts = {"train": 0, "dev": 0, "test": 0}
    for r in out:
        counts[r.split] += 1
    # hash-bucket assignment over 2000 independent speakers should land close
    # to the requested 80/10/10 split; generous tolerance to avoid test flakiness
    total = len(out)
    assert abs(counts["train"] / total - 0.8) < 0.05
    assert abs(counts["dev"] / total - 0.1) < 0.05
    assert abs(counts["test"] / total - 0.1) < 0.05


def test_output_is_sorted_by_source_and_record_id():
    records = [_record("amazwi", "003", "s1"), _record("amazwi", "001", "s2"), _record("amazwi", "002", "s3")]
    out = assign_speaker_splits(records, seed="s")
    assert [r.record_id for r in out] == ["001", "002", "003"]
