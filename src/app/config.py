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


class Settings(BaseSettings):
    api_url_records: str = "http://localhost:8000/financial_records/"
    auth_jwt: AuthJWT = AuthJWT()
    db: DbSettings = DbSettings()


settings = Settings()
