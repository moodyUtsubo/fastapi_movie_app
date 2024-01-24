from typing import List, Union

from pydantic import BaseModel

from .models import Type, Genre


class MovieBase(BaseModel):
    name: str
    type: Type
    genres: List[Genre]


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int
    # owner_id: int

    class Config:
        orm_mode = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: List[Item] = []

#     class Config:
#         orm_mode = True