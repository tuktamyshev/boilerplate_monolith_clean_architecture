from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from application.interfaces.repositories.user import UserRepository
from application.interfaces.user_uuid_provider import UserUUIDProviderInterface
from controllers.dtos.user import ReadUserDTO
from domain.entities.user import UserEntity

router = APIRouter(
    prefix="/user",
    tags=["user"],
    route_class=DishkaRoute,
)


@router.get("/me", response_model=ReadUserDTO)
async def me(
    user_uuid_provider: FromDishka[UserUUIDProviderInterface],
    user_repository: FromDishka[UserRepository],
) -> UserEntity:
    user_uuid = user_uuid_provider.get_current_user_uuid()
    user = await user_repository.get_one(uuid=user_uuid)
    return user
