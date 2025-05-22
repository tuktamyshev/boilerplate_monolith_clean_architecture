from dishka import Provider, Scope, provide
from fastapi import WebSocketException
from starlette import status
from starlette.requests import Request
from starlette.websockets import WebSocket

from adapters.constants import JWTTokenType
from adapters.cookie_service import CookieService
from adapters.user_uuid_provider import AuthByTokenDTO, TokenUserUUIDProvider
from application.interfaces.user_uuid_provider import UserUUIDProviderInterface
from config.auth import JWTAuthConfig


class TokenUserUUIDProviderProvider(Provider):  # ;D ProviderProvider
    @provide(scope=Scope.REQUEST)
    async def user_uuid_provider(
        self,
        cookie_service: CookieService,
        auth_config: JWTAuthConfig,
        request: Request,
    ) -> UserUUIDProviderInterface:
        cookie_scheme = cookie_service.access_token_cookie_scheme
        token = await cookie_scheme(request)

        return TokenUserUUIDProvider(
            token_data=AuthByTokenDTO(token=token, token_type=JWTTokenType.ACCESS.value),
            auth_config=auth_config,
        )

    @provide(scope=Scope.SESSION)
    async def ws_user_uuid_provider(
        self,
        cookie_service: CookieService,
        auth_config: JWTAuthConfig,
        websocket: WebSocket,
    ) -> UserUUIDProviderInterface:
        cookie_scheme = cookie_service.access_token_cookie_scheme
        token = websocket.cookies.get(cookie_scheme.model.name)
        if token is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

        return TokenUserUUIDProvider(
            token_data=AuthByTokenDTO(token=token, token_type=JWTTokenType.ACCESS.value),
            auth_config=auth_config,
        )
