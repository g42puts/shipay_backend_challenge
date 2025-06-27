from http import HTTPStatus
from fastapi.testclient import TestClient

from app.models import Role, User
from app.schemas import RolePublic


def test_get_many_roles(
    client: TestClient,
    admin_user: User,
    user_role: Role,
    admin_role: Role,
    make_login_func,
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
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
