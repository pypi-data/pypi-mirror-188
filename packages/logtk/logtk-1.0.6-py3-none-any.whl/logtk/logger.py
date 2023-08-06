import colortk
from time import time
from dataclasses import dataclass, field
from typing import Optional, Callable, Dict, Union, Any


def __removeprefix(__str: str, __affix: str):
    result = __str
    while result.startswith(__affix):
        result = result.removeprefix(__affix)
    return result


def __logger_name(__file: str):
    result = __file.replace("/", ".").removesuffix(".py")
    if ".." in result:
        result = result.split("..",1)[1]
    result = __removeprefix(result,".")
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

    def colorized_id(self):
        return self.colorize(self.name)

    def colorize(self, __str: str):
        return self.colorize_base(__str)

    def sub_colorizer(self, __key: str, color: Optional[Union[str, int]] = None):
        if __key in self:
            colorizer = self[__key]
        else:
            name = __key
            colorize_base = colortk.colorizer(color=color)
            colorizer = Colorizer(name=name, colorize_base=colorize_base)
            self[__key] = colorizer
        return colorizer


@dataclass(frozen=False, order=True)
class LogManager:

    colorizer: Colorizer

    def __getitem__(self, key: str):
        return self.colorizer[key]

    def __setitem__(self, key: str, value):
        self.colorizer[key] = value

    def sub_colorizer(self, __key: str, color: Optional[Union[str, int]] = None):
        if __key in self.colorizer:
            result = self.colorizer[__key]
        else:
            colorizer = self.colorizer
            result = colorizer.sub_colorizer(__key, color=color)
            self.colorizer = colorizer
        return result


log_manager = LogManager(
    colorizer=Colorizer(name="log", colorize_base=colortk.colorizer("cyan"))
)


def form_log_message(settings: dict, func):
    file = settings["file"]
    color = settings.get("color", None)
    limit = settings.get("limit", 200)
    include_result = settings.get("include_result", True)
    format_result = settings.get("format_result",lambda value:value)
    time_colorizer = colortk.colorizer("green")
    sublogger_name = __logger_name(file)
    module_colorizer = log_manager.sub_colorizer(sublogger_name, color=color)
    module_id = module_colorizer.colorized_id()

    method_name = func.__name__
    func_colorizer = log_manager[sublogger_name].sub_colorizer(method_name)
    log_manager[sublogger_name][method_name] = func_colorizer
    func_id = func_colorizer.colorized_id()

    def log_message(result, elapsed: str):
        m_time_base = f"( {str(elapsed)[:12]}s )"
        m_time = time_colorizer(m_time_base)

        args = ["INFO:     ", m_time, ": ", module_id, ".", func_id]
        if include_result:
            m_result_base = str(format_result(result))[:limit].replace("\n", " ")
            m_result = f"[{m_result_base}]"
            args.extend([": ", m_result])
        # message = module_id+"."+func_id+": "+m_time+": "+m_result
        print(*args, sep="")

    return log_message


def timelog_sync(settings: dict):
    def sublog(func):
        log_message = form_log_message(settings=settings, func=func)

        def inner(*args, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            elapsed = time() - start
            log_message(result=result, elapsed=elapsed)
            return result

        return inner

    return sublog


def timelog_async(settings: dict):
    def sublog(func):
        log_message = form_log_message(settings=settings, func=func)

        async def inner(*args, **kwargs):
            start = time()
            result = await func(*args, **kwargs)
            elapsed = time() - start
            log_message(result=result, elapsed=elapsed)
            return result

        return inner

    return sublog


def timelog(
    file: str,
    color: Optional[Union[str, int]] = None,
    include_result: bool = True,
    format_result: Callable[[object],str] = lambda value:value,
    limit: int = 200,
    is_async: bool = False,
):
    settings = dict(file=file, color=color, limit=limit,format_result=format_result, include_result=include_result)
    return (timelog_async if is_async else timelog_sync)(settings=settings)

