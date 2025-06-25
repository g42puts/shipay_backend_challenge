from http import HTTPStatus
from typing import Annotated

from fastapi import HTTPException, Query
from sqlalchemy import select

from app.guards.check_admin_role import CheckAdminRole
from app.models import Claim
from app.schemas import ClaimSchema
from app.shared.depends import SessionDep
from app.interfaces.modules.claim_router import ClaimRouterInterface


class ClaimRouter(ClaimRouterInterface):
    def create_claim(
        self, payload: ClaimSchema, session: SessionDep, _: CheckAdminRole
    ):
        claim_exists = session.scalar(
            select(Claim).where(Claim.description == payload.description)
        )
        if claim_exists:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Claim already exists"
            )

        new_claim = Claim(description=payload.description)

        session.add(new_claim)
        session.commit()
        session.refresh(new_claim)

        return new_claim

    def find_many_claims(
        self,
        session: SessionDep,
        _: CheckAdminRole,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
    ):
        claims = session.scalars(select(Claim).offset(offset).limit(limit)).all()
        return {"claims": claims}

    def find_claim_by_id(self, claim_id: int, session: SessionDep, _: CheckAdminRole):
        claim_exists = session.scalar(select(Claim).where(Claim.id == claim_id))
        if not claim_exists:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Claim not found"
            )

        return claim_exists

    def delete_claim(self, claim_id: int, session: SessionDep, _: CheckAdminRole):
        claim_exists = session.scalar(select(Claim).where(Claim.id == claim_id))
        if not claim_exists:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Claim not found"
            )

        session.delete(claim_exists)
        session.commit()

        return {"message": "Claim deleted"}
