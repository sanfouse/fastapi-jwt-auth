import datetime
from abc import ABC, abstractmethod
from typing import Type

from fastapi import HTTPException, status, Response, Request
from jwt.exceptions import InvalidTokenError

from src.auth.schemas import UserAuth, PayloadEncode, PayloadDecode
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
    COOKIE_ACCESS_TOKEN_KEY = "access_token"

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
        payload: dict = PayloadEncode(sub=user.id, email=schema.email).model_dump()
        access_token = self.jwt.encode(payload)
        response.set_cookie(self.COOKIE_ACCESS_TOKEN_KEY, access_token, httponly=True)
        return {"message": "Login successful"}

    async def authorized(self, request: Request) -> User | None:
        access_token = request.cookies.get(self.COOKIE_ACCESS_TOKEN_KEY)
        if not access_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        try:
            payload: PayloadDecode = PayloadDecode(**self.jwt.decode(access_token))
        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        if (
            not payload.exp
            or payload.exp < datetime.datetime.now(datetime.UTC).timestamp()
        ):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return await self.repository.get_one_by_id(payload.sub)

    async def logout(self, response: Response) -> dict:
        response.delete_cookie(self.COOKIE_ACCESS_TOKEN_KEY)
        return {"message": "Logout successful"}
