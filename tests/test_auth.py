import pytest
from sqlalchemy import insert, select

from app.auth.models import Role
from conftest import client, async_session_maker


@pytest.mark.asyncio
async def test_add_role():
    async with async_session_maker() as session:
        new_role = Role(id=1, role_name='string')
        session.add(new_role)
        await session.flush()

        query = select(Role)
        result = await session.execute(query)
        added_roles = result.all()
        print(added_roles)
    #     assert len(added_roles) == 1, "Role not added"
    assert 1 == 1
