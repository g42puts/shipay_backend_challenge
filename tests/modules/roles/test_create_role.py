from http import HTTPStatus
from fastapi.testclient import TestClient

from app.models import Role, User


def test_create_role(client: TestClient, admin_user: User, make_login_func):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.post(
        "/role",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": "registered"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["description"] == "registered"
    assert response.json()["id"]


def test_create_role_already_exists(
    client: TestClient, admin_user: User, user_role: Role, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.post(
        "/role",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": user_role.description},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Role already exists"
