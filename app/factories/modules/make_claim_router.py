from http import HTTPStatus
from fastapi import APIRouter, Depends

from app.guards.require_claim import require_claim
from app.modules.claims.claims import ClaimRouter
from app.schemas import ClaimPublic, ClaimSchema, ClaimList


def make_claim_router() -> APIRouter:
    claim_router = ClaimRouter()
    router = APIRouter(prefix="/claim", tags=["Claims", "Permissions"])

    router.post(
        "/",
        status_code=HTTPStatus.CREATED,
        response_model=ClaimSchema,
        description="Create a new claim",
        dependencies=[Depends(require_claim("claim:create"))],
    )(claim_router.create_claim)

    router.get(
        "/",
        status_code=HTTPStatus.OK,
        response_model=ClaimList,
        description="Return a list of claims",
        dependencies=[Depends(require_claim("claim:list"))],
    )(claim_router.find_many_claims)

    router.get(
        "/{claim_id}",
        status_code=HTTPStatus.OK,
        response_model=ClaimPublic,
        description="Recive a claim id and return the current role",
        dependencies=[Depends(require_claim("claim:view"))],
    )(claim_router.find_claim_by_id)

    router.delete(
        "/{claim_id}",
        status_code=HTTPStatus.OK,
        description="Delete a claim",
        dependencies=[Depends(require_claim("claim:delete"))],
    )(claim_router.delete_claim)

    return router
