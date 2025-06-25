from abc import ABC, abstractmethod

from fastapi import HTTPException

from app.guards.check_admin_role import CheckAdminRole
from app.schemas import ClaimList, ClaimPublic, ClaimSchema
from app.shared.depends import SessionDep


class ClaimRouterInterface(ABC):
    @abstractmethod
    def create_claim(
        self, payload: ClaimSchema, session: SessionDep, admin_user: CheckAdminRole
    ) -> HTTPException | ClaimPublic:
        pass

    @abstractmethod
    def find_many_claims(self, session: SessionDep) -> HTTPException | ClaimList:
        pass

    @abstractmethod
    def find_claim_by_id(
        self, claim_id: int, session: SessionDep
    ) -> HTTPException | ClaimPublic:
        pass

    @abstractmethod
    def delete_claim(
        self, claim_id: int, session: SessionDep
    ) -> HTTPException | dict[str, str]:
        pass
