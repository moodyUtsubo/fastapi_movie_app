from fastapi import APIRouter, Depends, HTTPException, status

from datetime import timedelta

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from auth.token import Token
from data import schemas, crud, models
from auth.jwt import authenticate_user, create_access_token, get_current_active_user, get_db, get_password_hash, get_current_active_admin

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

@router.post("/token", tags=["user"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=schemas.User, tags=["user"])
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)]
):
    return current_user


@router.post("/signup/", response_model=schemas.User, tags=["user"])
async def signup(full_name: str, email: str, username: str, password: str, 
                 db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_username(db, username=username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already existed")
    hashed_password = get_password_hash(password)
    user = models.User(full_name=full_name, email=email, username=username, hashed_password=hashed_password)
    return crud.create_user(db=db, user=user)


@router.put("/role/{id}", response_model=schemas.User, tags=["user"])
def role(current_admin: Annotated[schemas.User, Depends(get_current_active_admin)], 
               id: int, role: models.Role, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, id=id)
    if db_user:
        # if role:
        crud.user_role(db, id=id, role=role)
        db_user = crud.get_user_by_id(db, id=id)
        return db_user
    raise HTTPException(status_code=404, detail=f'User with id {id} not found')