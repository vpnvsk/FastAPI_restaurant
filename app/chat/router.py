from typing import List
import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel
from sqlalchemy import insert, select, join
from sqlalchemy.ext.asyncio import AsyncSession

from cart.models import cart, cart_item
from items.models import item


from database import async_session_maker, get_async_session


router = APIRouter(
    prefix='/chat',
    tags=["Chat"]
)


# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)

#     async def broadcast(self, message: str, ):

#         for connection in self.active_connections:
#             await connection.send_text(message)
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

    # async def enqueue_message(self, message: str):
    #     await self.message_queue.put(message)

    # async def process_message_queue(self):
    #     while True:
    #         message = await self.message_queue.pop()
    #         await self.broadcast(message)


manager = ConnectionManager()

@router.get("/last_messages")
async def get_last_messages(
        session: AsyncSession = Depends(get_async_session),
):
    query = select(item.c.name, cart_item.c.quantity).select_from(
        join(item, cart_item, item.c.id == cart_item.c.item_id).join(cart, cart_item.c.cart_id == cart.c.id)
    ).where(cart.c.is_done == False)
    result = await session.execute(query)
    messages = [dict(r._mapping) for r in result]
    print(messages)
    return messages

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket ):

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client left the chat")





