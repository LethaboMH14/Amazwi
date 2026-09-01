from __future__ import annotations

from functools import lru_cache
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import database_url


@lru_cache(maxsize=1)
def get_engine():
    return create_engine(database_url())


def get_session() -> Generator[Session, None, None]:
    session = Session(get_engine())
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
