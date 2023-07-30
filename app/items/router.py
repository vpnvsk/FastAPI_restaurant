import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, join
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_cache.decorator import cache


from typing import Dict, List
import asyncio
from database import get_async_session
from items.schemas import ListItemModel
from items.models import category, item
from auth.base_config import current_user
from auth.models import User
from cart.schemas import AddToCart
from cart.models import cart, cart_item
from chat.router import manager

from fastapi import BackgroundTasks

# manager = ConnectionManager()

def notify_clients( message: str):
    asyncio.create_task(manager.broadcast(message))

router = APIRouter(
        prefix='/menu',
        tags=['Menu']
)


@router.get('/',response_model=Dict[str, List[ListItemModel]])
@cache(expire=360)
async def get_menu(session: AsyncSession = Depends(get_async_session)):

    query = select(category.c.name, item.c.name, item.c.price).join(category)
    print(query)
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
async def get_menu_item(item_id: int, session: AsyncSession=Depends(get_async_session)):
    
    query = select(item.c.name, item.c.price, item.c.ingridients).where(item.c.id == item_id)
    result = await session.execute(query)

    return [dict(r._mapping) for r in result]


@router.post('/{item_id}')
async def add_to_cart(operation: AddToCart ,item_id: int,background_tasks: BackgroundTasks,session: AsyncSession=Depends(get_async_session),
                       user: User = Depends(current_user) ):
    print(operation)
    for key, value in operation:
        quantity = value

    query = select(cart.c.id).where(cart.c.user_id==user.id)
    res = await session.execute(query)
    cart_obj = res.fetchone()
    if cart_obj is None:
        query = insert(cart).values(user_id=user.id)
        result = await session.execute(query)
        cart_id = result.inserted_primary_key[0]
    else:
        cart_id = cart_obj[0] 
    stmt = insert(cart_item).values(quantity=quantity,cart_id=cart_id,item_id=item_id)
    await session.execute(stmt)
    await session.commit()




    # query = select(item.c.name, cart_item.c.quantity).select_from(
    #     join(item, cart_item, item.c.id == cart_item.c.item_id).join(cart, cart_item.c.cart_id == cart.c.id)
    # ).where(cart.c.is_done == False)
    # result = await session.execute(query)[dict(r._mapping) for r in result]
    cart_items = 'test items'

    # Convert the cart items to JSON


    # Notify connected clients in the background (without waiting for their response)
    cart_items = [{"name": "Test Item", "quantity": 1}]  # Replace with actual item details

    # Enqueue the message instead of broadcasting directly
    await manager.broadcast(json.dumps(cart_items))
    return {"status":"added to cart"}




