from abc import ABC, abstractmethod
from typing import List, Type

from fastapi import HTTPException, status
from pydantic import BaseModel

from src.database import Base
from src.repositories.base import RepositoryABC


class ServiceABC[T: Base, S: BaseModel, C: BaseModel](ABC):
    @abstractmethod
    async def create(self, filter_by: dict, create_schema: C) -> T:
        raise NotImplementedError

    @abstractmethod
    async def one(self, idx: int) -> T:
        raise NotImplementedError

    @abstractmethod
    async def all(self) -> List[T]:
        raise NotImplementedError


class Service[T: Base, S: BaseModel, C: BaseModel](ServiceABC):
    def __init__(self, model: Type[T], repository: Type[RepositoryABC[T, C]]):
        self.model: Type[T] = model
        self.repository: RepositoryABC[T, C] = repository(model)

    async def create(self, filter_by: dict, create_schema: C) -> T:
        result: T | None = await self.repository.filter_by(filter_by)
        if not result:
            return await self.repository.create_one(create_schema)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{self.model.__name__} already exists",
        )

    async def one(self, idx: int) -> T:
        result: T | None = await self.repository.get_one_by_id(idx)
        if result:
            return result
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{self.model.__name__} not found",
        )

    async def all(self) -> list[T]:
        return await self.repository.get_all()
