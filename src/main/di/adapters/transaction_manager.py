from dishka import Provider, provide, Scope

from adapters.password_hasher import PasswordHasherService
from adapters.transaction_manager import SqlAlchemyTransactionManager
from application.interfaces.password_hasher import PasswordHasherInterface
from application.interfaces.transaction_manager import TransactionManager


class SQLAlchemyTransactionManagerProvider(Provider):
    transaction_manager = provide(SqlAlchemyTransactionManager, provides=TransactionManager, scope=Scope.REQUEST)
