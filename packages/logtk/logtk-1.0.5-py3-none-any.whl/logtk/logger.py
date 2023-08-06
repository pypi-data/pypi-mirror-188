import colortk
from time import time
from dataclasses import dataclass, field
from typing import Optional, Callable, Dict, Union, Any


def __removeprefix(__str: str, __affix: str):
    result = __str
    while result.startswith(__affix):
        result = result.removeprefix(__affix)
    return result


def logger_name(__file: str):
    result = __file.replace("/", ".").removesuffix(".py")
    result = __removeprefix(result, ".")
    result = __removeprefix(result, "app")
    result = __removeprefix(result, ".")
    return result


@dataclass(frozen=False, order=True)
class Colorizer:

    name: str
    colorize_base: Callable[[str], str]
    colorizer_map: Dict[str, Any] = field(default_factory=dict)

    def __getitem__(self, __key: str):
        result: Colorizer = self.colorizer_map[__key]
        return result

    def __contains__(self, __key: str):
        return __key in self.colorizer_map

    def __setitem__(self, __key: str, value):
        self.colorizer_map[__key] = value

    @property
    def colorized_id(self) -> str:
        return self.colorize(self.name)

    def colorize(self, __str: str):
        return self.colorize_base(__str)

    def sub_colorizer(self, __key: str, color: Optional[Union[str, int]] = None):
        if __key in self:
            colorizer = self[__key]
        else:
            name = __key
            colorize = colortk.colorizer(color=color)
            colorizer = Colorizer(name=name, colorize=colorize)
            self[__key] = colorizer
        return colorizer


class LogManager:

    colorizer: Colorizer = field(
        default=Colorizer(name="log", colorize_base=colortk.colorizer("cyan"))
    )


log_manager = LogManager()


def log(__file: str, __message, color: Optional[str] = None, limit: int = 200):
    colorizer = log_manager.colorizer.sub_colorizer(__file, color=color)
    module_id = colorizer.colorize(colorizer.name)
    message = module_id + f":[{str(__message)[:limit]}]"
    print(message)


def timelog(settings: dict):
    """
    settings are required:
    {
        "file":__file__,
        "color":None,
        "limit":200
    }
    """
    file = settings["file"]
    color = settings.get("color", None)
    limit = settings.get("limit", 200)
    time_colorizer = colortk.colorizer("green")
    sublogger_name = logger_name(file)
    module_colorizer = log_manager.colorizer.sub_colorizer(sublogger_name, color=color)
    module_id = module_colorizer.colorized_id

    def sublog(func):
        method_name = func.__name__
        func_colorizer = module_colorizer.sub_colorizer(method_name)
        log_manager[file][method_name] = func_colorizer
        func_id = func_colorizer.colorize(func_colorizer.name)
        address = module_id + "." + func_id

        def log_message(result, elapsed: str):
            m_time_base = f"[[{str(elapsed)[:12]}]:"
            m_result = f"[{str(result)[:limit]}]"
            m_time = time_colorizer(m_time_base)
            message = m_time + address + ":", m_result
            print(message)

        def inner(*args, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            elapsed = time() - start
            log_message(result=result, elapsed=elapsed)
            return result

        return inner

    return sublog
