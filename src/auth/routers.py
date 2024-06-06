from typing import Annotated

from fastapi import APIRouter, Depends, Response, Request

from src.services.auth import AuthABC
from src.users.schemas import UserSchema
from .dependencies import auth_service
from .schemas import UserAuth

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def user_register(
    register_schema: UserAuth, auth: Annotated[AuthABC, Depends(auth_service)]
):
    return await auth.register(register_schema)


@router.post("/login")
async def user_login(
    response: Response,
    login_schema: UserAuth,
    auth: Annotated[AuthABC, Depends(auth_service)],
) -> dict:
    return await auth.authenticate(login_schema, response)


@router.get("/me")
async def user_me(
    request: Request, user: Annotated[AuthABC, Depends(auth_service)]
) -> UserSchema | None:
    return await user.authorized(request)  # pyright: ignore [reportReturnType]


@router.post("/logout")
async def user_logout(
    response: Response, auth: Annotated[AuthABC, Depends(auth_service)]
) -> dict:
    return await auth.logout(response)
