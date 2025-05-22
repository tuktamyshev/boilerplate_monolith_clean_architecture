from dataclasses import dataclass

from config.app import AppConfig
from config.auth import JWTAuthConfig
from fastapi.security import APIKeyCookie
from starlette.responses import Response


@dataclass(frozen=True)
class CookieService:
    access_token_cookie_scheme: APIKeyCookie
    refresh_token_cookie_scheme: APIKeyCookie
    auth_config: JWTAuthConfig
    app_config: AppConfig

    def set_access_token_cookie(self, response: Response, access_token: str) -> None:
        response.set_cookie(
            self.access_token_cookie_scheme.model.name,
            value=access_token,
            max_age=self.auth_config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            samesite="none",
            secure=True,
            domain=self.app_config.WEB_DOMAIN,
        )

    def set_refresh_token_cookie(self, response: Response, refresh_token: str) -> None:
        response.set_cookie(
            self.refresh_token_cookie_scheme.model.name,
            value=refresh_token,
            max_age=self.auth_config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            httponly=True,
            samesite="none",
            secure=True,
            domain=self.app_config.WEB_DOMAIN,
        )

    def delete_cookies(self, response: Response) -> None:
        response.delete_cookie(
            self.access_token_cookie_scheme.model.name,
            httponly=True,
            samesite="none",
            secure=True,
            domain=self.app_config.WEB_DOMAIN,
        )
        response.delete_cookie(
            self.refresh_token_cookie_scheme.model.name,
            httponly=True,
            samesite="none",
            secure=True,
            domain=self.app_config.WEB_DOMAIN,
        )
