import logging
import sys
from pprint import pformat
from typing import Any
from loguru import logger
from loguru._defaults import LOGURU_FORMAT
from .objects import InterceptHandler, LoggerConfig


def format_record(record: dict) -> str:

    format_string = LOGURU_FORMAT
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


def init_logging(
    logger_config: LoggerConfig = LoggerConfig(
        startswith=[], endswith=[], contains=[], include=[], exclude=[]
    )
):

    if not logger_config.is_empty:
        system_loggers = [
            logging.getLogger(name) for name in logging.root.manager.loggerDict
        ]
        system_loggers_names = [sublogger.name for sublogger in system_loggers]
        system_loggers_names.sort()
        logged_modules = [
            sublogger for sublogger in system_loggers if sublogger.name in logger_config
        ]
        for sublogger in logged_modules:
            sublogger.handlers = []

        intercept_handler = InterceptHandler(level=logging.DEBUG)
        for logged_module in logged_modules:
            logging.getLogger(logged_module.name).handlers = [intercept_handler]

        logger.configure(
            handlers=[
                {"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}
            ]
        )


def log(__level: int or str, __message: str, *args: Any, **kwargs: Any):
    logger.log(__level, __message, *args, **kwargs)


def info(__message: str, *args: Any, **kwargs: Any):
    logger.info(__message, *args, **kwargs)


def error(__message: str, *args: Any, **kwargs: Any):
    logger.error(__message, *args, **kwargs)
