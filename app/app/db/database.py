from typing import AsyncGenerator

import databases
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import UNQUOTED_DATABASE_URL, DATABASE_URL
from app.db.tables import Base
from app.db.tables.users import Users
from app.models.user import UserDB

normalized_scheme_url = "postgresql" + DATABASE_URL.render_as_string(
    hide_password=False
).lstrip("postgresql+asyncpg")
database = databases.Database(normalized_scheme_url)

engine = create_async_engine(UNQUOTED_DATABASE_URL,  connect_args={"server_settings": {"timezone": "est"}})
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def test_connection():
    async with engine.begin() as conn:
        pass


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(UserDB, session, Users)
