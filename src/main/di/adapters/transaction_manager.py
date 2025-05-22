from dishka import Provider, Scope, provide

from adapters.transaction_manager import SqlAlchemyTransactionManager
from application.interfaces.transaction_manager import TransactionManager


class SQLAlchemyTransactionManagerProvider(Provider):
    transaction_manager = provide(SqlAlchemyTransactionManager, provides=TransactionManager, scope=Scope.REQUEST)
