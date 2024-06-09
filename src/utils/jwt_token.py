import datetime
from datetime import timedelta
from typing import NamedTuple, Literal, Final

from jwt import encode, decode

from config import settings
from src.auth.schemas import Payload
from src.users.models import User


class ExpireIATDates(NamedTuple):
    exp: float
    iat: float


class JWTToken:
    __private_key: Final = settings.auth_jwt.private_key.read_text()
    __public_key: Final = settings.auth_jwt.public_key.read_text()
    __access_token_expire_minutes: Final = settings.auth_jwt.access_token_expire_minutes
    __refresh_token_expire_days: Final = settings.auth_jwt.refresh_token_expire_days
    algorithm: Final = settings.auth_jwt.algorithm

    @classmethod
    def create_jwt(cls, payload: Payload) -> str:
        payload_dict: dict = payload.model_dump()
        return encode(payload_dict, cls.__private_key, algorithm=cls.algorithm)

    @classmethod
    def decode(cls, jwt: str) -> dict:
        return decode(jwt, cls.__public_key, algorithms=[cls.algorithm])

    @classmethod
    def create_payload(
            cls,
            user: User,
            token_type: Literal["access", "refresh"],
            expire_timedelta: timedelta,
    ) -> Payload:
        iat = datetime.datetime.now(datetime.UTC)
        exp = iat + expire_timedelta
        return Payload(
            sub=user.id,
            exp=exp.timestamp(),
            iat=iat.timestamp(),
            token_type=token_type,
        )

    @classmethod
    def create_access_token(
            cls, user: User | None = None, old_payload: Payload | None = None
    ) -> str:
        if user:
            payload = cls.create_payload(
                user, "access", timedelta(minutes=cls.__access_token_expire_minutes)
            )
        elif old_payload:
            iat = datetime.datetime.now(datetime.UTC)
            exp = iat + timedelta(minutes=cls.__access_token_expire_minutes)
            old_payload.exp = exp.timestamp()
            old_payload.iat = iat.timestamp()
            payload = old_payload
        else:
            raise ValueError("Either user or payload must be provided")
        return cls.create_jwt(payload)

    @classmethod
    def create_refresh_token(cls, user: User) -> str:
        payload = cls.create_payload(
            user, "refresh", timedelta(days=cls.__refresh_token_expire_days)
        )
        return cls.create_jwt(payload)
