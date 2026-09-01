from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from app.storage import LocalAudioObjectStore


@lru_cache(maxsize=1)
def get_audio_store() -> LocalAudioObjectStore:
    secret = (os.environ.get("AMAZWI_AUDIO_TOKEN_SECRET") or "").encode()
    if not secret:
        raise RuntimeError("AMAZWI_AUDIO_TOKEN_SECRET is required")
    root = os.environ.get("AMAZWI_PRIVATE_AUDIO_ROOT") or ".private_audio"
    return LocalAudioObjectStore(Path(root), secret=secret)
