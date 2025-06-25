from http import HTTPStatus

from fastapi.testclient import TestClient

from app.models import Claim, User
from app.schemas import ClaimPublic


def make_login(client: TestClient, email: str, password: str) -> str:
    response = client.post(
        "/auth/login", data={"username": email, "password": password}
    )
    assert response.status_code == HTTPStatus.OK
    return response.json()["access_token"]


def test_create_claim(client: TestClient, user: User):
    token = make_login(client, user.email, user.clean_password)
    response = client.post(
        "/claim",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": "unique_claim"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["description"] == "unique_claim"


def test_create_claim_already_exists(
    client: TestClient, user: User, user_create_claim: Claim
):
    token = make_login(client, user.email, user.clean_password)
    response = client.post(
        "/claim",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": user_create_claim.description},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Claim already exists"


def test_find_many_claims(client: TestClient, user: User, user_create_claim: Claim):
    claim_schema = ClaimPublic.model_validate(user_create_claim).model_dump()
    token = make_login(client, user.email, user.clean_password)
    response = client.get(
        "/claim",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"claims": [claim_schema]}


def test_find_claim_by_id(client: TestClient, user: User, user_create_claim: Claim):
    token = make_login(client, user.email, user.clean_password)
    claim_id = user_create_claim.id
    response = client.get(
        f"/claim/{claim_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == claim_id


def test_find_claim_by_id_not_found(client: TestClient, user: User):
    token = make_login(client, user.email, user.clean_password)
    response = client.get(
        "/claim/999999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Claim not found"


def test_delete_claim(client: TestClient, user: User, user_create_claim: Claim):
    token = make_login(client, user.email, user.clean_password)
    response = client.delete(
        f"/claim/{user_create_claim.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Claim deleted"


def test_delete_claim_not_found(client: TestClient, user: User):
    token = make_login(client, user.email, user.clean_password)
    response = client.delete(
        "/claim/999999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Claim not found"
