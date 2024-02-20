from fastapi import APIRouter, Depends, HTTPException, Query

from typing import Union, List
from typing_extensions import Annotated

from sqlalchemy.orm import Session
from data.database import SessionLocal

from auth.jwt import get_current_active_user, get_current_active_admin, get_db

from data import crud, models, schemas


router = APIRouter()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@router.post("/api/v1/movies/", response_model=schemas.Movie, tags=["movies"])
def create_movie(current_admin: Annotated[schemas.User, Depends(get_current_active_admin)], 
                 name: str, type: models.Type, genres: List[models.Genre] = Query(...), db: Session = Depends(get_db)):
    movie = models.Movie(name=name, type=type, genres=genres)
    # db_user = crud.get_movies(db, email=user.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_movies(db=db, movie=movie)


@router.get("/api/v1/movies/", response_model=List[schemas.Movie], tags=["movies"])
def read_movies(current_user: Annotated[schemas.User, Depends(get_current_active_user)], 
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


@router.put("/api/v1/movies/{id}", response_model=schemas.Movie, tags=["movies"])
def update_movie(current_user: Annotated[schemas.User, Depends(get_current_active_admin)], id: int,
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


@router.delete("/api/v1/movies/{id}", response_model=List[schemas.Movie], tags=["movies"])
def delete_movie(current_user: Annotated[schemas.User, Depends(get_current_active_admin)], id: int, db: Session = Depends(get_db)):
    movie = crud.get_movie(db, id=id)
    if movie:
        db_movie = crud.delete_movie(db, id=id)
        return db_movie
    raise HTTPException(status_code=404, detail=f"Failed, movie with id {id} not found!")