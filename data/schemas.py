from typing import List, Union

from pydantic import BaseModel

from .models import Type, Genre, Role


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


class UserBase(BaseModel):
    full_name: str
    email: str
    username: str
    role: Role
    


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    disabled: bool
    # items: List[Item] = []

    class Config:
        orm_mode = True