"""
Automatically add all models to __all__
This is used in alembic while autogenerating database migration script.
"""
from typing import Tuple

from sqlalchemy import Column, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from os.path import dirname, basename, isfile, join
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [
    basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")
]

Base = declarative_base()


def timestamps(indexed: bool = False) -> Tuple[Column, Column]:
    return (
        Column(
            "created_at",
            TIMESTAMP(timezone=True),
            server_default=func.now(),
            nullable=False,
            index=indexed,
        ),
        Column(
            "updated_at",
            TIMESTAMP(timezone=True),
            server_default=func.now(),
            nullable=False,
            index=indexed,
        ),
    )
