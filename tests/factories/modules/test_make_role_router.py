from fastapi import APIRouter

from app.factories.modules.make_role_router import make_role_router


def test_make_role_router_returns_router():
    router = make_role_router()
    assert isinstance(router, APIRouter)
