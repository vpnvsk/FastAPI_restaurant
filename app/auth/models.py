from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table

from database import Base, metadata, metadata1

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("role_name", String, unique=True, index=True),
    extend_existing=True
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, index=True),

    Column("name", String),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
    Column("email", String, nullable=True),
    extend_existing=True
)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey(role.c.id))
    email = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    __table_args__ = {'extend_existing': True}
