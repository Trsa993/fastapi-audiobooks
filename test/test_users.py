import pytest
from jose import jwt
from app import schemas
from app.config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def test_create_user(client):
    res = client.post("/users/", json={"email": "milos123@mail.com", "password": "123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "milos123@mail.com"
    assert res.status_code == 201