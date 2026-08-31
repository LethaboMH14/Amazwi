import os
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context

from app.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Real target metadata -- app/models.py, not None. AMAZWI_DATABASE_URL
# overrides alembic.ini's placeholder when set (tests/CI/local dev all set
# it; alembic.ini keeps a non-functional placeholder on purpose so nobody
# accidentally migrates a default local Postgres with no override).
#
# Deliberately NOT using config.set_main_option("sqlalchemy.url", ...) here
# (the naive approach): alembic.ini is read by Python's ConfigParser, which
# treats a bare "%" as the start of interpolation syntax. Any URL-encoded
# password containing a special character -- e.g. "!" becomes "%21" -- then
# crashes with "invalid interpolation syntax", a real bug this project hit
# against an actual local PostgreSQL password (see BUILD_LOG.md). Storing
# the URL in config.attributes instead, and building the Engine directly in
# run_migrations_online() below, bypasses ConfigParser interpolation
# entirely -- the URL is a plain Python string the whole way through.
db_url = os.environ.get("AMAZWI_DATABASE_URL")
if db_url:
    config.attributes["sqlalchemy_url_override"] = db_url

target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def _resolved_url() -> str:
    return config.attributes.get("sqlalchemy_url_override") or config.get_main_option("sqlalchemy.url")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = _resolved_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(_resolved_url(), poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
