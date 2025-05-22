from datetime import UTC, datetime
from uuid import uuid4

import bcrypt
import factory
from domain.entities.post import PostEntity
from domain.entities.user import UserEntity
from domain.value_objects.email import EmailValueObject
from domain.value_objects.post_text import PostTextValueObject
from faker import Faker

fake = Faker()


class PostEntityFactory(factory.Factory):
    class Meta:
        model = PostEntity

    uuid = factory.LazyFunction(uuid4)
    user_uuid = factory.LazyFunction(uuid4)
    text = factory.LazyAttribute(lambda _: PostTextValueObject("Sample post text"))
    created_at = factory.LazyFunction(lambda: datetime.now(UTC))


class UserEntityFactory(factory.Factory):
    class Meta:
        model = UserEntity

    uuid = factory.LazyFunction(uuid4)
    created_at = factory.LazyFunction(lambda: datetime.now(UTC))

    email = factory.LazyFunction(lambda: EmailValueObject(fake.email()))

    hashed_password = factory.Faker("text")

    is_active = True
    is_superuser = False
    is_verified = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):  # noqa
        pwd = extracted or "password"

        salt = bcrypt.gensalt()
        pwd_bytes = pwd.encode("utf-8")
        self.hashed_password = bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")
