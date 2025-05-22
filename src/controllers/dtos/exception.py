from pydantic import BaseModel


class ApplicationExceptionSchema(BaseModel):
    detail: str
