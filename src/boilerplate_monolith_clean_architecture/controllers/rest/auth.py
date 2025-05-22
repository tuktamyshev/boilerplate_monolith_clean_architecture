from typing import Annotated

from adapters.auth import JWTTokenService, TokenInfoDTO
from adapters.constants import JWTTokenType
from adapters.cookie_service import CookieService
from adapters.user_uuid_provider import AuthByTokenDTO, TokenUserUUIDProvider
from application.interfaces.user_uuid_provider import UserUUIDProviderInterface
from application.use_cases.user.login import LoginUserUseCase, UserLoginDTO
from application.use_cases.user.register import RegisterUserUseCase, UserCreateDTO
from application.use_cases.user.verify_email import VerifyEmailUseCase
from config.auth import JWTAuthConfig
from controllers.dtos.user import ReadUserDTO
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute, inject
from domain.entities.user import UserEntity
from fastapi import APIRouter, Depends, Form, Query
from pydantic import EmailStr
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    route_class=DishkaRoute,
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ReadUserDTO,
)
async def register(
    use_case: FromDishka[RegisterUserUseCase],
    email: EmailStr = Form(),
    password: str = Form(),
) -> UserEntity:
    user_data = UserCreateDTO(email=email, password=password)
    user = await use_case(user_data)
    return user


@router.post("/verify_email", response_model=ReadUserDTO)
async def verify_email(
    use_case: FromDishka[VerifyEmailUseCase],
    token: Annotated[str, Query()],
) -> UserEntity:
    user = await use_case(token)
    return user


@router.post("/login")
async def login(
    response: Response,
    login_use_case: FromDishka[LoginUserUseCase],
    cookie_service: FromDishka[CookieService],
    token_service: FromDishka[JWTTokenService],
    email: EmailStr = Form(),
    password: str = Form(),
) -> TokenInfoDTO:
    data = UserLoginDTO(email=email, password=password)
    user_uuid = await login_use_case(data)

    tokens_info = token_service.create_tokens(user_uuid)
    cookie_service.set_access_token_cookie(
        response,
        access_token=tokens_info.access_token,
    )
    cookie_service.set_refresh_token_cookie(
        response,
        refresh_token=tokens_info.refresh_token,
    )
    # TODO debug, better not return tokens_info
    return tokens_info


@router.post(
    "/logout",
)
async def logout(
    response: Response,
    uuid_provider: FromDishka[UserUUIDProviderInterface],
    cookie_service: FromDishka[CookieService],
) -> None:
    uuid_provider.get_current_user_uuid()
    cookie_service.delete_cookies(response)


@inject
async def get_user_uuid_provider_from_refresh_token(
    request: Request, cookie_service: FromDishka[CookieService], auth_config: FromDishka[JWTAuthConfig]
) -> UserUUIDProviderInterface:
    cookie_scheme = cookie_service.refresh_token_cookie_scheme
    token = await cookie_scheme(request)
    return TokenUserUUIDProvider(
        token_data=AuthByTokenDTO(token=token, token_type=JWTTokenType.REFRESH.value),
        auth_config=auth_config,
    )


@router.post("/refresh", response_model_exclude_none=True)
async def refresh(
    response: Response,
    token_service: FromDishka[JWTTokenService],
    cookie_service: FromDishka[CookieService],
    uuid_provider: UserUUIDProviderInterface = Depends(get_user_uuid_provider_from_refresh_token),
) -> TokenInfoDTO:
    user_uuid = uuid_provider.get_current_user_uuid()
    access_token = token_service.create_access_token(user_uuid)
    cookie_service.set_access_token_cookie(
        response,
        access_token=access_token,
    )
    return TokenInfoDTO(  # nosec
        access_token=access_token,
        token_type="Cookie",
    )
