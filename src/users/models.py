from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class User(Base):
    email: Mapped[str] = mapped_column(String(40), unique=True)
    password: Mapped[str]
