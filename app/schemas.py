from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None
    email: str | None = None
    token_type: str
    jti: str


class UserSchema(BaseModel):
    name: str
    email: str
    password: str | None = None
    role_id: int


class UserPublic(UserSchema):
    id: int
    created_at: datetime
    updated_at: datetime | None
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class UpdateUserSchema(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    role_id: int | None = None


class RoleSchema(BaseModel):
    description: str


class RolePublic(RoleSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RoleList(BaseModel):
    roles: list[RolePublic]


class UpdateRoleSchema(BaseModel):
    description: str | None = None


class ClaimSchema(BaseModel):
    description: str


class ClaimPublic(ClaimSchema):
    id: int
    active: bool
    model_config = ConfigDict(from_attributes=True)


class ClaimList(BaseModel):
    claims: list[ClaimPublic]


class UpdateClaimSchema(BaseModel):
    description: str | None = None
    active: bool | None = None
