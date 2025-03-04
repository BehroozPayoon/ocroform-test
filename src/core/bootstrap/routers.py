from fastapi import FastAPI

from src.api import router as api_router


def init_routers(app_: FastAPI):

    app_.include_router(api_router)
