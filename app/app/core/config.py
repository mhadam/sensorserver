import os
from urllib.parse import quote

from sqlalchemy.engine import URL
from starlette.config import Config
from starlette.datastructures import Secret


config = Config(".env.app")
PROJECT_NAME = "sensorserver"
VERSION = "1.0.0"
API_PREFIX = "/api"
SECRET_KEY = config(
    "SECRET_KEY",
    cast=str,
)
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=7 * 24 * 60
)
DEVICE_ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "DEVICE_TOKEN_EXPIRE_MINUTES", cast=int, default=10
)

JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="HS256")
JWT_AUDIENCE = config("JWT_AUDIENCE", cast=str, default="sensorserver:auth")
JWT_TOKEN_PREFIX = config("JWT_TOKEN_PREFIX", cast=str, default="Bearer")

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=int, default=5432)
POSTGRES_DB = config("POSTGRES_DB", cast=str)
if os.environ.get("TESTING"):
    POSTGRES_DB += "_test"
DATABASE_URL = URL.create(
    "postgresql+asyncpg",
    POSTGRES_USER,
    quote(str(POSTGRES_PASSWORD), safe=""),
    POSTGRES_SERVER,
    POSTGRES_PORT,
    POSTGRES_DB,
)
UNQUOTED_DATABASE_URL = URL.create(
    "postgresql+asyncpg",
    POSTGRES_USER,
    str(POSTGRES_PASSWORD),
    POSTGRES_SERVER,
    POSTGRES_PORT,
    POSTGRES_DB,
)
