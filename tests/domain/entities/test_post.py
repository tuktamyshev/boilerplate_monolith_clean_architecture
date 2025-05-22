from uuid import UUID, uuid4

from domain.entities.post import PostEntity
from domain.value_objects.post_text import PostTextValueObject


def test_post_create_success() -> None:
    user_uuid = uuid4()
    text = PostTextValueObject("hello world")

    post = PostEntity.create(user_uuid=user_uuid, text=text)

    assert isinstance(post.uuid, UUID)
    assert post.user_uuid == user_uuid
    assert post.text == text
    assert post.created_at is not None
