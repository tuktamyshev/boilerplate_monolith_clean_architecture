from contextlib import AbstractAsyncContextManager, asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from faststream.confluent.fastapi import KafkaRouter

from config.base import Config
from config.logs import setup_logging
from main.admin_panel import init_admin
from main.api_gateway import init_routers
from main.di import init_web_di
from main.exception_handlers import faststream_exc_middleware, init_exceptions_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AbstractAsyncContextManager[None]:
    await init_admin(app)

    yield

    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    config = Config()
    app = FastAPI(
        default_response_class=ORJSONResponse,
        title="FastAPI Boilerplate",
        docs_url="/docs",
        description="FastAPI Clean Architecture Boilerplate",
        lifespan=lifespan,
    )
    broker = KafkaRouter(
        f"{config.broker.HOST}:{config.broker.PORT}",
        schema_url="/asyncapi",
        middlewares=[faststream_exc_middleware],
    )

    app.state.config = config
    app.state.faststream_app = broker

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.app.ALLOW_ORIGINS.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_web_di(app)
    init_routers(app)
    init_exceptions_handlers(app)
    setup_logging()

    return app


if __name__ == "__main__":
    uvicorn.run("web:create_app", port=8000, factory=True, reload=True)
