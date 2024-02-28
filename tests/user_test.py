from fastapi.testclient import TestClient
from datetime import timedelta

from setup_test_env import override_get_db, engine

import sys
sys.path.append("..")
import main
import auth.jwt
import postgres_session.database


postgres_session.database.Base.metadata.create_all(bind=engine)


main.app.dependency_overrides[postgres_session.database.get_db] = override_get_db


access_token_expires = timedelta(minutes=30)

client = TestClient(main.app)


def test_signup_success():
    response = client.post("/signup/", json={"full_name": "Mary Jane", "email": "maryjane@example.com", "username": "maryjane", "password": "13579", "disabled": "false", "role": "user"})
    assert response.status_code == 200, response.text
    db = response.json()
    assert db["username"] == "maryjane"
    assert db["email"] == "maryjane@example.com"
    assert db["role"] == "user"


def test_signup_return_400_existed_email():
    response = client.post("/signup/", json={"full_name": "Mary Jane", "email": "maryjane@example.com", "username": "maryjane", "password": "13579", "disabled": "false", "role": "user"})
    assert response.status_code == 400
    assert response.json() == {"detail":"Email already registered"}


def test_signup_return_400_existed_username():
    response = client.post("/signup/", json={"full_name": "Mary Jane", "email": "maryjane1@example.com", "username": "maryjane", "password": "13579", "disabled": "false", "role": "user"})
    assert response.status_code == 400
    assert response.json() == {"detail":"Username already existed"}


def test_not_admin_return_400():
    response = client.post("/api/v1/movies/", headers={
        "Authorization": f'Bearer {auth.jwt.create_access_token(data={"sub": "maryjane"}, expires_delta=access_token_expires)}'
    }, json={"name":"Up", "type":"Animation", "genres":["Comedy","Action"]})
    assert response.status_code == 400
    assert response.json() == {"detail":"Inactive admin"}
    
    response = client.patch("/api/v1/movies/1", headers={
        "Authorization": f'Bearer {auth.jwt.create_access_token(data={"sub": "maryjane"}, expires_delta=access_token_expires)}'
    }, json={"name":"Avatar 2"})
    assert response.status_code == 400
    assert response.json() == {"detail":"Inactive admin"}
    
    response = client.delete("/api/v1/movies/1", headers={
        "Authorization": f'Bearer {auth.jwt.create_access_token(data={"sub": "maryjane"}, expires_delta=access_token_expires)}'
    })
    assert response.status_code == 400
    assert response.json() == {"detail":"Inactive admin"}


def test_unauth_return_401():
    response = client.get("/api/v1/movies/?name=Ava")
    assert response.status_code == 401
    assert response.json() == {"detail":"Not authenticated"}