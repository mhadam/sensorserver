import os
import databases

from app.core.config import DATABASE_URL

DB_URL = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else str(DATABASE_URL)

database = databases.Database("postgresql" + DB_URL.lstrip("postgresql+asyncpg"))
