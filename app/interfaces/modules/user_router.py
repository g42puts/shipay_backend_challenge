from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import HTTPException, Query

from app.guards.check_admin_role import CheckAdminRole
from app.guards.get_current_user import CurrentUser
from app.schemas import UpdateUserSchema, UserPublic, UserSchema
from app.shared.depends import SessionDep


class UserRouterInterface(ABC):
    @abstractmethod
    def create_user(
        user: UserSchema, session: SessionDep
    ) -> HTTPException | UserPublic:
        pass

    @abstractmethod
    def find_many_users(
        session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
    ) -> HTTPException | UserPublic:
        pass

    @abstractmethod
    def update_user(
        user_id: int,
        user: UpdateUserSchema,
        session: SessionDep,
        current_user: CurrentUser,
    ) -> HTTPException | UserPublic:
        pass

    @abstractmethod
    def delete_user(
        user_id: int, session: SessionDep, current_user: CurrentUser
    ) -> HTTPException | dict[str, str]:
        pass

    @abstractmethod
    def update_user_claim(
        user_id: int, claim_id: int, session: SessionDep, _: CheckAdminRole
    ) -> HTTPException | dict[str, str]:
        pass

    @abstractmethod
    def delete_user_claim(
        user_id: int, claim_id: int, session: SessionDep, _: CheckAdminRole
    ) -> HTTPException | dict[str, str]:
        pass
