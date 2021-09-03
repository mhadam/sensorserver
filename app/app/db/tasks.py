import logging
import os

from app.core.config import DATABASE_URL
from app.db import database
from databases import DatabaseURL
from fastapi import FastAPI

logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    if os.environ.get("TESTING"):
        database.url = DatabaseURL(f"{DATABASE_URL}_test")
    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logger.warning("--- DB CONNECTION ERROR ---")
        logger.warning(e)
        logger.warning("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    try:
        await database.disconnect()
    except Exception as e:
        logger.warning("--- DB DISCONNECT ERROR ---")
        logger.warning(e)
        logger.warning("--- DB DISCONNECT ERROR ---")
