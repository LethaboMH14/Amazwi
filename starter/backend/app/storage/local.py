from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import io
import json
import re
from datetime import datetime
from pathlib import Path

from app.storage.base import (
    AudioHashMismatch,
    AudioUnavailable,
    InvalidAudioToken,
    InvalidObjectKey,
    StoredObject,
)


class LocalAudioObjectStore:
    def __init__(self, root: str | Path, *, secret: bytes):
        if not secret:
            raise ValueError("audio token secret must not be empty")
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.secret = secret

    def _relative_key(self, object_key: str) -> Path:
        if not object_key or "\x00" in object_key:
            raise InvalidObjectKey("object key is empty or contains a NUL byte")
        # Validate POSIX and Windows syntax identically on every host. Path()
        # is platform-sensitive, so Linux otherwise treats C:/x as relative.
        if object_key.startswith(("/", "\\")) or "\\" in object_key or re.match(r"^[A-Za-z]:", object_key):
            raise InvalidObjectKey("object key must use safe relative POSIX syntax")
        candidate = Path(object_key)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise InvalidObjectKey("object key must remain below the storage root")
        path = (self.root / candidate).resolve()
        try:
            path.relative_to(self.root)
        except ValueError as exc:
            raise InvalidObjectKey("object key must remain below the storage root") from exc
        return path

    def pending_path(self, object_key: str) -> Path:
        return self._relative_key(object_key).with_suffix(".pending")

    def final_path(self, object_key: str) -> Path:
        return self._relative_key(object_key).with_suffix(".bin")

    def quarantine_path(self, object_key: str) -> Path:
        return self._relative_key(object_key).with_suffix(".quarantine")

    def begin_upload(self, object_key: str) -> str:
        pending = self.pending_path(object_key)
        final = self.final_path(object_key)
        if pending.exists() or final.exists():
            raise InvalidObjectKey("object key is already in use")
        pending.parent.mkdir(parents=True, exist_ok=True)
        return object_key

    def write_upload(self, object_key: str, body: bytes) -> StoredObject:
        self.begin_upload(object_key)
        pending = self.pending_path(object_key)
        pending.write_bytes(body)
        return StoredObject(object_key, hashlib.sha256(body).hexdigest(), len(body))

    def sha256(self, object_key: str) -> str:
        path = self.pending_path(object_key)
        if not path.exists():
            path = self.final_path(object_key)
        if not path.exists():
            raise AudioUnavailable("audio object is not available")
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def verify(self, object_key: str, sha256: str, byte_length: int) -> StoredObject:
        path = self.pending_path(object_key)
        if not path.exists():
            raise AudioUnavailable("pending audio object is not available")
        body = path.read_bytes()
        actual_hash = hashlib.sha256(body).hexdigest()
        if not hmac.compare_digest(actual_hash, sha256) or len(body) != byte_length:
            raise AudioHashMismatch("audio hash or byte length does not match")
        return StoredObject(object_key, actual_hash, len(body))

    def finalise(self, stored: StoredObject) -> StoredObject:
        pending = self.pending_path(stored.object_key)
        if not pending.exists():
            raise AudioUnavailable("pending audio object is not available")
        pending.replace(self.final_path(stored.object_key))
        return stored

    def issue_token(
        self,
        object_key: str,
        *,
        audience: str,
        purpose: str,
        ttl_seconds: int,
        now: datetime,
    ) -> str:
        self.final_path(object_key)
        if ttl_seconds <= 0:
            raise InvalidAudioToken("token TTL must be positive")
        payload = {
            "key": object_key,
            "aud": audience,
            "purpose": purpose,
            "exp": now.timestamp() + ttl_seconds,
            "iat": now.timestamp(),
        }
        encoded = base64.urlsafe_b64encode(
            json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
        ).rstrip(b"=")
        signature = hmac.new(self.secret, encoded, hashlib.sha256).digest()
        return encoded.decode() + "." + base64.urlsafe_b64encode(signature).rstrip(b"=").decode()

    def _decode_token(self, token: str) -> dict:
        try:
            encoded_text, signature_text = token.split(".", 1)
            encoded = encoded_text.encode()
            signature = base64.urlsafe_b64decode(signature_text + "=" * (-len(signature_text) % 4))
            expected = hmac.new(self.secret, encoded, hashlib.sha256).digest()
            if not hmac.compare_digest(signature, expected):
                raise InvalidAudioToken("invalid audio token signature")
            payload = json.loads(base64.urlsafe_b64decode(encoded + b"=" * (-len(encoded) % 4)))
            if not isinstance(payload, dict):
                raise InvalidAudioToken("invalid audio token payload")
            return payload
        except (
            ValueError,
            TypeError,
            binascii.Error,
            json.JSONDecodeError,
            UnicodeDecodeError,
        ) as exc:
            raise InvalidAudioToken("invalid audio token") from exc

    def token_payload(self, token: str) -> dict:
        return self._decode_token(token)

    def open_private(self, token: str, *, audience: str, now: datetime, purpose: str | None = None) -> io.BytesIO:
        payload = self._decode_token(token)
        if payload.get("aud") != audience or (purpose is not None and payload.get("purpose") != purpose):
            raise InvalidAudioToken("audio token audience or purpose mismatch")
        if now.timestamp() >= float(payload.get("exp", 0)):
            raise InvalidAudioToken("audio token has expired")
        object_key = payload.get("key")
        if not isinstance(object_key, str):
            raise InvalidAudioToken("audio token has no object key")
        return io.BytesIO(self.open_by_key(object_key))

    def open_by_key(self, object_key: str) -> bytes:
        final = self.final_path(object_key)
        if not final.exists():
            raise AudioUnavailable("audio object is not available")
        return final.read_bytes()

    def quarantine(self, object_key: str) -> None:
        final = self.final_path(object_key)
        if not final.exists():
            raise AudioUnavailable("audio object is not available")
        final.replace(self.quarantine_path(object_key))

    def delete(self, object_key: str) -> None:
        for path in (
            self.pending_path(object_key),
            self.final_path(object_key),
            self.quarantine_path(object_key),
        ):
            path.unlink(missing_ok=True)
