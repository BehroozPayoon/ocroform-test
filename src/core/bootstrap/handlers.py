from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DBAPIError, NoResultFound


def init_handlers(app_: FastAPI) -> None:

    @app_.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = exc.errors()[0]
        msg = errors["msg"]
        if len(errors["loc"]) == 1:
            field = errors["loc"][0]
        else:
            field = errors["loc"][1]
        return JSONResponse(content={'error': msg, 'data': None,
                                     'status': False},
                            status_code=422)

    @app_.exception_handler(DBAPIError)
    async def database_error_handler(
        _: Request, exc: DBAPIError,
    ) -> JSONResponse:
        msg = str(exc.orig).split('DETAIL: ')[-1].rstrip('.')
        return JSONResponse(content={'error': msg, 'data': None,
                                     'status': False},
                            status_code=422)

    @app_.exception_handler(NoResultFound)
    async def database_not_found_handler(
        _: Request, exc: NoResultFound
    ) -> JSONResponse:
        return JSONResponse(
            content={'error': str(exc), 'data': None,
                     'status': False},
            status_code=404,
        )
