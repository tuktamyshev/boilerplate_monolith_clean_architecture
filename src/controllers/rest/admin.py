from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query

from application.use_cases.admin.delete_post import AdminDeletePostUseCase
from application.use_cases.admin.delete_user import AdminDeleteUserUseCase
from domain.value_objects.email import EmailValueObject

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    route_class=DishkaRoute,
)


@router.delete("/delete_user")
async def delete_user(
    user_email: Annotated[EmailValueObject, Query()],
    use_case: FromDishka[AdminDeleteUserUseCase],
) -> None:
    user_email = user_email.lower()
    await use_case(data=user_email)


@router.delete("/delete_post")
async def delete_post(post_uuid: Annotated[UUID, Query()], use_case: FromDishka[AdminDeletePostUseCase]) -> None:
    await use_case(data=post_uuid)
