from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from sqladmin.authentication import AuthenticationBackend
from starlette.responses import Response

from adapters.auth import JWTTokenService
from adapters.constants import JWTTokenType
from adapters.user_uuid_provider import AuthByTokenDTO
from application.exceptions.auth import AuthenticationException
from application.interfaces.user_uuid_provider import UserUUIDProviderInterface
from application.use_cases.user.login import LoginUserUseCase, UserLoginDTO


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

        user_uuid_provider = await request.scope["state"]["dishka_container"].get(UserUUIDProviderInterface)

        try:
            user = await user_uuid_provider(AuthByTokenDTO(token=token, token_type=JWTTokenType.ACCESS.value))
        except AuthenticationException:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        return user.is_superuser
