from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Claim, User, UserClaim, BlacklistedToken


def test_delete_user(
    client: TestClient, admin_user: User, session: Session, make_login_func
):
    # Remove tokens da blacklist antes de deletar o usuário
    session.query(UserClaim).filter_by(user_id=admin_user.id).delete()
    session.query(Claim).filter(Claim.description.like("user:%")).delete()
    session.query(BlacklistedToken).filter_by(user_id=admin_user.id).delete()
    session.commit()
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.delete(
        f"/user/{admin_user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "User deleted"


def test_delete_user_with_admin_role_should_return_ok(
    client: TestClient, admin_user: User, normal_user: User, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.delete(
        f"/user/{normal_user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK


def test_delete_user_with_wrong_user_id(
    client: TestClient, admin_user: User, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.delete("/user/1234", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "User not found"


def test_delete_user_with_admin_role(
    client: TestClient, admin_user: User, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.delete(
        f"/user/{admin_user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
