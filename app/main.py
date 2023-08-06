import uvicorn

from fastapi import FastAPI, BackgroundTasks
import asyncio
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware

from redis import asyncio as aioredis

from app.auth.base_config import auth_backend, fastapi_users
from app.auth.schemas import UserRead, UserCreate
from app.items.router import router as router_menu
from app.cart.router import router as router_cart
from app.pages.router import router as router_pages
from app.chat.router import router as router_chat
from app.chat.router import ConnectionManager
from app.payment.router import router as router_payment


manager = ConnectionManager()

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8080,reload=True,workers=3)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_menu)
app.include_router(router_cart)
app.include_router(router_chat)
app.include_router(router_pages)
app.include_router(router_payment)

origins = [
    "http://localhost:8000",
    "http://localhost",
    "http://127.0.0.1:8000",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# app.add_event_handler("startup", lambda: asyncio.create_task(manager.process_message_queue()))

