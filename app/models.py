from datetime import datetime

from sqlalchemy import (
    Column,
    PrimaryKeyConstraint,
    String,
    Integer,
    BigInteger,
    DateTime,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)

from app.database import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)
    __table_args__ = (PrimaryKeyConstraint("id", name="roles_pk"),)

    def __repr__(self):
        return f"id: {self.id}, description: {self.description}"


class Claim(Base):
    __tablename__ = "claims"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    __table_args__ = (PrimaryKeyConstraint("id", name="claims_pk"),)

    def __repr__(self):
        return f"id: {self.id}, description: {self.description}"


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", name="users_fk"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)
    __table_args__ = (PrimaryKeyConstraint("id", name="users_pk"),)

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, email: {self.email}"


class UserClaim(Base):
    __tablename__ = "user_claims"
    user_id = Column(
        BigInteger, ForeignKey("users.id", name="user_claims_fk"), primary_key=True
    )
    claim_id = Column(
        BigInteger, ForeignKey("claims.id", name="user_claims_fk_1"), primary_key=True
    )
    __table_args__ = (UniqueConstraint("user_id", "claim_id", name="user_claims_un"),)

    def __repr__(self):
        return f"user_id: {self.user_id}, claim_id: {self.claim_id}"


class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    jti = Column(String(255), nullable=False, unique=True)  # JWT ID
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    expires_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"jti: {self.jti}, user_id: {self.user_id}"
