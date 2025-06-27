import string
import secrets
from http import HTTPStatus
from typing import Annotated
from datetime import datetime
import re

from fastapi import HTTPException, Query
from sqlalchemy import select

from app.guards.check_admin_role import CheckAdminRole
from app.guards.get_current_user import CurrentUser
from app.shared.depends import SessionDep
from app.models import User, Role, Claim, UserClaim
from app.schemas import UserSchema, UpdateUserSchema
from app.interfaces.modules.user_router import UserRouterInterface
from app.interfaces.password_helper import PasswordHelperInterface


class UserRouter(UserRouterInterface):
    def __init__(self, password_helper: PasswordHelperInterface):
        self.password_helper = password_helper

    def _validate_email(self, email: str) -> bool:
        email_regex = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
        return bool(re.fullmatch(email_regex, email))

    def create_user(self, payload: UserSchema, session: SessionDep):
        if not self._validate_email(payload.email):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Invalid email format"
            )

        user_exists = session.query(User).where(User.email == payload.email).first()

        if user_exists:
            if user_exists.email == payload.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST, detail="Email already exists"
                )

        if not payload.password:
            alphabet = string.ascii_letters + string.digits
            password = "".join(secrets.choice(alphabet) for _ in range(16))
        else:
            password = payload.password

        new_user = User(
            name=payload.name,
            email=payload.email,
            password=self.password_helper.hash(password),
            role_id=payload.role_id,
            created_at=datetime.now(),
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        claims = session.query(Claim).filter(Claim.description.contains("user:")).all()
        admin_claim_ids = {
            uc.claim_id
            for uc in session.query(UserClaim).filter_by(user_id=new_user.id)
        }
        new_user_claims = [
            UserClaim(user_id=new_user.id, claim_id=claim.id)
            for claim in claims
            if claim.id not in admin_claim_ids
        ]
        if new_user_claims:
            session.bulk_save_objects(new_user_claims)
            session.commit()

        return new_user

    def find_many_users(
        self,
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
    ) -> list[User]:
        users = session.scalars(select(User).offset(offset).limit(limit)).all()
        return {"users": users}

    def find_user_by_id(
        self, user_id: int, session: SessionDep, current_user: CurrentUser
    ):
        if current_user.id != user_id:
            role = session.get(Role, current_user.role_id)
            if role.description != "admin":
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
                )

        user = session.scalar(select(User).where(User.id == user_id))

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="User not found"
            )
        return user

    def update_user(
        self,
        user_id: int,
        payload: UpdateUserSchema,
        session: SessionDep,
        current_user: CurrentUser,
    ):
        if current_user.id != user_id:
            role = session.get(Role, current_user.role_id)
            if role.description != "admin":
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
                )

        if payload.name is not None:
            current_user.name = payload.name
        if payload.email is not None:
            existing_user = session.scalar(
                select(User).where(
                    User.email == payload.email, User.id != current_user.id
                )
            )
            if existing_user:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT, detail="Email already exists"
                )
            current_user.email = payload.email
        if payload.password is not None:
            current_user.password = self.password_helper.hash(payload.password)

        session.commit()
        session.refresh(current_user)

        return current_user

    def delete_user(self, user_id: int, session: SessionDep, current_user: CurrentUser):
        user = session.scalar(select(User).where(User.id == user_id))
        if not user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="User not found"
            )

        if current_user.id != user_id:
            role = session.get(Role, current_user.role_id)
            if role.description != "admin":
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
                )

        session.delete(user)
        session.commit()

        return {"message": "User deleted"}

    def update_user_claim(
        self, user_id: int, claim_id: int, session: SessionDep, _: CheckAdminRole
    ):
        user = session.scalar(select(User).where(User.id == user_id))
        if not user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="User not found"
            )

        claim = session.scalar(select(Claim).where(Claim.id == claim_id))
        if not claim:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Claim not found"
            )

        user_claim = session.scalar(
            select(UserClaim).where(
                UserClaim.user_id == user_id, UserClaim.claim_id == claim_id
            )
        )
        if user_claim:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="User already have claim"
            )

        user_claim = UserClaim(user_id=user_id, claim_id=claim_id)
        session.add(user_claim)
        session.commit()
        return {"message": "Claim added to user."}

    def delete_user_claim(
        self, user_id: int, claim_id: int, session: SessionDep, _: CheckAdminRole
    ):
        user_claim = session.scalar(
            select(UserClaim).where(
                UserClaim.user_id == user_id, UserClaim.claim_id == claim_id
            )
        )
        if not user_claim:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="User Claim not found"
            )

        session.delete(user_claim)
        session.commit()

        return {"message": "User Claim deleted"}
