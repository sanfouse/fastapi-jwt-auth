import datetime
from datetime import timedelta

from jwt import encode, decode

from config import settings


class JWTToken:
    __private_key: str = settings.auth_jwt.private_key.read_text()
    __public_key: str = settings.auth_jwt.public_key.read_text()
    __expire_minutes: int = settings.auth_jwt.access_token_expire_minutes
    algorithm: str = settings.auth_jwt.algorithm

    @classmethod
    def encode(cls, payload: dict, expire_timedelta: timedelta | None = None) -> str:
        payload = payload.copy()
        now = datetime.datetime.now(datetime.UTC)
        if expire_timedelta:
            exp = now + expire_timedelta
        else:
            exp = now + timedelta(minutes=cls.__expire_minutes)
        payload.update(exp=exp, iat=now)
        encoded = encode(payload, cls.__private_key, algorithm=cls.algorithm)
        return encoded

    @classmethod
    def decode(cls, jwt: str):
        decoded = decode(jwt, cls.__public_key, algorithms=[cls.algorithm])
        return decoded
