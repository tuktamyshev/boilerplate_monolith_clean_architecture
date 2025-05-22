from adapters.auth import JWTTokenService
from dishka import Provider, provide


class JWTAuthServiceProvider(Provider):
    auth_service = provide(JWTTokenService)
