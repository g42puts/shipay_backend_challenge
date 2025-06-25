from http import HTTPStatus

from fastapi import HTTPException

from app.guards.get_current_user import CurrentUser
from app.shared.depends import SessionDep
from app.models import Role, UserClaim, Claim


def require_claim(claim_name: str):
    def dependency(
        current_user: CurrentUser,
        session: SessionDep,
    ):
        role = session.get(Role, current_user.role_id)
        if role and role.description == "admin":
            return
        claim = session.query(Claim).filter_by(description=claim_name).first()
        if not claim:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail=f"Claim '{claim_name}' not found",
            )
        user_claim = (
            session.query(UserClaim)
            .filter_by(user_id=current_user.id, claim_id=claim.id)
            .first()
        )
        if not user_claim:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail=f"User does not have claim '{claim_name}'",
            )

    return dependency
