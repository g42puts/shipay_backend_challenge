from http import HTTPStatus

from fastapi.testclient import TestClient

from app.models import Role, User


def test_create_user(client: TestClient, user_role: Role):
    response = client.post(
        "/user",
        json={
            "name": "John Doe",
            "email": "johndoe53@email.com",
            "password": "random_password",
            "role_id": user_role.id,
        },
    )
    assert response.status_code == HTTPStatus.CREATED


def test_create_user_with_incorrect_email_format(client: TestClient, user_role: Role):
    response = client.post(
        "/user",
        json={
            "name": "John Doe",
            "email": "johndoe53",
            "role_id": user_role.id,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Invalid email format"


def test_create_user_without_password(client: TestClient, user_role: Role):
    response = client.post(
        "/user",
        json={
            "name": "John Doe",
            "email": "johndoe53@email.com",
            "role_id": user_role.id,
        },
    )
    assert response.status_code == HTTPStatus.CREATED


def test_email_already_exists(client: TestClient, admin_user: User, user_role: Role):
    response = client.post(
        "/user",
        json={
            "name": "John Doe",
            "email": admin_user.email,
            "password": "random_password",
            "role_id": user_role.id,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Email already exists"
