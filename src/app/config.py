from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent


class AuthJWT(BaseSettings):
    """JWT authentication configuration."""

    private_key_path: Path = BASE_DIR / "certs/jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs/jwt-public.pem"
    cert_path: Path = BASE_DIR / "certs/cert.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 10080


class DbSettings(BaseSettings):
    """Database connection configuration."""

    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = False


class RedisSettings(BaseSettings):
    """Redis server connection settings."""

    host: str = "localhost"
    port: int = 6379
    db: int = 0
    decode_responses: bool = True


class APIEndpoints(BaseSettings):
    """API endpoint URLs configuration."""

    base_url: str = "https://localhost:8000"
    financial_records: str = "/financial_records/"
    categories: str = "/categories/"
    auth_login: str = "/users/login/"
    auth_logout: str = "/users/logout/"
    auth_register: str = "/users/register/"
    generate_pdf: str = "/financial_records/generate-pdf/"

    @property
    def financial_records_url(self):
        return f"{self.base_url}{self.financial_records}"

    @property
    def categories_url(self):
        return f"{self.base_url}{self.categories}"

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
    """Root configuration container aggregating all service settings."""

    api_endpoints: APIEndpoints = APIEndpoints()
    auth_jwt: AuthJWT = AuthJWT()
    db: DbSettings = DbSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
