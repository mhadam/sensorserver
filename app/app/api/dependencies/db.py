from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import UNQUOTED_DATABASE_URL

engine = create_async_engine(UNQUOTED_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with async_session() as s:
        yield s
