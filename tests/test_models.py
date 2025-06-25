from app.models import BlacklistedToken, Role, Claim, User, UserClaim
from datetime import datetime


def test_role_repr():
    role = Role(id=1, description="admin")
    assert repr(role) == "id: 1, description: admin"


def test_claim_repr():
    claim = Claim(id=2, description="can_edit", active=True)
    assert repr(claim) == "id: 2, description: can_edit"


def test_user_repr():
    user = User(
        id=3,
        name="Gilmar",
        email="gilmar@email.com",
        password="hash",
        role_id=1,
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=None,
    )
    assert repr(user) == "id: 3, name: Gilmar, email: gilmar@email.com"


def test_userclaim_repr():
    user_claim = UserClaim(user_id=4, claim_id=5)
    assert repr(user_claim) == "user_id: 4, claim_id: 5"


def test_blacklisted_token_repr():
    blacklisted_token = BlacklistedToken(
        id=1,
        jti="123",
        user_id=1,
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        expires_at=datetime(2024, 1, 4, 12, 0, 0),
    )
    assert repr(blacklisted_token) == "jti: 123, user_id: 1"
