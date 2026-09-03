"""Package init.

`.env` is loaded here, before any submodule imports, because
`app/config.py` reads some values at import time -- loading later would
be too late for those. Shell-exported variables always win; see
`app/env.py`.
"""
from app.env import load_env

load_env()
