from sqlalchemy import  Table, Column, ForeignKey, Integer, String, MetaData, Boolean
from app.database import Base, metadata

from app.items.models import item
from app.auth.models import User


cart = Table(
    "cart",
    metadata,
    Column('id',Integer, primary_key=True, index=True),
    Column('is_ordered', Boolean, default=False,nullable =False),
    Column('user_id', Integer, ForeignKey(User.id),nullable =False),
    Column('is_done',Boolean, default=False, nullable=False),
)

cart_item = Table(
    "cart_item",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('quantity', Integer,nullable =False),
    Column('item_id', Integer, ForeignKey(item.c.id),nullable =False),
    Column('cart_id', Integer, ForeignKey(cart.c.id), nullable=False),
)