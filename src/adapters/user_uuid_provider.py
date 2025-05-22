from dataclasses import dataclass
from uuid import UUID

import jwt
from jwt import InvalidTokenError
from pydantic import BaseModel

from application.exceptions.auth import WrongTokenException
from application.interfaces.user_uuid_provider import UserUUIDProviderInterface
from config.auth import JWTAuthConfig


class AuthByTokenDTO(BaseModel):
    token: str
    token_type: str


@dataclass(frozen=True)
class TokenUserUUIDProvider(UserUUIDProviderInterface):
    token_data: AuthByTokenDTO
    auth_config: JWTAuthConfig

    def get_current_user_uuid(self) -> UUID:
        payload = self._get_token_payload(self.token_data.token)
        self._validate_token_type(payload, self.token_data.token_type)

        try:
            return UUID(payload.get("sub"))
        except ValueError:
            raise WrongTokenException()

    @staticmethod
    def _validate_token_type(payload: dict, token_type: str) -> None:
        type_ = payload["type"]
        if type_ != token_type:
            raise WrongTokenException()

    def _get_token_payload(self, token: str) -> dict:
        try:
            return self._decode_jwt(
                token,
                self.auth_config.PUBLIC_KEY_PATH.read_text(),
                self.auth_config.ALGORITHM,
            )
        except InvalidTokenError:
            raise WrongTokenException()

    @staticmethod
    def _decode_jwt(token: str, public_key: str, algorithm: str) -> dict:
        return jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )


@dataclass(frozen=True)
class ContextUserUUIDProvider(UserUUIDProviderInterface):
    user_uuid: UUID

    def get_current_user_uuid(self) -> UUID:
        return self.user_uuid
