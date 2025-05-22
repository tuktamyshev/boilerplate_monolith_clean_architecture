from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from pydantic import BaseModel

from config.auth import JWTAuthConfig


class TokenInfoDTO(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str


@dataclass(frozen=True)
class JWTTokenService:
    auth_config: JWTAuthConfig

    def create_tokens(self, user_uuid: UUID) -> TokenInfoDTO:
        access_token = self.create_access_token(user_uuid)
        refresh_token = self.create_refresh_token(user_uuid)

        return TokenInfoDTO(  # nosec
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Cookie",
        )

    def create_access_token(self, user_uuid: UUID) -> str:
        jwt_payload = {
            "sub": str(user_uuid),
            "type": "access",
        }

        return self._encode_jwt(
            jwt_payload,
            self.auth_config.PRIVATE_KEY_PATH.read_text(),
            self.auth_config.ALGORITHM,
            self.auth_config.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

    def create_refresh_token(self, user_uuid: UUID) -> str:
        jwt_payload = {
            "sub": str(user_uuid),
            "type": "refresh",
        }

        return self._encode_jwt(
            jwt_payload,
            self.auth_config.PRIVATE_KEY_PATH.read_text(),
            self.auth_config.ALGORITHM,
            self.auth_config.ACCESS_TOKEN_EXPIRE_MINUTES,
            expire_timedelta=timedelta(days=self.auth_config.REFRESH_TOKEN_EXPIRE_DAYS),
        )

    @staticmethod
    def _encode_jwt(
        payload: dict,
        private_key: str,
        algorithm: str,
        expire_minutes: int,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(UTC)
        expire = now + expire_timedelta if expire_timedelta else now + timedelta(minutes=expire_minutes)

        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm,
        )
        return encoded
