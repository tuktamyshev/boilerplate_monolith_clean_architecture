from dataclasses import dataclass

from faststream.confluent.publisher.asyncapi import AsyncAPIDefaultPublisher

from application.interfaces.analyze_service import AnalyzePostServiceInterface
from domain.entities.post import PostEntity


@dataclass(frozen=True)
class AnalyzePostService(AnalyzePostServiceInterface):
    publisher: AsyncAPIDefaultPublisher

    async def analyze_post(self, post: PostEntity) -> None:
        # analyze service can be another server and you can send it messages by broker
        await self.publisher.publish(post, key=str(post.uuid).encode())
