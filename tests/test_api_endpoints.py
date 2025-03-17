import pytest
from fastapi.testclient import TestClient
from src.main import app
from fastapi.requests import Request
from fastapi.responses import Response
from typing import Optional


@pytest.fixture
def test_user():
    return {"email": "some@mail.ru", "password": "1234456543"}


client = TestClient(app=app)


# def test_register(test_user):
#     response: Response = client.post("/api/v1/register", json=test_user)
#     assert response.status_code == 200


def test_login(test_user):
    response: Response = client.post("/api/v1/login", json=test_user)
    assert response.status_code == 200


def test_create_code(test_user):
    login_response = client.post("/api/v1/login", json=test_user)
    assert login_response.status_code == 200
    
    assert "user_access_token" in client.cookies

    response = client.post(
        "/api/v1/create_code",
        data={"code": "3124124sadas"}
    )
    
    assert response.status_code == 201


def test_logout():
    response: Response = client.post("/api/v1/logout")
    assert response.status_code == 200
