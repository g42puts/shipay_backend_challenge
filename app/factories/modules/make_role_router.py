from http import HTTPStatus
from fastapi import APIRouter, Depends

from app.guards.require_claim import require_claim
from app.modules.roles.roles import RoleRouter
from app.schemas import RoleList, RolePublic


def make_role_router() -> APIRouter:
    role_router = RoleRouter()
    router = APIRouter(prefix="/role", tags=["Role"])

    router.post(
        path="/",
        status_code=HTTPStatus.CREATED,
        response_model=RolePublic,
        description="Create a new role",
        dependencies=[Depends(require_claim("role:create"))],
    )(role_router.create_role)

    router.get(
        path="/",
        status_code=HTTPStatus.OK,
        response_model=RoleList,
        description="Return a list of roles",
        dependencies=[Depends(require_claim("role:list"))],
    )(role_router.get_many_roles)

    router.get(
        path="/{role_id}",
        status_code=HTTPStatus.OK,
        response_model=RolePublic,
        description="Recive a role id and return the current role",
        dependencies=[Depends(require_claim("role:view"))],
    )(role_router.get_role_by_id)

    router.put(
        path="/{role_id}",
        status_code=HTTPStatus.OK,
        response_model=RolePublic,
        description="Update role",
        dependencies=[Depends(require_claim("role:update"))],
    )(role_router.update_role)

    router.delete(
        path="/{role_id}",
        status_code=HTTPStatus.OK,
        description="Recive a role id and delete the current role",
        dependencies=[Depends(require_claim("role:delete"))],
    )(role_router.delete_role)

    return router
