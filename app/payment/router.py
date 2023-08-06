import json
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, join, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.base_config import current_user
from app.items.models import item
from app.cart.models import cart, cart_item
from app.chat.router import manager


from app.database import get_async_session


router = APIRouter(
        prefix='/payment',
        tags=['Payment']
)

@router.get('/')
async def pay_for_order(session: AsyncSession=Depends(get_async_session), user: User=Depends(current_user)):
    query = (
        select(cart_item.c.quantity, item.c.price, item.c.name,)
        .select_from(
            join(item, cart_item, item.c.id == cart_item.c.item_id)
            .join(cart, cart_item.c.cart_id == cart.c.id)
        )
        .where(cart.c.user_id == user.id, cart.c.is_ordered == False)
    )
    result = await session.execute(query)
    # cart_items = [{user.name: []}]
    
    # for row in result:
    #     item_data = {
    #         "quantity": row.quantity,
    #         "name": row.name
    #     }
    #     cart_items[0][user.name].append(item_data)
    cart_items = [dict(r._mapping) for r in result]
    # cart_items = [{"quantity": quantity, "name": name} for quantity, name in result]    
    final_value = sum(item["quantity"] * item["price"] for item in cart_items)

    """     PAYMENT IMITATION     """
    payment_status = True

    if payment_status:

        stmt = update(cart).where(cart.c.user_id==user.id, cart.c.is_ordered ==False).values(is_ordered=True)
        await session.execute(stmt)
        # query = select(item.c.name, cart_item.c.quantity, User.name).select_from(
        # join(item, cart_item, item.c.id == cart_item.c.item_id).join(cart, cart_item.c.cart_id == cart.c.id).join(User, cart.c.user_id==User.id)
        # ).where(cart.c.is_done == False)
        # result = await session.execute(query)
        # user_items = defaultdict(list)
        # for row in result:
        #     item_data = dict(row._mapping)
        #     user_name = item_data.pop("name_1")  # Extract the user name and remove it from the dictionary
        #     user_items[user_name].append(item_data)

# Convert the defaultdict to the desired format
        # ######output = [{user_name: user_items[user_name]} for user_name in user_items]
        await session.commit()
        ''' test'''
        # for item_ in cart_items:
        #     item_.pop("price", None)
        # cart_items = [{user.name:cart_items}]
        # cart_items_json = json.dumps(cart_items)
        # print(cart_items_json)
        user_cart_items = defaultdict(list)
        for item_ in cart_items:
            user_cart_items[user.name].append({"name": item_["name"], "quantity": item_["quantity"]})

        # Convert the defaultdict to the desired format
        cart_items_output = [{user_name: user_cart_items[user_name]} for user_name in user_cart_items]

        cart_items_json = json.dumps(cart_items_output)
        print(cart_items_json)

        await manager.broadcast(cart_items_json)
        return {"status":"succes"}
    return{"status":"failure"}





