from fastapi import APIRouter

from .balance import balance_router

router = APIRouter()

router.include_router(balance_router)

__all__ = ["router"]
