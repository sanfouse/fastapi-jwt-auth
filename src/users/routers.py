from typing import List, Annotated

from fastapi import APIRouter, Depends

from src.services.base import ServiceABC
from .dependencies import user_service
from .models import User
from .schemas import UserSchema, UserCreate

router = APIRouter(prefix="/users", tags=["Users"])
type user_service_type = ServiceABC[User, UserSchema, UserCreate]


@router.get("/")
async def get_all(
    user: Annotated[user_service_type, Depends(user_service)]
) -> List[UserSchema]:
    return await user.all()  # pyright: ignore [reportReturnType]


@router.get("/{idx}")
async def get_one(
    idx: int, user: Annotated[user_service_type, Depends(user_service)]
) -> UserSchema:
    return await user.one(idx)  # pyright: ignore [reportReturnType]


@router.post("/create")
async def create_one(
    create_schema: UserCreate, user: Annotated[user_service_type, Depends(user_service)]
) -> UserSchema:
    return await user.create(
        {"email": create_schema.email}, create_schema
    )  # pyright: ignore [reportReturnType]
