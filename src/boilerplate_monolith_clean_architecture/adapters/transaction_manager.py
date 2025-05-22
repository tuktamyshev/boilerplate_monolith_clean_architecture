from dataclasses import dataclass
from types import TracebackType

from application.interfaces.transaction_manager import TransactionManager
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True)
class SqlAlchemyTransactionManager(TransactionManager):
    session: AsyncSession

    async def __aenter__(self) -> "SqlAlchemyTransactionManager":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
