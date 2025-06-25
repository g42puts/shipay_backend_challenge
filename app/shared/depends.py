from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.infra.db.db import get_session

SessionDep = Annotated[Session, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
