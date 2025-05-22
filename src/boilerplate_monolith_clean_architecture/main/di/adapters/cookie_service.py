from dishka import Provider, provide
from fastapi.security import APIKeyCookie

from adapters.cookie_service import CookieService
from config.app import AppConfig
from config.auth import JWTAuthConfig


class CookieServiceProvider(Provider):
    @provide
    def cookie_service(self, app_config: AppConfig, auth_config: JWTAuthConfig) -> CookieService:
        return CookieService(
            access_token_cookie_scheme=APIKeyCookie(name="access_token"),
            refresh_token_cookie_scheme=APIKeyCookie(name="refresh_token"),
            app_config=app_config,
            auth_config=auth_config,
        )
