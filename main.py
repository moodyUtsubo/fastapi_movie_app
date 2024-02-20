from fastapi import FastAPI

from data import models
from data.database import engine

from routers import movies, users

ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(movies.router)

@app.get("/")
async def root():
    return {"Greetings": "Hello Movie Lovers!"}


# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()