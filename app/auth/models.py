from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, MetaData
from app.database import Base


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True)
    __table_args__ = {'extend_existing': True}

class User(SQLAlchemyBaseUserTable[int],Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"))
    email = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable =False )
    is_superuser = Column(Boolean, default=False, nullable =False )
    is_verified = Column(Boolean, default=False, nullable =False )
    __table_args__ = {'extend_existing': True}