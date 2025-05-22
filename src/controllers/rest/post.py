from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query
from starlette import status

from application.interfaces.repositories.post import GetPostListDTO, PostListDTO, PostRepository
from application.use_cases.post.create import CreatePostDTO, CreatePostUseCase
from application.use_cases.post.delete import DeletePostUseCase
from application.use_cases.post.get_list import GetPostListUseCase
from application.use_cases.post.update import UpdatePostDTO, UpdatePostUseCase
from controllers.dtos.post import PostFilter, ReadPostDTO
from domain.entities.post import PostEntity

router = APIRouter(
    prefix="/post",
    tags=["post"],
    route_class=DishkaRoute,
)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=ReadPostDTO,
)
async def create(
    data: CreatePostDTO,
    use_case: FromDishka[CreatePostUseCase],
) -> PostEntity:
    post = await use_case(data)
    return post


@router.get(
    "/read",
    response_model=ReadPostDTO,
)
async def read(
    uuid: Annotated[UUID, Query()],
    post_repository: FromDishka[PostRepository],
) -> PostEntity:
    post = await post_repository.get_one(uuid=uuid)
    return post


@router.get(
    "/update",
    response_model=ReadPostDTO,
)
async def update(
    data: UpdatePostDTO,
    use_case: FromDishka[UpdatePostUseCase],
) -> PostEntity:
    post = await use_case(data)
    return post


@router.delete(
    "/delete",
)
async def delete(
    uuid: Annotated[UUID, Query()],
    use_case: FromDishka[DeletePostUseCase],
) -> None:
    await use_case(uuid)


@router.get("/list")
async def list(
    filters: Annotated[PostFilter, Query()],
    use_case: FromDishka[GetPostListUseCase],
) -> PostListDTO:
    posts = await use_case(GetPostListDTO(**filters.model_dump()))
    return posts
