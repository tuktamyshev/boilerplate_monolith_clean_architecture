from adapters.auth import JWTTokenService
from adapters.constants import JWTTokenType
from adapters.user_uuid_provider import AuthByTokenDTO, TokenUserUUIDProvider
from application.exceptions.auth import AuthenticationException
from application.interfaces.repositories.user import UserRepository
from application.use_cases.user.login import LoginUserUseCase, UserLoginDTO
from config.auth import JWTAuthConfig
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from sqladmin.authentication import AuthenticationBackend
from starlette.responses import Response


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        login_use_case = await request.scope["state"]["dishka_container"].get(LoginUserUseCase)
        token_service = await request.scope["state"]["dishka_container"].get(JWTTokenService)
        try:
            data = UserLoginDTO(email=email, password=password)
            user_uuid = await login_use_case(data)
            access_token = token_service.create_access_token(user_uuid)
        except Exception:
            return False

        request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Response | bool:
        token = request.session.get("token")

        if not token:
            return False

        auth_config = await request.scope["state"]["dishka_container"].get(JWTAuthConfig)
        user_uuid_provider = TokenUserUUIDProvider(
            token_data=AuthByTokenDTO(token=token, token_type=JWTTokenType.ACCESS.value), auth_config=auth_config
        )
        user_repository = await request.scope["state"]["dishka_container"].get(UserRepository)
        try:
            user_uuid = user_uuid_provider.get_current_user_uuid()
            user = await user_repository.get_one(uuid=user_uuid)
        except AuthenticationException:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        return user.is_superuser
