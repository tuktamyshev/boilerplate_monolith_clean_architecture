from pathlib import Path

from pydantic import BaseModel

from config import BASE_DIR


class JWTAuthConfig(BaseModel):
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    ADMIN_PANEL_SECRET_KEY: str
    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "jwt_private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "jwt_public.pem"
    ALGORITHM: str = "RS256"
