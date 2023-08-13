import json
from collections import defaultdict
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy import select, join, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from cart.models import cart, cart_item
from database import get_async_session
from items.models import item

router = APIRouter(
    prefix='/chat',
    tags=["Chat"]
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.message_queue: List[str] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


async def update_cart_status(user_name: str, session: AsyncSession = Depends(get_async_session)):
    stmt = update(cart).where(cart.c.user_id == User.id).values(is_done=True).where(User.name == user_name)
    await session.execute(stmt)
    await session.commit()
    return {"message": f"Carts for user {user_name} have been updated"}


manager = ConnectionManager()


@router.get("/last_messages")
async def get_last_messages(
        session: AsyncSession = Depends(get_async_session),
):
    query = select(item.c.name, cart_item.c.quantity, User.name).select_from(
        join(item, cart_item, item.c.id == cart_item.c.item_id).join(cart,
                                                                     cart_item.c.cart_id == cart.c.id).join(User,
                                                                     cart.c.user_id == User.id)
    ).where(cart.c.is_done == False, cart.c.is_ordered == True)
    result = await session.execute(query)
    user_items = defaultdict(list)
    for row in result:
        item_data = dict(row._mapping)
        user_name = item_data.pop("name_1")
        user_items[user_name].append(item_data)

    output = [{user_name: user_items[user_name]} for user_name in user_items]
    print(output)
    return output


# @router.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket ):

#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             json_data = json.dumps(data)
#             message_data = json.loads(data)
#             for message in message_data:
#                 user_name = message.get("userName")
#                 if user_name:
#                     # Update the database for the corresponding user name
#                     await update_cart_status(user_name)
#                     # Broadcast a message to all clients if needed
#                     await manager.broadcast(f"{user_name} has marked their order as done")
#             await manager.broadcast(f"says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client left the chat")
@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, session: AsyncSession = Depends(get_async_session)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)  # Parse the incoming JSON data
            for message in message_data:
                user_name = message.get("userName")
                if user_name:
                    # Update the database for the corresponding user name
                    stmt = update(cart).where(cart.c.user_id == User.id).values(is_done=True).where(
                        User.name == user_name)
                    await session.execute(stmt)
                    await session.commit()
                    # Broadcast a message to all clients if needed
                    await manager.broadcast(f"{user_name} has marked their order as done")
            await manager.broadcast(f"says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client left the chat")
