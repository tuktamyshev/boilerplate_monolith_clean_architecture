from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from email.message import EmailMessage

import aiosmtplib
import jwt
from application.exceptions.auth import WrongTokenException
from application.interfaces.email import EmailServiceInterface
from application.interfaces.repositories.user import UserRepository
from application.interfaces.transaction_manager import TransactionManager
from config.app import AppConfig
from config.auth import JWTAuthConfig
from config.smtp import SMTPConfig
from domain.value_objects.email import EmailValueObject
from jwt import InvalidTokenError


@dataclass(frozen=True)
class EmailService(EmailServiceInterface):
    auth_config: JWTAuthConfig
    app_config: AppConfig
    smtp_config: SMTPConfig

    async def send_verification_to_email(self, email: EmailValueObject) -> None:
        token = self._create_email_token(email)

        message = EmailMessage()
        message["From"] = self.smtp_config.USERNAME
        message["To"] = email
        message["Subject"] = "Account Verification"
        message.set_content(
            f"Please follow this link to verify your account: {self.app_config.FRONTEND_URL}/verify_email?token={token}"
        )

        html_content = f"""
            <html>
                <body>
                    <p>Hello!</p>
                    <p>Thank you for registering.
                    Please confirm your email by clicking the link below:</p>
                    <p>
                        <a href="{self.app_config.FRONTEND_URL}/verify_email?token={token}">
                            Verify Email
                        </a>
                    </p>
                    <p>If you did not request this email, please ignore it.</p>
                </body>
            </html>
        """

        message.add_alternative(html_content, subtype="html")

        await aiosmtplib.send(
            message,
            hostname=self.smtp_config.HOSTNAME,
            port=self.smtp_config.PORT,
            username=self.smtp_config.USERNAME,
            password=self.smtp_config.PASSWORD,
            start_tls=True,
        )

    def _create_email_token(self, email: EmailValueObject) -> str:
        expire = datetime.now(UTC) + timedelta(hours=1)
        payload = {"sub": email, "exp": expire}
        # TODO the same key is used as for jwt, it is recommended to use a different key
        return jwt.encode(
            payload,
            self.auth_config.PRIVATE_KEY_PATH.read_text(),
            algorithm=self.auth_config.ALGORITHM,
        )

    def verify_email(self, token: str) -> str:
        try:
            payload = jwt.decode(
                token,
                self.auth_config.PUBLIC_KEY_PATH.read_text(),
                algorithms=[self.auth_config.ALGORITHM],
            )
            email = payload.get("sub")
            return email
        except InvalidTokenError:
            raise WrongTokenException()


@dataclass(frozen=True)
class DevelopEmailService(EmailService):
    user_repository: UserRepository
    transaction_manager: TransactionManager

    async def send_verification_to_email(self, email: EmailValueObject) -> None:
        user = await self.user_repository.get_one(email=email)
        async with self.transaction_manager:
            await self.user_repository.update(user.uuid, is_verified=True)
        print(f"{email=} automatically verified")  # noqa T201
