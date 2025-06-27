from http import HTTPStatus
from datetime import datetime, timedelta
from jwt import decode

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from freezegun import freeze_time

from app.models import User, BlacklistedToken
from app.configs.configs import configs


def test_jwt_invalid_token(client: TestClient, admin_user: User):
    response = client.delete(
        f"/user/{admin_user.id}", headers={"Authorization": "Bearer token-invalido"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_token_expired_after_72hrs(client: TestClient, admin_user: User):
    with freeze_time("2022-01-01 00:00:00"):
        response = client.post(
            "/auth/login",
            data={"username": admin_user.email, "password": admin_user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2022-05-01 00:31:00"):
        response = client.put(
            f"/user/{admin_user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "username": "new_email@email.com",
                "password": "new_password",
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}


def test_blacklisted_token_is_rejected(
    client: TestClient, session: Session, admin_user: User, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    # Adiciona o token à blacklist manualmente
    payload = decode(token, configs.SECRET_KEY, algorithms=[configs.ALGORITHM])
    jti = payload["jti"]
    blacklisted = BlacklistedToken(
        jti=jti,
        user_id=admin_user.id,
        created_at=datetime.now(),
        expires_at=datetime.now()
        + timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_IN_MINUTES),
    )
    session.add(blacklisted)
    session.commit()
    # Tenta acessar rota protegida
    response = client.get("/user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "Token is blacklisted"
