from abc import ABC, abstractmethod

from fastapi import HTTPException

from app.guards.get_current_user import CurrentUser
from app.shared.depends import OAuth2Form, SessionDep


class AuthRouterInterface(ABC):
    @abstractmethod
    def login(self, form_data: OAuth2Form, session: SessionDep) -> HTTPException | dict:
        pass

    @abstractmethod
    def refresh_access_token(self, current_user: CurrentUser) -> dict[str, str]:
        pass
