from http import HTTPStatus
from typing import Annotated

from fastapi import HTTPException, Query
from sqlalchemy import select

from app.guards.check_admin_role import CheckAdminRole
from app.models import Role
from app.schemas import RoleSchema, UpdateRoleSchema
from app.shared.depends import SessionDep
from app.interfaces.modules.role_router import RoleRouterInterface


class RoleRouter(RoleRouterInterface):
    def create_role(self, payload: RoleSchema, session: SessionDep):
        role_exists = session.scalar(
            select(Role).where(Role.description == payload.description)
        )
        if role_exists:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Role already exists"
            )

        new_role = Role(description=payload.description)

        session.add(new_role)
        session.commit()
        session.refresh(new_role)

        return new_role

    def get_many_roles(
        self,
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
    ):
        roles = session.scalars(select(Role).offset(offset).limit(limit)).all()
        return {"roles": roles}

    def get_role_by_id(self, role_id: int, session: SessionDep):
        role_exists = session.scalar(select(Role).where(Role.id == role_id))
        if not role_exists:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Role not found"
            )

        return role_exists

    def update_role(self, role_id: int, session: SessionDep, payload: UpdateRoleSchema):
        role_exists = session.scalar(select(Role).where(Role.id == role_id))
        if not role_exists:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Role not found"
            )

        role_exists.description = payload.description
        session.commit()
        session.refresh(role_exists)

        return role_exists

    def delete_role(self, role_id: int, session: SessionDep):
        role_exists = session.scalar(select(Role).where(Role.id == role_id))
        if not role_exists:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Role not found"
            )

        session.delete(role_exists)
        session.commit()

        return {"message": "Role deleted"}
