from fastapi import APIRouter

from app.factories.modules.make_claim_router import make_claim_router


def test_make_claim_router_returns_router():
    router = make_claim_router()
    assert isinstance(router, APIRouter)
