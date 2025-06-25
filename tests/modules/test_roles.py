from http import HTTPStatus
from fastapi.testclient import TestClient

from app.models import Role, User
from app.schemas import RolePublic


def make_login(client: TestClient, email: str, password: str) -> str:
    response = client.post(
        "/auth/login", data={"username": email, "password": password}
    )
    assert response.status_code == HTTPStatus.OK
    return response.json()["access_token"]


def test_create_role(client: TestClient, user: User):
    token = make_login(client, user.email, user.clean_password)
    response = client.post(
        "/role",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": "registered"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["description"] == "registered"
    assert response.json()["id"]


def test_create_role_already_exists(client: TestClient, user: User, user_role: Role):
    token = make_login(client, user.email, user.clean_password)
    response = client.post(
        "/role",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": user_role.description},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Role already exists"


def test_get_many_roles(
    client: TestClient, user: User, user_role: Role, admin_role: Role
):
    token = make_login(client, user.email, user.clean_password)
    response = client.get(
        "/role",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "roles": [
            RolePublic.model_validate(admin_role).model_dump(),
            RolePublic.model_validate(user_role).model_dump(),
        ]
    }


def test_get_role_by_id(client: TestClient, user: User, user_role: Role):
    token = make_login(client, user.email, user.clean_password)
    response = client.get(
        f"/role/{user_role.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == user_role.id
    assert data["description"] == "user"


def test_get_role_by_id_not_exists(client: TestClient, user: User):
    token = make_login(client, user.email, user.clean_password)
    response = client.get(
        f"/role/999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Role not found"


def test_delete_role(client: TestClient, user: User, user_role: Role):
    token = make_login(client, user.email, user.clean_password)
    response = client.delete(
        f"/role/{user_role.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Role deleted"


def test_delete_role_not_exists(client: TestClient, user: User):
    token = make_login(client, user.email, user.clean_password)
    response = client.delete(
        f"/role/999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Role not found"


def test_update_role(client: TestClient, user: User, user_role: Role):
    token = make_login(client, user.email, user.clean_password)
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


def test_update_role_not_exists(client: TestClient, user: User):
    token = make_login(client, user.email, user.clean_password)
    response = client.put(
        "/role/9999",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": "desc"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Role not found"
