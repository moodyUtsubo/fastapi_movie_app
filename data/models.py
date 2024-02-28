from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
# from sqlalchemy.orm import relationship

from .database import Base

from enum import Enum

#Tách ra thành module models chứa nhiều file, chứ sau có mấy chục model e viết hết vào đây à?
class User(Base):
    __tablename__ = "watchers"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    role = Column(String, default='user')


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    type = Column(String, index=True)
    genres = Column(ARRAY(String), index=True)


class Type(str, Enum):
    animation = "Animation"
    liveaction = "Live Action"


class Genre(str, Enum):
    scifi = "Sci-Fi"
    comedy = "Comedy"
    action = "Action"
    fantasy = "Fantasy"
    horror = "Horror"
    romance = "Romance"
    western = "Western"
    thriller = "Thriller"


class Role(str, Enum):
    user = "user"
    admin = "admin"