from dishka import Provider, provide
from faststream.confluent.publisher.asyncapi import AsyncAPIDefaultPublisher

from adapters.analyze_service import AnalyzePostService
from application.interfaces.analyze_service import AnalyzePostServiceInterface
from config.broker import BrokerConfig


class AnalyzeServiceProvider(Provider):
    @provide
    def analyze_service(
        self, publishers: dict[str, AsyncAPIDefaultPublisher], config: BrokerConfig
    ) -> AnalyzePostServiceInterface:
        publisher = publishers.get(config.analyze_post)
        return AnalyzePostService(publisher=publisher)
