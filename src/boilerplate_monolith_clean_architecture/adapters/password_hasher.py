from dataclasses import dataclass

import bcrypt
from application.interfaces.password_hasher import PasswordHasherInterface


@dataclass(frozen=True)
class PasswordHasherService(PasswordHasherInterface):
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode("utf-8")
        return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

    def validate_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
