from pydantic import BaseModel


class WorkerConfig(BaseModel):
    BROKER_HOST: str
    BROKER_PORT: int
