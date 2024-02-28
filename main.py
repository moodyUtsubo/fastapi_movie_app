from fastapi import FastAPI

from postgres_session.database import engine, Base

from routers import movies, users

ACCESS_TOKEN_EXPIRE_MINUTES = 30

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(movies.router)

@app.get("/")
async def root():
    return {"Greetings": "Hello Movie Lovers!"}