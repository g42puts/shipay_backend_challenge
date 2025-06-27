from http import HTTPStatus
from datetime import datetime, timedelta
from jwt import decode

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User, BlacklistedToken
from app.configs.configs import configs


def test_logout_adds_token_to_blacklist(
    client: TestClient, session: Session, admin_user: User, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Logout successfully"

    payload = decode(token, configs.SECRET_KEY, algorithms=[configs.ALGORITHM])
    assert "jti" in payload, "Token JWT não possui o campo 'jti'"
    jti = payload["jti"]
    blacklisted = session.query(BlacklistedToken).filter_by(jti=jti).first()
    assert blacklisted is not None


def test_logout_blacklisted(
    client: TestClient, session: Session, admin_user: User, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    payload = decode(token, configs.SECRET_KEY, algorithms=[configs.ALGORITHM])
    jti = payload["jti"]
    # Adiciona o token à blacklist
    blacklisted = BlacklistedToken(
        jti=jti,
        user_id=admin_user.id,
        created_at=datetime.now(),
        expires_at=datetime.now()
        + timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_IN_MINUTES),
    )
    session.add(blacklisted)
    session.commit()
    # Tenta logout
    response = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "Token is blacklisted"
