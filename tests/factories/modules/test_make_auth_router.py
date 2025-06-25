from fastapi import APIRouter

from app.factories.modules.make_auth_router import make_auth_router


def test_make_auth_router_returns_router():
    router = make_auth_router()
    assert isinstance(router, APIRouter)
