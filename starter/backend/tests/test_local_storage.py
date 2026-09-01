import hashlib
from datetime import datetime, timedelta, timezone

import pytest

from app.storage.base import AudioHashMismatch, AudioUnavailable, InvalidAudioToken, InvalidObjectKey
from app.storage.local import LocalAudioObjectStore


@pytest.fixture
def store(tmp_path):
    return LocalAudioObjectStore(tmp_path, secret=b"task-3-test-secret")


def test_object_key_cannot_escape_storage_root(store):
    with pytest.raises(InvalidObjectKey):
        store.write_upload("../secret", b"x")
    with pytest.raises(InvalidObjectKey):
        store.write_upload("C:/secret", b"x")
    for key in ("", "/etc/passwd", r"..\secret", r"audio\one", "voice\x00raw"):
        with pytest.raises(InvalidObjectKey):
            store.write_upload(key, b"x")


def test_write_verify_and_finalise_use_sha256_and_atomic_state(store):
    stored = store.write_upload("audio/one", b"voice")
    assert stored.sha256 == hashlib.sha256(b"voice").hexdigest()
    assert stored.byte_length == 5
    assert store.pending_path("audio/one").exists()

    with pytest.raises(AudioHashMismatch):
        store.verify("audio/one", "0" * 64, 5)
    verified = store.verify("audio/one", stored.sha256, 5)
    finalised = store.finalise(verified)
    assert finalised.object_key == "audio/one"
    assert store.final_path("audio/one").read_bytes() == b"voice"
    assert not store.pending_path("audio/one").exists()


def test_expired_wrong_audience_and_tampered_tokens_cannot_play(store):
    store.write_upload("audio/one", b"voice")
    finalised = store.finalise(store.verify("audio/one", store.sha256("audio/one"), 5))
    now = datetime(2026, 9, 1, tzinfo=timezone.utc)
    token = store.issue_token(finalised.object_key, audience="user-a", purpose="VERIFY", ttl_seconds=1, now=now)
    with pytest.raises(InvalidAudioToken):
        store.open_private(token, audience="user-b", now=now)
    with pytest.raises(InvalidAudioToken):
        store.open_private(token, audience="user-a", now=now + timedelta(seconds=2))
    with pytest.raises(InvalidAudioToken):
        store.open_private(token[:-2] + "xx", audience="user-a", now=now)


def test_quarantine_blocks_playback_and_delete_removes_object(store):
    store.write_upload("audio/one", b"voice")
    finalised = store.finalise(store.verify("audio/one", store.sha256("audio/one"), 5))
    store.quarantine(finalised.object_key)
    with pytest.raises(AudioUnavailable):
        store.open_by_key(finalised.object_key)
    store.delete(finalised.object_key)
    assert not store.final_path(finalised.object_key).exists()
