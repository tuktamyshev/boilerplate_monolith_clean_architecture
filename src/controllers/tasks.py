from dishka import FromDishka
from dishka.integrations.taskiq import inject
from taskiq.brokers.shared_broker import shared_task

from application.interfaces.user_notificator import NotifyUsersDTO, UserNotificatorInterface


@shared_task(schedule=[{"cron": "* * * * *"}])  # every hour
@inject
async def notify_users_about_good_day(
    user_notificator: FromDishka[UserNotificatorInterface],
) -> None:
    # Example of scheduling by taskiq
    # This would not work because users connected to app instance but this is worker.
    # TODO Need to implement redis pub\sub for websocket connections
    await user_notificator.notify_users_about_something(NotifyUsersDTO(text="have a good day!"))
