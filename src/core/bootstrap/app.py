from fastapi import FastAPI

from src.core.settings import get_settings
from .middlewares import init_middlewares
from .routers import init_routers
from .handlers import init_handlers


def create_app() -> FastAPI:
    app_ = FastAPI(
        title=get_settings().app_name,
        description=get_settings().app_description,
        version=get_settings().version,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Initializing required dependencies
    init_handlers(app_=app_)
    init_middlewares(app_=app_)
    init_routers(app_=app_)

    return app_
