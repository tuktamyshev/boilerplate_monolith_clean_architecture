from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
    route_class=DishkaRoute,
)


@router.get("")
async def healthcheck() -> None:
    return
