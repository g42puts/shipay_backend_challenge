from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Claim, User, UserClaim


def test_update_user_claim(
    client: TestClient,
    admin_user: User,
    normal_user: User,
    session: Session,
    make_login_func,
):
    # Cria claim
    claim = Claim(description="test_claim")
    session.add(claim)
    session.commit()
    # user é admin
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.post(
        f"/user/claims/{normal_user.id}/claim/{claim.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Claim added to user."
    # Garante que existe no banco
    user_claim = (
        session.query(UserClaim)
        .filter_by(user_id=normal_user.id, claim_id=claim.id)
        .first()
    )
    assert user_claim


def test_update_user_claim_already_exists(
    client: TestClient,
    admin_user: User,
    normal_user: User,
    session: Session,
    make_login_func,
):
    # Cria claim e já associa
    claim = Claim(description="test_claim2")
    session.add(claim)
    session.commit()
    user_claim = UserClaim(user_id=normal_user.id, claim_id=claim.id)
    session.add(user_claim)
    session.commit()
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.post(
        f"/user/claims/{normal_user.id}/claim/{claim.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert (
        response.status_code == HTTPStatus.BAD_REQUEST
        or response.status_code == HTTPStatus.CONFLICT
    )
