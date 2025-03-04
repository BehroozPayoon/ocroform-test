from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import SqlAlchemyRepository
from src.core.mocks import get_database_session
from .models import BalanceResult


class BalanceResultRepository(SqlAlchemyRepository[BalanceResult]):

    def __init__(self, session: AsyncSession = Depends(get_database_session)):
        super().__init__(session, BalanceResult)

    async def save_result(self, balance_date: str, balance: float, source_file: str):
        balance_result = BalanceResult(
            balance_date=balance_date, balance=balance, source_file=source_file)
        await self.save(balance_result)
