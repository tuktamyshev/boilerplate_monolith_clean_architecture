from adapters.orm.post import PostORM
from adapters.orm.user import UserORM
from sqladmin import ModelView


class BaseAdmin(ModelView):
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_default_sort = ("created_at", True)


class UserAdmin(BaseAdmin, model=UserORM):
    category = "Users"
    name_plural = "Users"

    column_list = [
        UserORM.uuid,
        UserORM.email,
        UserORM.is_active,
        UserORM.is_superuser,
    ]


class CallAdmin(BaseAdmin, model=PostORM):
    category = "Posts"
    name_plural = "Posts"

    column_searchable_list = [PostORM.user_uuid, PostORM.text]

    column_list = [
        PostORM.uuid,
        PostORM.user,
    ]
