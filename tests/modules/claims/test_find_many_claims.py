from http import HTTPStatus

from fastapi.testclient import TestClient

from app.models import Claim, User
from app.schemas import ClaimPublic


def test_find_many_claims(
    client: TestClient, admin_user: User, user_create_claim: Claim, make_login_func
):
    claim_schema = ClaimPublic.model_validate(user_create_claim).model_dump()
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.get(
        "/claim",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"claims": [claim_schema]}
