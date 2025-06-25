import uuid
from http import HTTPStatus
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from jwt import decode
from sqlalchemy import select

from app.configs.configs import configs
from app.interfaces.modules.auth_router import AuthRouterInterface
from app.interfaces.password_helper import PasswordHelperInterface
from app.infra.auth.security import create_access_token
from app.guards.get_current_user import CurrentUser, oauth2_scheme
from app.shared.depends import SessionDep, OAuth2Form
from app.models import BlacklistedToken, User


class AuthRoute(AuthRouterInterface):
    def __init__(self, password_helper: PasswordHelperInterface):
        self.password_helper = password_helper

    def login(self, form_data: OAuth2Form, session: SessionDep):
        user = session.scalar(select(User).where(User.email == form_data.username))

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect email or password"
            )

        if not self.password_helper.verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect password"
            )

        access_token = create_access_token(
            data={
                "sub": user.email,
                "user_id": str(user.id),
                "token_type": "bearer",
                "jti": str(uuid.uuid4()),
            }
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def refresh_access_token(
        self,
        current_user: CurrentUser,
        session: SessionDep,
        token: str = Depends(oauth2_scheme),
    ):
        payload = decode(token, configs.SECRET_KEY, algorithms=[configs.ALGORITHM])

        jti: str = payload.get("jti")
        blacklisted = session.query(BlacklistedToken).filter_by(jti=jti).first()
        if blacklisted:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Token is blacklisted"
            )

        new_blacklisted = BlacklistedToken(
            jti=jti,
            user_id=current_user.id,
            created_at=datetime.now(),
            expires_at=datetime.now()
            + timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_IN_MINUTES),
        )
        session.add(new_blacklisted)
        session.commit()

        new_access_token = create_access_token(
            data={
                "sub": current_user.email,
                "user_id": str(current_user.id),
                "token_type": "bearer",
                "jti": str(uuid.uuid4()),
            }
        )
        return {"access_token": new_access_token, "token_type": "bearer"}

    def logout(
        self,
        current_user: CurrentUser,
        session: SessionDep,
        token: str = Depends(oauth2_scheme),
    ):
        payload = decode(token, configs.SECRET_KEY, algorithms=[configs.ALGORITHM])

        jti: str = payload.get("jti")
        blacklisted = session.query(BlacklistedToken).filter_by(jti=jti).first()
        if blacklisted:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Token is blacklisted"
            )

        new_blacklisted = BlacklistedToken(
            jti=jti,
            user_id=current_user.id,
            created_at=datetime.now(),
            expires_at=datetime.now()
            + timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_IN_MINUTES),
        )
        session.add(new_blacklisted)
        session.commit()

        return {"message": "Logout successfully"}
