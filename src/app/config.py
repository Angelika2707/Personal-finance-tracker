from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent


class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs/jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs/jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 10080


class DbSettings(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = True


class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    decode_responses: bool = True


class APIEndpoints(BaseSettings):
    base_url: str = "https://localhost:8000"
    financial_records: str = "/financial_records/"
    auth_login: str = "/users/login/"
    auth_logout: str = "/users/logout/"
    auth_register: str = "/users/register/"

    @property
    def financial_records_url(self):
        return f"{self.base_url}{self.financial_records}"

    @property
    def login_url(self):
        return f"{self.base_url}{self.auth_login}"

    @property
    def logout_url(self):
        return f"{self.base_url}{self.auth_logout}"

    @property
    def register_url(self):
        return f"{self.base_url}{self.auth_register}"

    @property
    def create_financial_records_url(self):
        return f"{self.base_url}{self.auth_register}"


class Settings(BaseSettings):
    api_endpoints: APIEndpoints = APIEndpoints()
    auth_jwt: AuthJWT = AuthJWT()
    db: DbSettings = DbSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
