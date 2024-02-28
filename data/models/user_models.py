from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY

from postgres_session.database import Base

from enum import Enum


class User(Base):
    __tablename__ = "watchers"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    role = Column(String, default='user')


class Role(str, Enum):
    user = "user"
    admin = "admin"