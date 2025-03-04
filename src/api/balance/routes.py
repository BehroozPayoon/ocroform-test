from fastapi import APIRouter, Depends

from .service import BalanceResultService
from .schemas.requests import SingleFetchRequest

balance_router = APIRouter(prefix="/balances", tags=["Balance"])


@balance_router.post("/single")
async def fetch_single_daily_balance(request: SingleFetchRequest,
                                     service: BalanceResultService = Depends()):
    await service.operate_single_file(file_name=request.source_file)


@balance_router.post("/batch")
async def add_user_take(service: BalanceResultService = Depends()):
    await service.operate_batch()
