from fastapi import APIRouter, Depends

from .service import BalanceResultService
from .schemas.requests import SingleFetchRequest

balance_router = APIRouter(prefix="/balances", tags=["Balance"])


@balance_router.post("/single")
def fetch_single_daily_balance(request: SingleFetchRequest,
                                     service: BalanceResultService = Depends()):
    service.operate_single_file(file_name=request.source_file)
    return "Ok"


@balance_router.post("/batch")
def add_user_take(service: BalanceResultService = Depends()):
    service.operate_batch()
    return "Ok"
