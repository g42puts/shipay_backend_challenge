import uuid
import pytest
from jwt import encode
from http import HTTPStatus

from fastapi import HTTPException
from unittest.mock import MagicMock

from app.models import User
from app.configs.configs import configs
from app.guards.get_current_user import get_current_user


def make_token(payload):
    return encode(payload, configs.SECRET_KEY, algorithm=configs.ALGORITHM)


def test_get_current_user_success():
    user = User(
        id=1,
        name="Test",
        email="test@email.com",
        password="hash",
        role_id=1,
        created_at=None,
    )
    session = MagicMock()
    session.scalar.return_value = user
    session.query().filter_by().first.return_value = None

    payload = {
        "sub": user.email,
        "user_id": str(user.id),
        "token_type": "bearer",
        "jti": str(uuid.uuid4()),
    }
    token = encode(payload, configs.SECRET_KEY, algorithm=configs.ALGORITHM)
    result = get_current_user(session, token)
    assert result == user


def test_get_current_user_invalid_token():
    session = MagicMock()
    session.scalar.return_value = None
    invalid_token = "invalid.token.value"

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(session, invalid_token)
    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"


def test_get_current_user_raises_if_email_missing():
    payload = {"user_id": "1", "token_type": "bearer"}
    token = make_token(payload)
    session = MagicMock()
    session.query().filter_by().first.return_value = (
        None  # Garante que não está na blacklist
    )
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(session, token)
    assert exc_info.value.detail == "Could not validate credentials"


def test_get_current_user_raises_if_user_not_found():
    payload = {
        "sub": "naoexiste@email.com",
        "user_id": "1",
        "token_type": "bearer",
        "jti": str(uuid.uuid4()),
    }
    token = make_token(payload)
    session = MagicMock()
    session.scalar.return_value = None
    session.query().filter_by().first.return_value = (
        None  # Garante que não está na blacklist
    )
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(session, token)
    assert exc_info.value.detail == "Could not validate credentials"
