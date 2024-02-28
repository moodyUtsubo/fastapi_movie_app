from typing import List, Optional

from pydantic import BaseModel

from ..models.user_models import Role


class UserBase(BaseModel):
    full_name: str
    email: str
    username: str
    role: Role    


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    disabled: bool

    class Config:
        orm_mode = True