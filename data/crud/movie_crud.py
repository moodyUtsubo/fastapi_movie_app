from sqlalchemy.orm import Session

from ..schemas import movie_schemas
from ..models import movie_models


def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(movie_models.Movie).offset(skip).limit(limit).all()


def get_movie(db: Session, id: int):
    return db.query(movie_models.Movie).filter(movie_models.Movie.id == id).first()


def create_movies(db: Session, movie: movie_schemas.MovieCreate):
    db_movie = movie_models.Movie(name=movie.name, type=movie.type, genres=movie.genres)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie(db: Session, movie: movie_models.Movie, upd_movie: movie_schemas.MovieUpdate):
    movie_data = upd_movie.dict(exclude_unset=True)
    for key, value in movie_data.items():
        setattr(movie, key, value)
    db.commit()


def delete_movie(db: Session, id: int):
    db.query(movie_models.Movie).filter(movie_models.Movie.id == id).delete()
    db.commit()
    return db.query(movie_models.Movie).all()