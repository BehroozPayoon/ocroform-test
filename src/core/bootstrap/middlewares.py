from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def init_middlewares(app_: FastAPI) -> None:

    # CORSMiddleware
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
