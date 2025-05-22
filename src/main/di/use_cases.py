from dishka import Provider, Scope, provide

from application.use_cases.admin.check_is_admin import CheckIsAdminUseCase
from application.use_cases.admin.delete_post import AdminDeletePostUseCase
from application.use_cases.admin.delete_user import AdminDeleteUserUseCase
from application.use_cases.message_from_user import MessageFromUserUseCase
from application.use_cases.notify_users import NotifyUsersUseCase
from application.use_cases.post.create import CreatePostUseCase
from application.use_cases.post.delete import DeletePostUseCase
from application.use_cases.post.get_list import GetPostListUseCase
from application.use_cases.post.update import UpdatePostUseCase
from application.use_cases.user.login import LoginUserUseCase
from application.use_cases.user.register import RegisterUserUseCase


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    register_user_use_case = provide(RegisterUserUseCase)
    login_user_use_case = provide(LoginUserUseCase)
    admin_delete_user_use_case = provide(AdminDeleteUserUseCase)
    admin_delete_post_use_case = provide(AdminDeletePostUseCase)
    create_post_use_case = provide(CreatePostUseCase)
    delete_post_use_case = provide(DeletePostUseCase)
    update_post_use_case = provide(UpdatePostUseCase)
    check_is_admin_use_case = provide(CheckIsAdminUseCase)
    message_from_user_use_case = provide(MessageFromUserUseCase)
    get_post_list_use_case = provide(GetPostListUseCase)
    notify_users_use_case = provide(NotifyUsersUseCase)
