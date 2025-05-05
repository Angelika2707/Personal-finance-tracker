from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent


class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs/jwt-private_key.pem"
    public_key_path: Path = BASE_DIR / "certs/jwt-public_key.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3


class DbSettings(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = True


class Settings(BaseSettings):
    api_url_records: str = "http://localhost:8000/financial_records/"
    api_url_categories: str = "http://localhost:8000/categories/"
    auth_jwt: AuthJWT = AuthJWT()
    db: DbSettings = DbSettings()


settings = Settings()
