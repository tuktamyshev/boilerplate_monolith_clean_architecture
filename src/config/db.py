from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    NAME: str

    ECHO: bool
    ECHO_POOL: bool
    POOL_SIZE: int
    MAX_OVERFLOW: int

    @property
    def URI(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"
