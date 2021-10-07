import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL

db_url = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else str(DATABASE_URL)

engine = create_async_engine(db_url, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with async_session() as s:
        yield s
