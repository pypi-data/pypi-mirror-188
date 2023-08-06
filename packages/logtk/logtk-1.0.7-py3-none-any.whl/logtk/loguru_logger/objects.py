import logging
from dataclasses import dataclass, field
from typing import Callable, List
from loguru import logger


@dataclass
class LoggerConfig:

    startswith: List[str] = field(default_factory=list)
    endswith: List[str] = field(default_factory=list)
    contains: List[str] = field(default_factory=list)
    include: List[str] = field(default_factory=list)
    exclude: List[str] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not (
            self.startswith
            or self.endswith
            or self.contains
            or self.exclude
            or self.include
        )

    def __contains__(self, __name: str):
        result = False
        for base in self.startswith:
            if __name.startswith(base):
                result = True
                break
        else:
            for base in self.endswith:
                if __name.endswith(base):
                    result = True
                    break
            else:
                for base in self.contains:
                    if base in __name:
                        result = True
                        break
        if result:
            if __name in self.exclude:
                result = False
        elif __name in self.include:
            result = True
        return result


class InterceptHandler(logging.Handler):
    def __init___(self, record_callback: Callable[[logging.LogRecord], str]):
        super().__init__()
        self.record_callback = record_callback

    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        message = self.record_callback(record)
        logger.opt(depth=depth, exception=record.exc_info).log(level, message)
