import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_register(ac: AsyncClient):
    response = await ac.post("/auth/register", json=
    {
        "password": "s",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "name": "q",
        "role_id": 1,
        "email": "string@gmail.com",
    })

    assert response.status_code == 201


@pytest.fixture(scope="session")
async def auth_ac():
    async with AsyncClient(app=app, base_url="http://test") as acc:
        response = await acc.post("auth/jwt/login", data={
            "username": "string@gmail.com",
            "password": "s",
        })

        yield acc
