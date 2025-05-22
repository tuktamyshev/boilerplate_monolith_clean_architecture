from controllers import broker_router, main_http_router
from fastapi import FastAPI


def init_routers(app: FastAPI) -> None:
    app.include_router(main_http_router)

    # need to separate register broker app
    faststream_app = app.state.faststream_app
    app.include_router(faststream_app)

    # and include router to broker
    faststream_app.include_router(broker_router)
