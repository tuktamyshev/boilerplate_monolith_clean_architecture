from pydantic import BaseModel, Field


class InfraPaginationDTO(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
