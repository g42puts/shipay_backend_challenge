from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import (
    DecodeError,
    ExpiredSignatureError,
    decode,
    encode,
)
from app.configs.configs import configs


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=configs.ACCESS_TOKEN_EXPIRE_IN_MINUTES
    )
    to_encode.update({"exp": expire})
    encode_jwt = encode(to_encode, configs.SECRET_KEY, algorithm=configs.ALGORITHM)
    return encode_jwt


def validate_token(token: str) -> bool:
    try:
        decode(token, configs.SECRET_KEY, algorithms=[configs.ALGORITHM])
        return True
    except (DecodeError, ExpiredSignatureError):
        return False