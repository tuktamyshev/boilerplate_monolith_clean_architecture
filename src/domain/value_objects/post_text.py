from domain.exceptions.post import PostTextCannotBeEmptyException, PostTextTooLongException
from domain.value_objects.base import BaseValueObject


class PostTextValueObject(BaseValueObject, str):
    @classmethod
    def validate(cls, value: str) -> None:
        if not value:
            raise PostTextCannotBeEmptyException()

        max_len = 1024
        if len(value) > max_len:
            raise PostTextTooLongException(len(value), max_len)
