from tests.conftest import tokennn
from tests.test_auth import auth_ac


async def test_get_cart_items(auth_ac):
    response = await auth_ac.get("cart/", cookies={"cook": tokennn})
    assert response.status_code == 200
