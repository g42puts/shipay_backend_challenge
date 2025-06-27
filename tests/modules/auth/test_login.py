from http import HTTPStatus

from fastapi.testclient import TestClient

from app.models import User


def test_get_token(client: TestClient, admin_user: User):
    response = client.post(
        "/auth/login",
        data={"username": admin_user.email, "password": admin_user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token


def test_get_token_with_wrong_password_should_return_error(
    client: TestClient, admin_user: User
):
    response = client.post(
        "/auth/login",
        data={"username": admin_user.email, "password": "wrong_password"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Incorrect password"


def test_token_inexistent_user(client: TestClient):
    response = client.post(
        "/auth/login",
        data={"username": "random_email@email.com", "password": "random_password"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Incorrect email or password"
