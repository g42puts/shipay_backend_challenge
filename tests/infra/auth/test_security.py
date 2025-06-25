from jwt import decode

from app.factories.infra.auth.make_password_helper import make_password_helper
from app.configs.configs import configs
from app.infra.auth.security import (
    create_access_token,
    validate_token,
)


def test_create_access_token_should_return_token():
    data = {"user_id": "1", "email": "teste@teste.com", "token_type": "bearer"}
    token = create_access_token(data)

    decoded = decode(token, configs.SECRET_KEY, algorithms=["HS256"])

    assert decoded["email"] == data["email"]
    assert decoded["exp"]


def test_validate_token_should_return_true():
    data = {"user_id": "1", "email": "teste@teste.com", "token_type": "bearer"}
    token = create_access_token(data)
    is_token_valid = validate_token(token)
    assert is_token_valid is True


def test_validate_token_should_return_false():
    is_token_valid = validate_token('invalid_token')
    assert is_token_valid is False


def test_get_password_hash_should_return_hashed_password():
    password = "test"
    hashed_password = make_password_helper().hash(password)
    assert hashed_password
    assert hashed_password != password


def test_verify_password_should_return_true():
    password = "test"
    hashed_password = make_password_helper().hash(password)
    assert make_password_helper().verify_password(password, hashed_password) is True