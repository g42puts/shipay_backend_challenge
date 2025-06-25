from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode
from sqlalchemy import select

from app.configs.configs import configs
from app.shared.depends import SessionDep
from app.models import BlacklistedToken, User
from app.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)) -> User:
    """Recupera o usuário autenticado a partir do token JWT."""
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, configs.SECRET_KEY, algorithms=[configs.ALGORITHM])

        email: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        token_type: str = payload.get("token_type")
        jti: str = payload.get("jti")

        blacklisted = session.query(BlacklistedToken).filter_by(jti=jti).first()
        if blacklisted:
            raise HTTPException(status_code=401, detail="Token is blacklisted")

        if not email:
            raise credentials_exception

        token_data = TokenData(
            user_id=user_id, email=email, token_type=token_type, jti=jti
        )
    except (DecodeError, ExpiredSignatureError):
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == token_data.email))
    if not user:
        raise credentials_exception
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
