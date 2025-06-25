from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.infra.auth.password import PwdLibPasswordHelper
from app.interfaces.password_helper import PasswordHelperInterface


def make_password_helper() -> PasswordHelperInterface:
    password_hash = PasswordHash(hashers=[Argon2Hasher()])
    return PwdLibPasswordHelper(password_hash)
