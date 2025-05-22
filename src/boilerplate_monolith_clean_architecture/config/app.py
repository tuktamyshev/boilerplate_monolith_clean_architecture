from pydantic import BaseModel


class AppConfig(BaseModel):
    MODE: str
    WEB_DOMAIN: str
    API_PORT: int
    ALLOW_ORIGINS: str
    FRONTEND_URL: str
