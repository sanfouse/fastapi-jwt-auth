from pydantic import BaseModel, EmailStr

from src.users.schemas import UserCreate


class UserAuth(UserCreate):
    pass


class PayloadEncode(BaseModel):
    sub: int
    email: EmailStr


class PayloadDecode(PayloadEncode):
    exp: int
    iat: int
