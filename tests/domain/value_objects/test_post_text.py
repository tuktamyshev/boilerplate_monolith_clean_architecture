import pytest
from domain.exceptions.post import PostTextCannotBeEmptyException, PostTextTooLongException
from domain.value_objects.post_text import PostTextValueObject


def test_post_text_value_object_valid() -> None:
    text = PostTextValueObject("hello world")
    assert str(text) == "hello world"


def test_post_text_value_object_empty() -> None:
    with pytest.raises(PostTextCannotBeEmptyException):
        PostTextValueObject("")


def test_post_text_value_object_too_long() -> None:
    long_text = "a" * 1025
    with pytest.raises(PostTextTooLongException):
        PostTextValueObject(long_text)
