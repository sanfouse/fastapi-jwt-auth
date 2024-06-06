from src.repositories.base import SQLAlchemyRepository
from src.services.auth import JWTAuthService

from src.utils.hash_password import Bcrypt


def auth_service() -> JWTAuthService:
    return JWTAuthService(SQLAlchemyRepository, Bcrypt)
