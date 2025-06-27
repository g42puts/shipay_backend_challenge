from http import HTTPStatus

from fastapi.testclient import TestClient

from app.schemas import UserPublic
from app.models import User


def test_find_many_users(client: TestClient, admin_user: User, make_login_func):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    user_schema = UserPublic.model_validate(admin_user).model_dump()
    user_schema["created_at"] = user_schema["created_at"].isoformat()
    if user_schema.get("updated_at"):
        user_schema["updated_at"] = user_schema["updated_at"].isoformat()

    response = client.get("/user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}
