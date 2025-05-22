from config.broker import BrokerConfig
from dishka import Provider, Scope, from_context, provide
from faststream.broker.core.abc import ABCBroker
from faststream.confluent.publisher.asyncapi import AsyncAPIDefaultPublisher


class KafkaBrokerProvider(Provider):
    scope = Scope.APP

    broker = from_context(ABCBroker)

    @provide
    def provide_publishers(self, broker: ABCBroker, config: BrokerConfig) -> dict[str, AsyncAPIDefaultPublisher]:
        # create your publishers here
        return {
            config.analyze_post: broker.publisher(config.analyze_post),
        }
