from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class AuthJWT(BaseModel):
    private_key: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 1
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    PORT: int
    HOST: str

    auth_jwt: AuthJWT = AuthJWT()

    @property
    def database_url(self) -> str:
        url = "postgresql+asyncpg://{}:{}@{}:{}/{}"
        return url.format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.HOST,
            self.PORT,
            self.POSTGRES_DB,
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # pyright: ignore [reportCallIssue]
