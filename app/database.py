from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from config import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER

# settings = Settings(env="main")  # Default to main database environment

# engine = create_async_engine(settings.db_url)


SQLALCHEMY_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}'
Base = declarative_base()

metadata = MetaData()
metadata1 = MetaData()

engine = create_async_engine(SQLALCHEMY_URL, poolclass=NullPool, echo=True)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
