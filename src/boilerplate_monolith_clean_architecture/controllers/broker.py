from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.confluent.fastapi import KafkaRouter

from application.interfaces.user_notificator import NotifyUsersDTO
from application.use_cases.notify_users import NotifyUsersUseCase

router = KafkaRouter()


@router.subscriber(
    "receive-something-from-broker",
    group_id="monolith-backend-boilerplate.receive-something-from-broker",
)
@inject
async def receive_something_from_broker(
    data: NotifyUsersDTO,
    use_case: FromDishka[NotifyUsersUseCase],
) -> None:
    # An example of receiving messages from a broker
    await use_case(data)
