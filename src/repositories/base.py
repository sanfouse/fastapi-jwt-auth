from abc import ABC, abstractmethod
from typing import List, Type

from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.engine import Result

from src.database import async_session_maker, Base


class RepositoryABC[T: Base, C: BaseModel](ABC):
    @abstractmethod
    def __init__(self, model: Type[T]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def get_one_by_id(self, idx: int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def create_one(self, create_schema: C) -> T:
        raise NotImplementedError

    @abstractmethod
    async def filter_by(self, filter_by: dict) -> T | None:
        raise NotImplementedError


class SQLAlchemyRepository[T: Base, C: BaseModel](RepositoryABC[T, C]):
    def __init__(self, model: Type[T]) -> None:
        self.model = model

    async def get_all(self) -> List[T]:
        async with async_session_maker() as session:
            stmt = select(self.model).order_by(self.model.id)
            result: Result = await session.execute(stmt)
            return list(result.scalars().all())

    async def get_one_by_id(self, idx: int) -> T | None:
        async with async_session_maker() as session:
            return await session.get(self.model, idx)

    async def create_one(self, create_schema: C) -> T:
        async with async_session_maker() as session:
            stmt = (
                insert(self.model).values(**create_schema.dict()).returning(self.model)
            )
            result: Result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def filter_by(self, filter_by: dict) -> T | None:
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(**filter_by)
            result: Result = await session.execute(stmt)
            return result.scalars().first()
