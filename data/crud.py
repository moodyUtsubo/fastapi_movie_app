from sqlalchemy.orm import Session

from . import models, schemas


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).offset(skip).limit(limit).all()


def get_movie(db: Session, id: int):
    return db.query(models.Movie).filter(models.Movie.id == id).first()


def get_movies_by_name(db: Session, name: str):
    return db.query(models.Movie).filter(models.Movie.name.contains(name)).all()


def get_movies_by_type(db: Session, type: str):
    return db.query(models.Movie).filter(models.Movie.type == type).all()


def get_movies_by_genre(db: Session, genre: list):
    return db.query(models.Movie).filter(models.Movie.genres.contains(genre)).all()


def create_movies(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(name=movie.name, type=movie.type, genres=movie.genres)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def update_movies_name(db: Session, id: int, name: str):
    db.query(models.Movie).filter(models.Movie.id == id).update({models.Movie.name: name})
    db.commit()

def update_movies_type(db: Session, id: int, type: str):
    db.query(models.Movie).filter(models.Movie.id == id).update({models.Movie.type: type})
    db.commit()

def update_movies_genres(db: Session, id: int, genre: list):
    db.query(models.Movie).filter(models.Movie.id == id).update({models.Movie.genres: genre})
    db.commit()


def delete_movie(db: Session, id: int):
    db.query(models.Movie).filter(models.Movie.id == id).delete()
    db.commit()
    return db.query(models.Movie).all()