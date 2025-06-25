# from http import HTTPStatus

# import pytest
# from fastapi import HTTPException
# from unittest.mock import MagicMock
# from sqlalchemy.orm import Session

# from app.guards.require_claim import require_claim
# from app.models import Claim, UserClaim, User


# @pytest.fixture
# def session():
#     return MagicMock()


# def test_require_claim_success(user: User, session: Session):
#     claim = Claim(id=10, description="user:view", active=True)

#     def filter_by_side_effect(**kwargs):
#         mock = MagicMock()
#         if kwargs == {"description": "user:view", "active": True}:
#             mock.first.return_value = claim
#         elif kwargs == {"user_id": user.id, "claim_id": claim.id}:
#             mock.first.return_value = UserClaim(user_id=user.id, claim_id=claim.id)
#         else:
#             mock.first.return_value = None
#         return mock

#     session.query().filter_by.side_effect = filter_by_side_effect

#     guard = require_claim("user:view").dependency
#     result = guard(user, session)
#     assert result == user


# def test_require_claim_claim_not_found(user: User, session: Session):
#     def filter_by_side_effect(**kwargs):
#         mock = MagicMock()
#         mock.first.return_value = None
#         return mock

#     session.query().filter_by.side_effect = filter_by_side_effect

#     guard = require_claim("user:view").dependency
#     with pytest.raises(HTTPException) as exc_info:
#         guard(user, session)
#     assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
#     assert exc_info.value.detail == "Claim not found"


# def test_require_claim_user_without_claim(user: User, session: Session):
#     claim = Claim(id=10, description="user:view", active=True)

#     def filter_by_side_effect(*args, **kwargs):
#         if kwargs == {"description": "user:view", "active": True}:
#             mock = MagicMock()
#             mock.first.return_value = claim
#             return mock
#         elif kwargs == {"user_id": user.id, "claim_id": claim.id}:
#             mock = MagicMock()
#             mock.first.return_value = None
#             return mock
#         return MagicMock()

#     session.query().filter_by.side_effect = filter_by_side_effect

#     guard = require_claim("user:view").dependency
#     with pytest.raises(HTTPException) as exc_info:
#         guard(user, session)
#     assert exc_info.value.status_code == HTTPStatus.FORBIDDEN
#     assert exc_info.value.detail == "Not enough permissions"
