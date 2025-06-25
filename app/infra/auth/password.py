from pwdlib import PasswordHash

from app.interfaces.password_helper import PasswordHelperInterface


class PwdLibPasswordHelper(PasswordHelperInterface):
    def __init__(self, pwd_context=None):
        self.pwd_context = pwd_context or PasswordHash().recommended()

    def hash(self, password: str) -> str:
        return self.pwd_context.hash(password=password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password=plain_password, hash=hashed_password)
