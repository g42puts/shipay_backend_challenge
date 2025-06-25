from fastapi import APIRouter

from app.factories.modules.make_user_router import make_user_router


def test_make_user_router_returns_router():
    router = make_user_router()
    assert isinstance(router, APIRouter)
