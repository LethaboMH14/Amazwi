from __future__ import annotations

from dataclasses import dataclass


class StorageError(Exception):
    pass


class InvalidObjectKey(StorageError):
    pass


class InvalidAudioToken(StorageError):
    pass


class AudioUnavailable(StorageError):
    pass


class AudioHashMismatch(StorageError):
    pass


@dataclass(frozen=True)
class StoredObject:
    object_key: str
    sha256: str
    byte_length: int
