from sqlalchemy import Table, Column, ForeignKey, Integer, String

from database import metadata

category = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String),
    extend_existing=True
)

item = Table(
    "item",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, unique=True, nullable=False),
    Column("ingridients", String),
    Column("price", Integer),
    Column("category_id", Integer, ForeignKey(category.c.id)),
    extend_existing=True
)
