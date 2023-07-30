from sqlalchemy import  Table,Column, ForeignKey, Integer, String, MetaData
from database import Base

metadata = MetaData()





category = Table(
    "category",
    metadata,
    Column("id",Integer, primary_key=True, index=True),
    Column("name", String),
)

item = Table(
    "item",
    metadata,
    Column("id",Integer, primary_key=True, index=True),
    Column("name",String, unique=True, nullable=False),
    Column("ingridients", String),
    Column("price", Integer),
    Column("category_id", Integer, ForeignKey(category.c.id)),
)