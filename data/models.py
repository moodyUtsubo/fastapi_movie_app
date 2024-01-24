from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from .database import Base

from enum import Enum


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     username = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)


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