import logging
import os
import pathlib
import sys
from logging.config import fileConfig

import alembic
from app.core.config import DATABASE_URL, POSTGRES_DB  # noqa
from sqlalchemy import create_engine, pool, engine_from_config

base_dir = str(pathlib.Path(__file__).resolve().parent.parent)  # db module
sys.path.append(base_dir)

config = alembic.context.config

fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

from app.db.tables import *  # noqa; helps autogenerate
from app.db.tables import Base  # noqa

target_metadata = Base.metadata


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode
    """
    DB_URL = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else str(DATABASE_URL)
    DB_URL = "postgresql" + DB_URL.lstrip("postgresql+asyncpg")
    if os.environ.get("TESTING"):
        default_engine = create_engine(str(DATABASE_URL), isolation_level="AUTOCOMMIT")
        with default_engine.connect() as default_conn:
            default_conn.execute(f"DROP DATABASE IF EXISTS {POSTGRES_DB}_test")
            default_conn.execute(f"CREATE DATABASE {POSTGRES_DB}_test")

    connectable = config.attributes.get("connection")
    config.set_main_option("sqlalchemy.url", DB_URL)

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        alembic.context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode
    """
    if os.environ.get("TESTING"):
        raise RuntimeError(
            "Running testing migrations offline currently not permitted."
        )

    alembic.context.configure(url=str(DATABASE_URL), target_metadata=target_metadata)

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()
