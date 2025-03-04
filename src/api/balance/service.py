from fastapi import Depends

from .repository import BalanceResultRepository


class BalanceResultService:

    def __init__(self, repository: BalanceResultRepository = Depends()):
        self.repository = repository

    async def save_result(self, balance_date: str, balance: float, source_file: str):
        await self.repository.save_result(balance_date=balance_date, balance=balance,
                                          source_file=source_file)
