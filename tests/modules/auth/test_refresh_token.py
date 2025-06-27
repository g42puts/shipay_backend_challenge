from http import HTTPStatus
from datetime import datetime, timedelta
from jwt import decode

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User, BlacklistedToken
from app.configs.configs import configs


def test_refresh_token(client: TestClient, admin_user: User):
    response = client.post(
        "/auth/login",
        data={"username": admin_user.email, "password": admin_user.clean_password},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["access_token"]
    token = response.json()["access_token"]

    response = client.post(
        "/auth/refresh_token", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["access_token"]


def test_refresh_access_token_blacklisted(
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
    # Tenta refresh
    response = client.post(
        "/auth/refresh_token", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "Token is blacklisted"
