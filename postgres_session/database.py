from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()

#connect to a database
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')

#create a SQLalchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

#a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()