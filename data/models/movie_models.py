from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY

from postgres_session.database import Base

from enum import Enum


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