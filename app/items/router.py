from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import User
from cart.models import cart, cart_item
from cart.schemas import AddToCart
from database import get_async_session
from items.models import category, item
from items.schemas import ListItemModel

router = APIRouter(
    prefix='/menu',
    tags=['Menu']
)


@router.get('/', response_model=Dict[str, List[ListItemModel]])
@cache(expire=360)
async def get_menu(session: AsyncSession = Depends(get_async_session)):
    query = select(category.c.name, item.c.name, item.c.price).join(category)
    result = await session.execute(query)

    # Organize the data into the desired JSON structure
    category_items = {}
    for row in result:
        print(row)
        category_name, item_name, item_price = row
        if category_name not in category_items:
            category_items[category_name] = []
        category_items[category_name].append({"name": item_name, "price": item_price})

    if not category_items:
        raise HTTPException(status_code=404, detail="No data found")
    return category_items


@router.get('/{item_id}')
async def get_menu_item(item_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(item.c.name, item.c.price, item.c.ingridients).where(item.c.id == item_id)
    result = await session.execute(query)

    return [dict(r._mapping) for r in result]


@router.post('/{item_id}')
async def add_to_cart(operation: AddToCart, item_id: int, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    for key, value in operation:
        quantity = value

    query = select(cart.c.id).where(cart.c.user_id == user.id, cart.c.is_ordered == False, cart.c.is_done == False)
    res = await session.execute(query)
    cart_obj = res.fetchone()
    if cart_obj is None:
        query = insert(cart).values(user_id=user.id)
        result = await session.execute(query)
        cart_id = result.inserted_primary_key[0]
    else:
        cart_id = cart_obj[0]
    query = select(cart_item.c.id, cart_item.c.quantity).where(cart_item.c.cart_id == cart_id,
                                                               cart_item.c.item_id == item_id)
    res = await session.execute(query)
    cart_item_obj = res.fetchone()

    if cart_item_obj is None:
        stmt = insert(cart_item).values(quantity=quantity, cart_id=cart_id, item_id=item_id)
        await session.execute(stmt)
    else:
        existing_quantity = cart_item_obj[1]
        new_quantity = existing_quantity + quantity
        stmt = update(cart_item).where(cart_item.c.id == cart_item_obj[0]).values(quantity=new_quantity)
        await session.execute(stmt)
    await session.commit()


    return {"status": "added to cart"}
