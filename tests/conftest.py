import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import insert, values
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.database import get_async_session, metadata, Base
from app.config import (DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST,
                        DB_USER_TEST)
from app.main import app
from app.auth.models import role
from app.items.models import item, category

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest_asyncio.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True, scope='session')
async def set_up_data():
    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, role_name="admin")
        stmt_category = insert(category).values(id=1, name='test_category_name')
        stmt_item_1 = insert(item).values(id=1, name='test_item_1', ingridients='some', price=1, category_id=1)
        stmt_item_2 = insert(item).values(id=2, name='test_item_2', ingridients='something', price=2, category_id=1)
        await session.execute(stmt)
        await session.execute(stmt_category)
        await session.execute(stmt_item_1)
        await session.execute(stmt_item_2)
        await session.commit()


tokennn = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiYXVkIjpbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJleHAiOjE2OTE5NjMyMjR9.pBFPwWKMFKZGohluFcwrCLLoRjRhSBcmlpsD87ssRHY'

# @pytest.fixture(scope='session', autouse=True)
# async def user_token(ac: AsyncClient):
#     await ac.post("/api/v1/users", json=DATA_USER)
#     response = await ac.post("/api/v1/users/token", json=DATA_USER)
#     return response.json()

