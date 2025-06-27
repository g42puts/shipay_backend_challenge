from http import HTTPStatus
from datetime import datetime, timedelta
from jwt import decode

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from freezegun import freeze_time

from app.models import User, BlacklistedToken
from app.configs.configs import configs


def make_login(client: TestClient, email: str, password: str) -> str:
    response = client.post(
        "/auth/login", data={"username": email, "password": password}
    )
    assert response.status_code == HTTPStatus.OK
    return response.json()["access_token"]


def test_jwt_invalid_token(client: TestClient, admin_user: User):
    response = client.delete(
        f"/user/{admin_user.id}", headers={"Authorization": "Bearer token-invalido"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_get_token(client: TestClient, admin_user: User):
    response = client.post(
        "/auth/login",
        data={"username": admin_user.email, "password": admin_user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token


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


def test_token_inexistent_user(client: TestClient):
    response = client.post(
        "/auth/login",
        data={"username": "random_email@email.com", "password": "random_password"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Incorrect email or password"


def test_get_token_with_wrong_password_should_return_error(
    client: TestClient, admin_user: User
):
    response = client.post(
        "/auth/login",
        data={"username": admin_user.email, "password": "wrong_password"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Incorrect password"


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


def test_logout_adds_token_to_blacklist(
    client: TestClient, session: Session, admin_user: User
):
    token = make_login(client, admin_user.email, admin_user.clean_password)
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


def test_blacklisted_token_is_rejected(
    client: TestClient, session: Session, admin_user: User
):
    token = make_login(client, admin_user.email, admin_user.clean_password)
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


def test_refresh_access_token_blacklisted(
    client: TestClient, session: Session, admin_user: User
):
    token = make_login(client, admin_user.email, admin_user.clean_password)
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


def test_logout_blacklisted(client: TestClient, session: Session, admin_user: User):
    token = make_login(client, admin_user.email, admin_user.clean_password)
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
