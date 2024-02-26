from fastapi.testclient import TestClient
from datetime import timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.pool import StaticPool

import sys
sys.path.append("..")
import main
import auth.jwt
# import data.schemas
import data.models

SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/database"

#Tách đoạn này thành 1 file setup test, đặt lại tên file test theo từng module chứ ko đặt chung hết thành 1 file như
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

data.models.Base.metadata.create_all(bind=engine)
này
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

main.app.dependency_overrides[auth.jwt.get_db] = override_get_db


access_token_expires = timedelta(minutes=30)

client = TestClient(main.app)


# Tên function khi viết test cần viết đầy đủ nghĩa, ví dụ test_signup_success
def test_signup():
    response = client.post("/signup/", params={"full_name": "Mary Jane", "email": "maryjane@example.com", "username": "maryjane", "password": "13579"})
    assert response.status_code == 200, response.text
    db = response.json()
    assert db["username"] == "maryjane"
    assert db["email"] == "maryjane@example.com"
    assert db["role"] == "user"


# test_signup_return_400_existed_email
def test_existed_email():
    response = client.post("/signup/", params={"full_name": "Mary Jane", "email": "maryjane@example.com", "username": "maryjane", "password": "13579"})
    assert response.status_code == 400
    assert response.json() == {"detail":"Email already registered"}


def test_existed_username():
    response = client.post("/signup/", params={"full_name": "Mary Jane", "email": "maryjane1@example.com", "username": "maryjane", "password": "13579"})
    assert response.status_code == 400
    assert response.json() == {"detail":"Username already existed"}


#Tach movie va user thanh 2 file test rieng
def test_create_movies():
    response = client.post("/api/v1/movies/", headers={
        "Authorization": f'Bearer {auth.jwt.create_access_token(data={"sub": "johndoe"}, expires_delta=access_token_expires)}'
    }, params={"name":"Avatar", "type":"Live Action", "genres":["Sci-Fi", "Fantasy", "Action"]})
    
    assert response.status_code == 200, response.text
    db = response.json()
    assert db["name"] == "Avatar"
    assert db["type"] == "Live Action"
    assert db["genres"] == ["Sci-Fi", "Fantasy", "Action"]
    
    response = client.get("/api/v1/movies/?name=Ava", headers={
        "Authorization": f'Bearer {auth.jwt.create_access_token(data={"sub": "johndoe"}, expires_delta=access_token_expires)}'
    })
    assert response.status_code == 200, response.text
    db = response.json()
    db = db[0]
    assert db["name"] == "Avatar"
    assert db["type"] == "Live Action"
    assert db["genres"] == ["Sci-Fi", "Fantasy", "Action"]


def test_not_admin():
    response = client.post("/api/v1/movies/", headers={
        "Authorization": f'Bearer {auth.jwt.create_access_token(data={"sub": "maryjane"}, expires_delta=access_token_expires)}'
    }, params={"name":"Up", "type":"Animation", "genres":["Comedy","Action"]})
    assert response.status_code == 400
    assert response.json() == {"detail":"Inactive admin"}
    
    response = client.put("/api/v1/movies/1", headers={
        "Authorization": f'Bearer {auth.jwt.create_access_token(data={"sub": "maryjane"}, expires_delta=access_token_expires)}'
    }, params={"name":"Avatar 2"})
    assert response.status_code == 400
    assert response.json() == {"detail":"Inactive admin"}
    
    response = client.delete("/api/v1/movies/1", headers={
        "Authorization": f'Bearer {auth.jwt.create_access_token(data={"sub": "maryjane"}, expires_delta=access_token_expires)}'
    })
    assert response.status_code == 400
    assert response.json() == {"detail":"Inactive admin"}


def test_get_movies():
    response = client.get("/api/v1/movies/?name=Ava", headers={
        "Authorization": f'Bearer {auth.jwt.create_access_token(data={"sub": "maryjane"}, expires_delta=access_token_expires)}'
    })
    assert response.status_code == 200
    assert response.json() == [{"name": "Avatar", 
                                "type": "Live Action",
                                "genres": [
                                    "Sci-Fi",
                                    "Fantasy",
                                    "Action"
                                    ],
                                "id": 1}]


def test_unauth():
    response = client.get("/api/v1/movies/?name=Ava")
    assert response.status_code == 401
    assert response.json() == {"detail":"Not authenticated"}

# def test_delete_movie():
#     response = client.delete("/api/v1/movies/19")
