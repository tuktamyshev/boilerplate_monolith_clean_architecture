from taskiq import TaskiqScheduler, async_shared_broker
from taskiq.brokers.shared_broker import AsyncSharedBroker
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import RedisStreamBroker

from config.base import Config
from config.logs import setup_logging
from controllers.tasks import notify_users_about_good_day
from main.di import init_worker_di
from main.exception_handlers import ExceptionLoggingMiddleware

# importing all tasks so that the worker and scheduler processes can see them
tasks = [
    notify_users_about_good_day,
]


def create_worker() -> RedisStreamBroker:
    config = Config()
    worker = RedisStreamBroker(
        url=f"{config.worker.BROKER_HOST}:{config.worker.BROKER_PORT}",
    ).with_middlewares(ExceptionLoggingMiddleware())

    init_worker_di(worker, config)
    setup_logging()

    return worker


def create_scheduler(broker: RedisStreamBroker, async_shared_broker: AsyncSharedBroker) -> TaskiqScheduler:
    scheduler = TaskiqScheduler(
        broker=broker,
        sources=[LabelScheduleSource(async_shared_broker)],
    )
    return scheduler


worker = create_worker()
async_shared_broker.default_broker(worker)

scheduler = create_scheduler(worker, async_shared_broker)
