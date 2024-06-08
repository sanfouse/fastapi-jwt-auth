import datetime
from abc import ABC, abstractmethod
from typing import Type, Literal, Final

from fastapi import HTTPException, status, Response, Request
from jwt.exceptions import InvalidTokenError

from src.auth.schemas import UserAuth, Payload
from src.repositories.base import RepositoryABC
from src.users.models import User
from src.users.schemas import UserSchema
from src.utils.hash_password import HashPasswordABC
from src.utils.jwt_token import JWTToken
from .base import Service


class AuthValidatorABC(ABC):
    @staticmethod
    @abstractmethod
    async def validate_user_password(
            validator: Type[HashPasswordABC],
            schema: UserAuth,
            repository: RepositoryABC[User, UserAuth],
    ) -> tuple[bool, User | None]:
        raise NotImplementedError


class AuthValidator(AuthValidatorABC):
    @staticmethod
    async def validate_user_password(
            validator: Type[HashPasswordABC],
            schema: UserAuth,
            repository: RepositoryABC[User, UserAuth],
    ) -> tuple[bool, User | None]:
        user: User | None = await repository.filter_by({"email": schema.email})
        if not user:
            return False, None
        password: str = schema.password
        hash_password: str = user.password
        return validator.validate_password(password, hash_password), user


class AuthABC(ABC):
    @abstractmethod
    async def register(self, schema: UserAuth) -> None:
        raise NotImplementedError

    @abstractmethod
    async def authenticate(self, schema: UserAuth, response: Response) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def authorized(self, request: Request) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def logout(self, response: Response) -> dict:
        raise NotImplementedError


class JWTAuthService(AuthABC, Service[User, UserSchema, UserAuth]):
    COOKIE_ACCESS_TOKEN_KEY: Final = "access_token"
    COOKIE_REFRESH_TOKEN_KEY: Final = "refresh_token"

    def __init__(
            self,
            repository: Type[RepositoryABC[User, UserAuth]],
            validator: Type[HashPasswordABC],
    ):
        super().__init__(User, repository)
        self.validator: Type[HashPasswordABC] = validator
        self.jwt: Type[JWTToken] = JWTToken

    async def register(self, schema: UserAuth) -> None:
        schema.password = self.validator.hash_password(schema.password)
        await self.create({"email": schema.email}, schema)
        raise HTTPException(status_code=status.HTTP_201_CREATED)

    async def authenticate(self, schema: UserAuth, response: Response) -> dict:
        is_success, user = await AuthValidator.validate_user_password(
            self.validator, schema, self.repository
        )
        if not is_success or not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        access_token: str = self.jwt.create_access_token(user)
        refresh_token: str = self.jwt.create_refresh_token(user)

        response.set_cookie(self.COOKIE_ACCESS_TOKEN_KEY, access_token, httponly=True)
        response.set_cookie(self.COOKIE_REFRESH_TOKEN_KEY, refresh_token, httponly=True)
        return {"message": "Login successful"}

    async def authorized(self, request: Request) -> User | None:
        access_token: str | None = request.cookies.get(self.COOKIE_ACCESS_TOKEN_KEY)
        if not access_token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        payload = self._verify_token(access_token, "access")
        return await self.repository.get_one_by_id(payload.sub)

    async def logout(self, response: Response) -> dict:
        response.delete_cookie(self.COOKIE_ACCESS_TOKEN_KEY)
        response.delete_cookie(self.COOKIE_REFRESH_TOKEN_KEY)
        return {"message": "Logout successful"}

    async def refresh_token(self, request: Request, response: Response) -> dict | None:
        refresh_token: str | None = request.cookies.get(self.COOKIE_REFRESH_TOKEN_KEY)
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh token not provided",
            )
        payload = self._verify_token(refresh_token, "refresh")
        payload.token_type = "access"
        new_access_token: str = self.jwt.create_access_token(old_payload=payload)
        response.set_cookie(
            self.COOKIE_ACCESS_TOKEN_KEY, new_access_token, httponly=True
        )
        return {"message": "Access token refreshed"}

    def _verify_token(
            self, token: str, token_type: Literal["access", "refresh"]
    ) -> Payload:
        try:
            payload: Payload = Payload(**self.jwt.decode(token))
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )

        if (
                not payload.exp
                or payload.token_type != token_type
                or payload.exp < datetime.datetime.now(datetime.UTC).timestamp()
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token expired or invalid"
            )

        return payload
