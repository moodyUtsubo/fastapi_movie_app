from fastapi import APIRouter, Depends, HTTPException, Query

from typing import Union, List
from typing_extensions import Annotated

from sqlalchemy.orm import Session

from auth.jwt import get_current_active_user, get_current_active_admin

from data.models import movie_models
from data.schemas import movie_schemas, user_schemas
from data.crud import movie_crud

from postgres_session.database import get_db


router = APIRouter()


@router.post("/api/v1/movies/", response_model=movie_schemas.Movie, tags=["movies"])
def create_movie(_: Annotated[user_schemas.User, Depends(get_current_active_admin)], 
                 movie: movie_schemas.MovieCreate, db: Session = Depends(get_db)):
    return movie_crud.create_movies(db=db, movie=movie)


@router.get("/api/v1/movies/", response_model=List[movie_schemas.Movie], tags=["movies"])
def read_movies(_: Annotated[user_schemas.User, Depends(get_current_active_user)], 
                name: Annotated[Union[str, None], Query(max_length=100)] = None, 
                type: movie_models.Type = None, 
                genres: List[movie_models.Genre] = Query(None), 
                skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = db.query(movie_models.Movie)
    if name:
        movies = movies.filter(movie_models.Movie.name.contains(name))
    if type:
        movies = movies.filter(movie_models.Movie.type == type)
    if genres:
        movies = movies.filter(movie_models.Movie.genres.contains(genres))
    movies = movies.offset(skip).limit(limit).all()
    if movies:
        return movies
    raise HTTPException(status_code=404, detail=f"Failed, movies with input queries not found!")


@router.patch("/api/v1/movies/{id}", response_model=movie_schemas.Movie, tags=["movies"])
def update_movie(_: Annotated[user_schemas.User, Depends(get_current_active_admin)], id: int,
                upd_movie: movie_schemas.MovieUpdate, 
                db: Session = Depends(get_db)):
    movie = movie_crud.get_movie(db, id=id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Failed, movie with id {id} not found!")
    movie_crud.update_movie(db, movie=movie, upd_movie=upd_movie)
    movie = movie_crud.get_movie(db, id=id)
    return movie


@router.delete("/api/v1/movies/{id}", response_model=List[movie_schemas.Movie], tags=["movies"])
def delete_movie(_: Annotated[user_schemas.User, Depends(get_current_active_admin)], id: int, db: Session = Depends(get_db)):
    movie = movie_crud.get_movie(db, id=id)
    if movie:
        db_movie = movie_crud.delete_movie(db, id=id)
        return db_movie
    raise HTTPException(status_code=404, detail=f"Failed, movie with id {id} not found!")
