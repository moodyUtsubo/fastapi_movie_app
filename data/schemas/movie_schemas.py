from typing import List, Optional

from pydantic import BaseModel

from ..models.movie_models import Type, Genre


class MovieBase(BaseModel):
    name: str
    type: Type
    genres: List[Genre]


class MovieCreate(MovieBase):
    pass


class MovieUpdate(MovieBase):
    name: Optional[str] = None
    type: Optional[Type] = None
    genres: Optional[List[Genre]] = None


class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True