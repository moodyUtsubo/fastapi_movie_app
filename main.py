from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

# import data.crud, data.models, data.schemas
from data import crud, models, schemas
from data.database import SessionLocal, engine

from typing import Union, List
from typing_extensions import Annotated

from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from auth.userdb import fake_users_db, Token, User
from auth.jwt import authenticate_user, create_access_token, get_current_active_user, get_current_active_admin

ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/token", tags=["user"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
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


@app.get("/users/me/", response_model=User, tags=["user"])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@app.post("/api/v1/movies/", response_model=schemas.Movie, tags=["movies"])
def create_movie(current_admin: Annotated[User, Depends(get_current_active_admin)], 
                 name: str, type: models.Type, genres: List[models.Genre] = Query(None), db: Session = Depends(get_db)):
    movie = models.Movie(name=name, type=type, genres=genres)
    # db_user = crud.get_movies(db, email=user.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_movies(db=db, movie=movie)


@app.get("/api/v1/movies/", response_model=List[schemas.Movie], tags=["movies"])
def read_movies(current_user: Annotated[User, Depends(get_current_active_user)], 
                name: Annotated[Union[str, None], Query(max_length=100)] = None, 
                type: models.Type = None, 
                genres: List[models.Genre] = Query(None), 
                skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if name:
        movies = crud.get_movies_by_name(db, name=name)
        if movies != []:
            return movies
        raise HTTPException(status_code=404, detail=f"Failed, movie {name} not found!")
    elif type:
        movies = crud.get_movies_by_type(db, type=type)
        if movies != []:
            return movies
        raise HTTPException(status_code=404, detail=f"Failed, movie with type {type} not found!")
    elif genres:
        movies = crud.get_movies_by_genre(db, genre=genres)
        if movies != []:
            return movies
        raise HTTPException(status_code=404, detail=f"Failed, movie with genres {genres} not found!")
    else:
        movies = crud.get_movies(db, skip=skip, limit=limit)
        return movies


@app.put("/api/v1/movies/{id}", response_model=schemas.Movie, tags=["movies"])
def update_movie(current_user: Annotated[User, Depends(get_current_active_admin)], id: int,
                name: Annotated[Union[str, None], Query(max_length=100)] = None, 
                type: models.Type = None, 
                genres: List[models.Genre] = Query(None), 
                db: Session = Depends(get_db)):
    movie = crud.get_movie(db, id=id)
    if movie:
        if name:
            crud.update_movies_name(db, id=id, name=name)
        if type:
            crud.update_movies_type(db, id=id, type=type)
        if genres:
            crud.update_movies_genres(db, id=id, genre=genres)
        movie = crud.get_movie(db, id=id)
        return movie
    raise HTTPException(status_code=404, detail=f"Failed, movie with id {id} not found!")


@app.delete("/api/v1/movies/{id}", response_model=List[schemas.Movie], tags=["movies"])
def delete_movie(current_user: Annotated[User, Depends(get_current_active_admin)], id: int, db: Session = Depends(get_db)):
    movie = crud.get_movie(db, id=id)
    if movie:
        db_movie = crud.delete_movie(db, id=id)
        return db_movie
    raise HTTPException(status_code=404, detail=f"Failed, movie with id {id} not found!")