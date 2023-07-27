from sqlalchemy import  Table,Column, ForeignKey, Integer, String, MetaData
from database import Base

metadata = MetaData()

# class Category(Base):
#     __tablename__ = 'category'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
    

# class Item(Base):
#     __tablename__ = 'item'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, nullable=False)
#     ingridients = Column(String)
#     category_id = Column(Integer, ForeignKey('category.id'))
#     price = Column(Integer)



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