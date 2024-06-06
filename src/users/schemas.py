from typing import Annotated

from annotated_types import MinLen
from pydantic import BaseModel, EmailStr


class UserGet(BaseModel):
    id: int


class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(3)]

    class Config:
        from_attributes = True


class UserSchema(UserGet, UserCreate):
    pass
