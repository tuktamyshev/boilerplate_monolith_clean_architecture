import pytest

from domain.exceptions.email import EmailMustBeLowercaseException, EmailTooLongException, InvalidEmailException
from domain.value_objects.email import EmailValueObject


def test_email_value_object_valid():
    email = EmailValueObject("test@example.com")
    assert str(email) == "test@example.com"


def test_email_value_object_invalid():
    with pytest.raises(InvalidEmailException):
        EmailValueObject("not-an-email")


def test_email_value_object_not_lowercase():
    with pytest.raises(EmailMustBeLowercaseException):
        EmailValueObject("Test@Example.com")


def test_email_value_object_too_long():
    long_email = "a" * 314 + "@ex.com"
    with pytest.raises(EmailTooLongException):
        EmailValueObject(long_email)
