from dishka import Provider, provide

from adapters.auth import JWTTokenService


class JWTAuthServiceProvider(Provider):
    auth_service = provide(JWTTokenService)
