import time
from contextlib import asynccontextmanager
from typing import Callable, AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, Response
from loguru import logger

from app.config.constants import APP_NAME, APP_DESCRIPTION
from app.config.logger_config import configure_logger
from app.router import router


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator:
    configure_logger()
    logger.info("App setup done!")
    yield


def _add_middlewares(app: FastAPI) -> None:
    @app.middleware("http")
    async def logging_middleware(request: Request, call_next: Callable) -> Response:
        logger.info("{} {} from {}:{}", request.method, request.url, request.client.host, request.client.port)

        start_time = time.process_time()
        response: Response = await call_next(request)
        elapsed_time_ms = (time.process_time() - start_time) * 1000
        elapsed_time_ms_formatted = "{0:.2f}".format(elapsed_time_ms)

        logger.info("Request completed in {}ms with code {}", elapsed_time_ms_formatted, response.status_code)
        return response


def _generic_exception_handler(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"description": "Unexpected internal server error."}
    )


def default_app_factory() -> FastAPI:
    configure_logger()

    app = FastAPI(title=APP_NAME, description=APP_DESCRIPTION, lifespan=_lifespan)

    app.include_router(router=router)
    app.add_exception_handler(exc_class_or_status_code=Exception, handler=_generic_exception_handler)

    _add_middlewares(app=app)

    return app
