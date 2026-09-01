from __future__ import annotations

import os

AI_COUNCIL_ENABLED = os.environ.get("AI_COUNCIL_ENABLED", "false").lower() == "true"
AI_COUNCIL_MAX_ATTEMPTS = int(os.environ.get("AI_COUNCIL_MAX_ATTEMPTS", "5"))


def database_url() -> str:
    value = (os.environ.get("AMAZWI_DATABASE_URL") or "").strip()
    if not value:
        raise RuntimeError("AMAZWI_DATABASE_URL is required")
    return value
