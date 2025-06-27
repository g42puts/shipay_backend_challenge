from http import HTTPStatus

from fastapi.testclient import TestClient

from app.models import Claim, User


def test_delete_claim(
    client: TestClient, admin_user: User, user_create_claim: Claim, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.delete(
        f"/claim/{user_create_claim.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Claim deleted"


def test_delete_claim_not_found(client: TestClient, admin_user: User, make_login_func):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.delete(
        "/claim/999999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Claim not found"
