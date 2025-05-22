from pydantic import BaseModel


class SMTPConfig(BaseModel):
    HOSTNAME: str
    PORT: int
    USERNAME: str
    PASSWORD: str
