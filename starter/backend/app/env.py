"""Load `starter/backend/.env` into the process environment, once.

Why this exists: every other module reads `os.environ` directly, and
`app/config.py` evaluates some of its values at *import* time. Before
this, a key pasted into `.env` was simply invisible to the running
backend -- only `scripts/momo_smoke.py` ever loaded that file -- so a
correct credential looked like a broken one.

Two deliberate properties:

1. **`setdefault`, never overwrite.** A variable already exported in the
   shell that launched uvicorn wins over the file. The demo is launched
   with `AMAZWI_DATABASE_URL` and `AMAZWI_AUDIO_TOKEN_SECRET` exported;
   silently replacing those from a stale `.env` would repoint the demo
   at the wrong database mid-run.
2. **Never raises.** A missing or malformed `.env` is normal in CI and in
   production, where real environment variables are injected by the
   platform. A parse problem must not take the API down.

Values are not logged. `.env` holds live credentials and is gitignored.
"""
from __future__ import annotations

import os
from pathlib import Path

# app/env.py -> app/ -> backend/
_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"

_loaded = False


def load_env(path: Path | None = None) -> int:
    """Apply `.env` to `os.environ` without overwriting. Returns keys set."""
    global _loaded
    target = path or _ENV_PATH
    if path is None:
        if _loaded:
            return 0
        _loaded = True
    try:
        raw = target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0

    applied = 0
    for line in raw.splitlines():
        # Leading whitespace is tolerated: the real file indents its
        # provider sections, and a key silently ignored for being indented
        # is exactly the failure this module exists to prevent.
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        value = value.strip()
        # Strip one matched pair of surrounding quotes, if present.
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        if key not in os.environ:
            os.environ[key] = value
            applied += 1
    return applied
