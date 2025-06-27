from http import HTTPStatus
from fastapi.testclient import TestClient

from app.models import Role, User


def test_update_role(
    client: TestClient, admin_user: User, user_role: Role, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    new_description = "updated_role_desc"
    response = client.put(
        f"/role/{user_role.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": new_description},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == user_role.id
    assert data["description"] == new_description


def test_update_role_not_exists(client: TestClient, admin_user: User, make_login_func):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.put(
        "/role/9999",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": "desc"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Role not found"
