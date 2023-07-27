from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, join, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from auth.models import User
from auth.base_config import current_user
from items.models import item
from cart.models import cart, cart_item


router = APIRouter(
    prefix='/cart',
    tags=["Cart"]
)


@router.get('/')
async def get_cart_items(session: AsyncSession = Depends(get_async_session), user: User=Depends(current_user)):

    query = (
        select(item.c.name, cart_item.c.quantity, item.c.price)
        .select_from(
            join(item, cart_item, item.c.id == cart_item.c.item_id)
            .join(cart, cart_item.c.cart_id == cart.c.id)
        )
        .where(cart.c.user_id == user.id, cart.c.is_ordered == False)
    )
    result = await session.execute(query)

    cart_items = [dict(r._mapping) for r in result]
    final_value = sum(item["quantity"] * item["price"] for item in cart_items)
    response = {
        "cart_items": cart_items,
        "final_value": final_value
    }

    return response