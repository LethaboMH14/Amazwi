from __future__ import annotations

import os


def database_url() -> str:
    value = (os.environ.get("AMAZWI_DATABASE_URL") or "").strip()
    if not value:
        raise RuntimeError("AMAZWI_DATABASE_URL is required")
    return value
