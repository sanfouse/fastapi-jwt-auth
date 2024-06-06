from src.repositories.base import SQLAlchemyRepository
from src.services.base import Service

from .models import User
from .schemas import UserCreate, UserSchema


def user_service() -> Service[User, UserSchema, UserCreate]:
    return Service[User, UserSchema, UserCreate](User, SQLAlchemyRepository)
