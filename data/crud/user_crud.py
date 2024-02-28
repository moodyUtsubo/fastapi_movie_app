from sqlalchemy.orm import Session

from ..schemas import user_schemas
from ..models import user_models

from auth.jwt import get_password_hash


def get_user_by_username(db: Session, username: str):
    return db.query(user_models.User).filter(user_models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(user_models.User).filter(user_models.User.email == email).first()


def get_user_by_id(db: Session, id: int):
    return db.query(user_models.User).filter(user_models.User.id == id).first()


def create_user(db: Session, user: user_schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = user_models.User(full_name=user.full_name, email=user.email, 
                          username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def user_role(db: Session, id: int, role: str):
    db.query(user_models.User).filter(user_models.User.id == id).update({user_models.User.role: role})
    db.commit()