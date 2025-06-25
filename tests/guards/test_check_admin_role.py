import pytest
from http import HTTPStatus
from fastapi import HTTPException
from unittest.mock import MagicMock
from app.models import User, Role
from app.guards.check_admin_role import check_admin_role


def test_check_admin_role_admin():
    user = User(
        id=1,
        name="Admin",
        email="admin@email.com",
        password="hash",
        role_id=1,
        created_at=None,
    )
    session = MagicMock()
    session.get.return_value = Role(id=1, description="admin")
    result = check_admin_role(user, session)
    assert result == user


def test_check_admin_role_not_admin():
    user = User(
        id=2,
        name="User",
        email="user@email.com",
        password="hash",
        role_id=2,
        created_at=None,
    )
    session = MagicMock()
    session.get.return_value = Role(id=2, description="user")
    with pytest.raises(HTTPException) as exc_info:
        check_admin_role(user, session)
    assert exc_info.value.status_code == HTTPStatus.FORBIDDEN
    assert exc_info.value.detail == "Not enough permissions"
