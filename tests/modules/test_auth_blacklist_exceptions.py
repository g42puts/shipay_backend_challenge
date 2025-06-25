from http import HTTPStatus
import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from fastapi import HTTPException

from app.configs.configs import configs
from app.modules.auth.auth import AuthRoute
from app.models import BlacklistedToken, User
from app.infra.auth.security import create_access_token


class DummyPasswordHelper:
    def verify_password(self, plain, hashed):
        return True

    def hash(self, password):
        return password


def make_user():
    return User(
        id=1,
        name="Test",
        email="test@email.com",
        password="hash",
        role_id=1,
        created_at=datetime.now(),
    )


def make_token(user):
    return create_access_token(
        {
            "sub": user.email,
            "user_id": str(user.id),
            "token_type": "bearer",
            "jti": "jti-test",
        }
    )


def test_refresh_access_token_blacklisted():
    user = make_user()
    session = MagicMock()
    # Simula token na blacklist
    session.query().filter_by().first.return_value = BlacklistedToken(
        jti="jti-test",
        user_id=user.id,
        created_at=datetime.now(),
        expires_at=datetime.now()
        + timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_IN_MINUTES),
    )
    auth = AuthRoute(DummyPasswordHelper())
    token = make_token(user)
    with pytest.raises(HTTPException) as exc_info:
        auth.refresh_access_token(user, session, token)
    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exc_info.value.detail == "Token is blacklisted"


def test_logout_blacklisted():
    user = make_user()
    session = MagicMock()
    # Simula token na blacklist
    session.query().filter_by().first.return_value = BlacklistedToken(
        jti="jti-test",
        user_id=user.id,
        created_at=datetime.now(),
        expires_at=datetime.now()
        + timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_IN_MINUTES),
    )
    auth = AuthRoute(DummyPasswordHelper())
    token = make_token(user)
    with pytest.raises(HTTPException) as exc_info:
        auth.logout(user, session, token)
    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exc_info.value.detail == "Token is blacklisted"
