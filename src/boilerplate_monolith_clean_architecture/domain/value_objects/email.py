import re

from domain.exceptions.email import EmailMustBeLowercaseException, EmailTooLongException, InvalidEmailException
from domain.value_objects.base import BaseValueObject


class EmailValueObject(BaseValueObject, str):
    @classmethod
    def validate(cls, value: str) -> None:
        max_len = 320
        if len(value) > max_len:
            raise EmailTooLongException(len(value), max_len)

        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        if not re.fullmatch(regex, value):
            raise InvalidEmailException(value)
        if not value == value.lower():
            raise EmailMustBeLowercaseException(value)
