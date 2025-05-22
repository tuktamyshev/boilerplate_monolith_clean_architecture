from pydantic import BaseModel


class PaginatedRequestDTO(BaseModel):
    limit: int
    offset: int


class PaginatedResponseDTO[IT](BaseModel):
    total: int
    items: list[IT]
