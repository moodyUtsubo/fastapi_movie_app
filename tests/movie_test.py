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


def test_create_movies_success():
    response = client.post("/api/v1/movies/", headers={
        "Authorization": f'Bearer {auth.jwt.create_access_token(data={"sub": "johndoe"}, expires_delta=access_token_expires)}'
    }, json={"name":"Avatar", "type":"Live Action", "genres":["Sci-Fi", "Fantasy", "Action"]})
    
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


def test_get_movies_success():
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