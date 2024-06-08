from pydantic import BaseModel

from typing import Literal

from pydantic import BaseModel

from src.users.schemas import UserCreate


class UserAuth(UserCreate):
    pass


class Payload(BaseModel):
    sub: int
    exp: float
    iat: float
    token_type: Literal["access", "refresh"]
