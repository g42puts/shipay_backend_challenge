from http import HTTPStatus
from typing import Callable

from fastapi.testclient import TestClient

from app.models import User


def test_find_user_by_id(
    client: TestClient,
    admin_user: User,
    make_login_func,
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.get(
        f"/user/{admin_user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["email"] == admin_user.email


def test_find_user_by_id_return_error(
    client: TestClient, admin_user: User, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.get("/user/223", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"
