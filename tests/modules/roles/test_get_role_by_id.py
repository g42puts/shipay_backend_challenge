from http import HTTPStatus
from fastapi.testclient import TestClient

from app.models import Role, User


def test_get_role_by_id(
    client: TestClient, admin_user: User, user_role: Role, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.get(
        f"/role/{user_role.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == user_role.id
    assert data["description"] == "user"


def test_get_role_by_id_not_exists(
    client: TestClient, admin_user: User, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.get(
        f"/role/999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Role not found"
