from http import HTTPStatus
from fastapi import APIRouter, Depends

from app.guards.require_claim import require_claim
from app.factories.infra.auth.make_password_helper import make_password_helper
from app.modules.users.users import UserRouter
from app.schemas import UserList, UserPublic


def make_user_router() -> APIRouter:
    user_router = UserRouter(make_password_helper())
    router = APIRouter(prefix="/user", tags=["User"])

    router.post(
        path="/",
        status_code=HTTPStatus.CREATED,
        response_model=UserPublic,
        description="Create a new User",
    )(user_router.create_user)

    router.get(
        path="/",
        status_code=HTTPStatus.OK,
        response_model=UserList,
        description="Return a list of Users",
        dependencies=[Depends(require_claim("user:list"))],
    )(user_router.find_many_users)

    router.get(
        path="/{user_id}",
        status_code=HTTPStatus.OK,
        response_model=UserPublic,
        description="Recive a user id and return the current user",
        dependencies=[Depends(require_claim("user:view"))],
    )(user_router.find_user_by_id)

    router.put(
        path="/{user_id}",
        status_code=HTTPStatus.OK,
        response_model=UserPublic,
        description="Update user data",
        dependencies=[Depends(require_claim("user:update"))],
    )(user_router.update_user)

    router.delete(
        "/{user_id}",
        status_code=HTTPStatus.OK,
        description="Delete a user",
        dependencies=[Depends(require_claim("user:delete"))],
    )(user_router.delete_user)

    router.post(
        "/claims/{user_id}/claim/{claim_id}",
        status_code=HTTPStatus.OK,
        description="Update user claim",
        dependencies=[Depends(require_claim("user:claim:add"))],
    )(user_router.update_user_claim)

    router.delete(
        "/claims/{user_id}/claim/{claim_id}",
        status_code=HTTPStatus.OK,
        description="Remove a user claim",
        dependencies=[Depends(require_claim("user:claim:remove"))],
    )(user_router.delete_user_claim)

    return router
