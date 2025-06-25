from abc import ABC, abstractmethod

from fastapi import HTTPException

from app.guards.check_admin_role import CheckAdminRole
from app.schemas import RolePublic, RoleSchema, RoleList
from app.shared.depends import SessionDep


class RoleRouterInterface(ABC):
    @abstractmethod
    def create_role(
        self, payload: RoleSchema, _: CheckAdminRole, session: SessionDep
    ) -> HTTPException | RolePublic:
        pass

    @abstractmethod
    def get_many_roles(
        self, session: SessionDep, _: CheckAdminRole
    ) -> HTTPException | RoleList:
        pass

    @abstractmethod
    def get_role_by_id(
        self, role_id: int, session: SessionDep, _: CheckAdminRole
    ) -> HTTPException | RolePublic:
        pass

    @abstractmethod
    def delete_role(
        self, role_id: int, session: SessionDep, _: CheckAdminRole
    ) -> HTTPException | dict[str, str]:
        pass
