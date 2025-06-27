from http import HTTPStatus

from fastapi.testclient import TestClient

from app.models import Claim, User


def test_create_claim(client: TestClient, admin_user: User, make_login_func):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.post(
        "/claim",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": "unique_claim"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["description"] == "unique_claim"


def test_create_claim_already_exists(
    client: TestClient, admin_user: User, user_create_claim: Claim, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.post(
        "/claim",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": user_create_claim.description},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Claim already exists"
