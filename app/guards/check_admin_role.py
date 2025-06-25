from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException

from app.models import Role, User
from app.shared.depends import SessionDep
from .get_current_user import CurrentUser


def check_admin_role(current_user: CurrentUser, session: SessionDep):
    if current_user.role_id:
        role = session.get(Role, current_user.role_id)
        if role.description != "admin":
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
            )

    return current_user


CheckAdminRole = Annotated[User, Depends(check_admin_role)]
