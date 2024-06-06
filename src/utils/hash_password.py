from abc import ABC, abstractmethod

import bcrypt


class HashPasswordABC(ABC):
    @staticmethod
    @abstractmethod
    def hash_password(password: str) -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def validate_password(password: str, hashed_password) -> bool:
        raise NotImplementedError


class Bcrypt(HashPasswordABC):
    @staticmethod
    def validate_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
