from typing import Union

from pydantic import BaseModel


fake_users_db = {
    "thupnt": {
        "username": "thupnt",
        "full_name": "Thu Pham",
        "email": "thupnt@example.com",
        "hashed_password": "$2b$12$6B7S.WUcMVZrQRQ/voJtk.UAmROu/2aKoTutVRyAra9IMqiSbLuP6",
        "disabled": False,
        "role": "admin",
    },
    
    "hieuvt": {
        "username": "hieuvt",
        "full_name": "Hieu Vu",
        "email": "hieuvt@example.com",
        "hashed_password": "$2b$12$6v.uCDQMuQYqNpnNDSziQ.V1YFcuanzelYK0tQGuR.1cGLioM5mHO",
        "disabled": False,
        "role": "user",
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    role: Union[str, None] = None


class UserInDB(User):
    hashed_password: str