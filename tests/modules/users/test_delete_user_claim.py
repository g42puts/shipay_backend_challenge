from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Claim, User, UserClaim


def test_delete_user_claim(
    client: TestClient,
    admin_user: User,
    normal_user: User,
    session: Session,
    make_login_func,
):
    # Cria claim e associa
    claim = Claim(description="test_claim3")
    session.add(claim)
    session.commit()
    user_claim = UserClaim(user_id=normal_user.id, claim_id=claim.id)
    session.add(user_claim)
    session.commit()
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.delete(
        f"/user/claims/{normal_user.id}/claim/{claim.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "User Claim deleted"
    # Garante que foi removido
    user_claim = (
        session.query(UserClaim)
        .filter_by(user_id=normal_user.id, claim_id=claim.id)
        .first()
    )
    assert user_claim is None


def test_delete_user_claim_not_found(
    client: TestClient, admin_user: User, normal_user: User, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.delete(
        f"/user/claims/{normal_user.id}/claim/999999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "User Claim not found"
