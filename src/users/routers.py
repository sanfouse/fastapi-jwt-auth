from typing import List, Annotated

from fastapi import APIRouter, Depends

from src.services.base import ServiceABC
from .dependencies import user_service
from .models import User
from .schemas import UserSchema, UserCreate

router = APIRouter(prefix="/users", tags=["Users"])
type user_service_type = ServiceABC[User, UserSchema, UserCreate]


@router.get("/", response_model=List[UserSchema])
async def get_all(
    user: Annotated[user_service_type, Depends(user_service)]
) -> List[User]:
    return await user.all()


@router.get("/{idx}", response_model=UserSchema)
async def get_one(
    idx: int, user: Annotated[user_service_type, Depends(user_service)]
) -> User:
    return await user.one(idx)


@router.post("/create", response_model=UserSchema)
async def create_one(
    create_schema: UserCreate, user: Annotated[user_service_type, Depends(user_service)]
) -> User:
    return await user.create(
        {"email": create_schema.email}, create_schema
    )
