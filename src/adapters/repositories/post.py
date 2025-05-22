from dataclasses import dataclass

from sqlalchemy import func, select

from adapters.orm.base import BaseORM
from adapters.orm.post import PostORM
from adapters.repositories.base import SQLAlchemyRepository
from application.interfaces.repositories.post import (
    GetPostListDTO,
    PostInfoDTO,
    PostListDTO,
    PostRepository,
)
from domain.entities.base import BaseEntity
from domain.entities.post import PostEntity


@dataclass(frozen=True)
class SQLAlchemyPostRepository(PostRepository, SQLAlchemyRepository[PostEntity]):
    model: BaseORM = PostORM
    entity: BaseEntity = PostEntity

    async def get_list(self, filters: GetPostListDTO) -> PostListDTO:
        query = (
            select(
                PostORM,
                func.count().over().label("total_count"),
            )
            .limit(filters.limit)
            .offset(filters.offset)
        )

        if filters.text:
            query = query.filter(PostORM.text.ilike(f"%{filters.text}%"))
        if filters.date_from:
            query = query.filter(PostORM.created_at >= filters.date_from)
        if filters.date_to:
            query = query.filter(PostORM.created_at <= filters.date_to)
        if filters.user_uuid:
            query = query.filter(PostORM.user_uuid == filters.user_uuid)

        result = await self.session.execute(query)

        rows = result.all()

        posts_list = []
        total_count = 0
        for (
            post,
            count,
        ) in rows:
            posts_list.append(PostInfoDTO.model_validate(post))
            total_count = count

        return PostListDTO(items=posts_list, total=total_count)
