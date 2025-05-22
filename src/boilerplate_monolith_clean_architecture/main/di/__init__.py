from adapters.constants import ApplicationMode
from config.base import Config
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider
from dishka.integrations.fastapi import setup_dishka as fastapi_dishka
from dishka.integrations.faststream import FastStreamProvider
from dishka.integrations.faststream import setup_dishka as faststream_dishka
from dishka.integrations.taskiq import TaskiqProvider
from dishka.integrations.taskiq import setup_dishka as taskiq_dishka
from fastapi import FastAPI
from faststream.broker.core.abc import ABCBroker
from main.di.adapters import AdaptersProvider, DevelopmentAdaptersProvider
from main.di.config import ConfigProvider
from main.di.domain_services import DomainServiceProvider
from main.di.use_cases import UseCasesProvider
from taskiq import AsyncBroker


def init_web_di(app: FastAPI) -> None:
    faststream_app = app.state.faststream_app
    config = app.state.config

    if config.app.MODE in [ApplicationMode.STAGING.value, ApplicationMode.PRODUCTION.value]:
        container = web_container_factory(broker=faststream_app.broker, config=config)
    else:
        container = develop_web_container_factory(broker=faststream_app.broker, config=config)

    fastapi_dishka(container, app)
    faststream_dishka(container, faststream_app, auto_inject=True, finalize_container=False)


def init_worker_di(broker: AsyncBroker, config: Config) -> None:
    if config.app.MODE in [ApplicationMode.STAGING.value, ApplicationMode.PRODUCTION.value]:
        container = worker_container_factory(config=config)
    else:
        container = develop_worker_container_factory(config=config)
    taskiq_dishka(container, broker)


def web_container_factory(broker: ABCBroker, config: Config) -> AsyncContainer:
    return make_async_container(
        ConfigProvider(),
        AdaptersProvider(),
        UseCasesProvider(),
        DomainServiceProvider(),
        FastStreamProvider(),
        FastapiProvider(),
        context={Config: config, ABCBroker: broker},
    )


def develop_web_container_factory(broker: ABCBroker, config: Config) -> AsyncContainer:
    return make_async_container(
        ConfigProvider(),
        DevelopmentAdaptersProvider(),
        UseCasesProvider(),
        DomainServiceProvider(),
        FastStreamProvider(),
        FastapiProvider(),
        context={Config: config, ABCBroker: broker},
    )


def worker_container_factory(config: Config) -> AsyncContainer:
    return make_async_container(
        ConfigProvider(),
        AdaptersProvider(),
        UseCasesProvider(),
        DomainServiceProvider(),
        FastStreamProvider(),
        FastapiProvider(),
        TaskiqProvider(),
        context={Config: config},
    )


def develop_worker_container_factory(config: Config) -> AsyncContainer:
    return make_async_container(
        ConfigProvider(),
        DevelopmentAdaptersProvider(),
        UseCasesProvider(),
        DomainServiceProvider(),
        FastStreamProvider(),
        FastapiProvider(),
        TaskiqProvider(),
        context={Config: config},
    )
