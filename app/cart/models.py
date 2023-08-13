from sqlalchemy import Table, Column, ForeignKey, Integer, Boolean

from auth.models import user
from database import metadata
from items.models import item

cart = Table(
    "cart",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('is_ordered', Boolean, default=False, nullable=False),
    Column('user_id', Integer, ForeignKey(user.c.id), nullable=False),
    Column('is_done', Boolean, default=False, nullable=False),
    extend_existing=True
)

cart_item = Table(
    "cart_item",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('quantity', Integer, nullable=False),
    Column('item_id', Integer, ForeignKey(item.c.id), nullable=False),
    Column('cart_id', Integer, ForeignKey(cart.c.id), nullable=False),
    extend_existing=True
)
