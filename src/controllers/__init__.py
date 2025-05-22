from fastapi import APIRouter
from starlette import status

from controllers.broker import router as broker_router
from controllers.dtos.exception import ApplicationExceptionSchema
from controllers.rest.admin import router as admin_router
from controllers.rest.auth import router as auth_router
from controllers.rest.healthcheck import router as healthcheck_router
from controllers.rest.post import router as post_router
from controllers.rest.user import router as user_router
from controllers.websocket.user import router as ws_user_router

__all__ = ["main_http_router", "broker_router"]

routers = [
    # rest
    auth_router,
    user_router,
    healthcheck_router,
    admin_router,
    post_router,
    # ws
    ws_user_router,
]

main_http_router = APIRouter(
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ApplicationExceptionSchema},
    },
)

for router in routers:
    main_http_router.include_router(router)
