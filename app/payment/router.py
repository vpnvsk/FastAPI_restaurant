import json
from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy import select, join, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import User
from cart.models import cart, cart_item
from chat.router import manager
from database import get_async_session
from items.models import item

router = APIRouter(prefix='/payment',
                   tags=['Payment']
                   )


@router.get('/')
async def pay_for_order(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    query = (
        select(cart_item.c.quantity, item.c.price, item.c.name, )
        .select_from(
            join(item, cart_item, item.c.id == cart_item.c.item_id)
            .join(cart, cart_item.c.cart_id == cart.c.id)
        )
        .where(cart.c.user_id == user.id, cart.c.is_ordered == False)
    )
    result = await session.execute(query)

    cart_items = [dict(r._mapping) for r in result]
    final_value = sum(item["quantity"] * item["price"] for item in cart_items)

    """     PAYMENT IMITATION     """
    payment_status = True

    if payment_status:

        stmt = update(cart).where(cart.c.user_id == user.id, cart.c.is_ordered == False).values(is_ordered=True)
        await session.execute(stmt)

        await session.commit()

        user_cart_items = defaultdict(list)
        for item_ in cart_items:
            user_cart_items[user.name].append({"name": item_["name"], "quantity": item_["quantity"]})

        cart_items_output = [{user_name: user_cart_items[user_name]} for user_name in user_cart_items]

        cart_items_json = json.dumps(cart_items_output)
        print(cart_items_json)

        await manager.broadcast(cart_items_json)
        return {"status": "succes"}
    return {"status": "failure"}
