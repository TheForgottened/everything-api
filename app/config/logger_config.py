import inspect
import logging
import os
import sys
from typing import TYPE_CHECKING
from warnings import filterwarnings

from loguru import logger

if TYPE_CHECKING:
    from loguru import Record

_LOGGER_LEVEL = "DEBUG"
_LOGGER_FORMAT = "[{time}][LEVEL={level}][FILE={extra[relpath]}:{line}][FUNC={function}()] {message}\n{exception}"


class LoguruInterceptHandler(logging.Handler):
    _IGNORED_LOGGERS = ("uvicorn.access",)

    def emit(self, record: logging.LogRecord) -> None:
        if record.name in self._IGNORED_LOGGERS:
            return

        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def _custom_format(record: "Record") -> str:
    record["extra"] |= {"relpath": f"{record['name'].replace('.', os.sep)}.py"}

    return _LOGGER_FORMAT


def _add_loguru_handler_to_all_loggers() -> None:
    for logger_name in ["", *logging.Logger.manager.loggerDict.keys()]:
        std_logger = logging.getLogger(logger_name)
        std_logger.handlers.clear()
        std_logger.propagate = False
        std_logger.addHandler(LoguruInterceptHandler())

    logging.basicConfig(handlers=[LoguruInterceptHandler()], level=0, force=True)


def _configure_ignored_warnings() -> None:
    filterwarnings("ignore", message=".*Duplicate Operation ID.*for function do at .*")


def configure_logger() -> None:
    logger.remove()
    logger.add(sink=sys.stdout, level=_LOGGER_LEVEL, format=_custom_format)

    _add_loguru_handler_to_all_loggers()
    _configure_ignored_warnings()
