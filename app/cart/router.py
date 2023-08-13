from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update, join, delete
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import User
from cart.models import cart, cart_item
from cart.schemas import ChangeQuantity
from database import get_async_session
from items.models import item

router = APIRouter(
    prefix='/cart',
    tags=["Cart"]
)


@router.get('/')
async def get_cart_items(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
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


@router.post('/')
async def change_quantity_of_product(option: ChangeQuantity,
                                     session: AsyncSession = Depends(get_async_session),
                                     user: User = Depends(current_user)):
    query = select(cart_item.c.quantity, cart_item.c.id).select_from(
        join(item, cart_item, item.c.id == cart_item.c.item_id)
        .join(cart, cart_item.c.cart_id == cart.c.id)).where(cart.c.user_id == user.id,
                                                             cart.c.is_ordered == False, item.c.name == option.name)
    res = await session.execute(query)

    cart_item_row = res.fetchone()

    if cart_item_row:
        quantity_value, cart_item_id = cart_item_row

        match option.status:
            case option.status.incremente:
                quantity_value = quantity_value + 1
            case option.status.decremente:
                quantity_value = quantity_value - 1
            case option.status.delete:
                stmt = delete(cart_item).where(cart_item.c.id == cart_item_id)
                res = await session.execute(stmt)
                await session.commit()
                return {"mesage": "item has been deleted"}

        stmt = update(cart_item).where(cart_item.c.id == cart_item_id).values(quantity=quantity_value)
        await session.execute(stmt)
        await session.commit()
        return {"message": "Quantity updated successfully"}

    raise HTTPException(status_code=404, detail="Item not found in the cart")
