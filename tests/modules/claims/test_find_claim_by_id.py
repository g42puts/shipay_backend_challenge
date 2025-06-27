from http import HTTPStatus

from fastapi.testclient import TestClient

from app.models import Claim, User


def test_find_claim_by_id(
    client: TestClient, admin_user: User, user_create_claim: Claim, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    claim_id = user_create_claim.id
    response = client.get(
        f"/claim/{claim_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == claim_id


def test_find_claim_by_id_not_found(
    client: TestClient, admin_user: User, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.get(
        "/claim/999999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Claim not found"
