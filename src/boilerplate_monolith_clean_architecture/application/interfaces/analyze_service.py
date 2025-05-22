from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.post import PostEntity


@dataclass(frozen=True)
class AnalyzePostServiceInterface(ABC):
    @abstractmethod
    async def analyze_post(self, post: PostEntity) -> None: ...
