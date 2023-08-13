import pytest
from httpx import AsyncClient

from tests.conftest import tokennn
from tests.test_auth import auth_ac


async def test_get_item(ac: AsyncClient):
    response = await ac.get("menu/1")
    assert response.status_code == 200
    assert response.json() == [{'name': 'test_item_1', 'price': 1, 'ingridients': 'some'}]


async def test_get_item_404(ac: AsyncClient):
    response = await ac.get("menu/10")
    assert response.json() == []


async def test_add_item(auth_ac):
    response = await auth_ac.post("menu/1", cookies={"cook": tokennn}, json={"quantity": 1})
    assert response.status_code == 200


