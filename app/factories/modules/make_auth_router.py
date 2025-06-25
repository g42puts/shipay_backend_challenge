from http import HTTPStatus

from fastapi import APIRouter

from app.factories.infra.auth.make_password_helper import make_password_helper
from app.modules.auth.auth import AuthRoute
from app.schemas import Token


def make_auth_router() -> APIRouter:
    auth_router = AuthRoute(make_password_helper())
    router = APIRouter(prefix="/auth", tags=["Auth"])

    router.post(
        "/login",
        status_code=HTTPStatus.OK,
        response_model=Token,
        description="Recive email as username and password to login and return JWT Token.",
    )(auth_router.login)

    router.post(
        "/refresh_token",
        response_model=Token,
        description="Request a new JWT Token if your token still valid, blacklist your old token.",
    )(auth_router.refresh_access_token)

    router.post(
        "/logout", description="Recive a request to logout, blacklist your old token."
    )(auth_router.logout)

    return router
