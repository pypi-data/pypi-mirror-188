import colortk
from time import time
from .objects import LogManager, TimeLogConfig, Colorizer
from typing import Optional, Callable, Union


def __logger_name(__file: str):
    result = __file.replace("/", ".").removesuffix(".py")
    if ".." in result:
        result = result.split("..", 1)[1]
    while result.startswith("."):
        result = result.removeprefix(".")
    return result


log_manager = LogManager(
    colorizer=Colorizer(name="log", colorize_base=colortk.colorizer("cyan"))
)


def __form_format_result(format_result, message_limit: int) -> Callable[[object], str]:
    format_base = lambda __result: str(format_result(__result))
    format_limit = lambda __result: format_base(__result)[:message_limit]
    format_unline = lambda __result: format_limit(__result).replace("\n", " ")
    return format_unline


def __form_log_message(config: TimeLogConfig, func):

    name_func = func.__name__

    colorize_time = colortk.colorizer("green")
    sublogger_name = __logger_name(config.file)
    colorizer_module = log_manager.sub_colorizer(sublogger_name, color=config.color)
    module_id = colorizer_module.colorized_id()

    colorizer_func = log_manager[sublogger_name].sub_colorizer(name_func)
    log_manager[sublogger_name][name_func] = colorizer_func
    func_id = colorizer_func.colorized_id()

    include_result = config.include_result
    format_result = config.format_result
    message_limit = config.message_limit

    form_result = __form_format_result(
        format_result=format_result, message_limit=message_limit
    )

    def log_message(result, elapsed: str):
        m_time_base = f"( {str(elapsed)[:12]}s )"
        m_time = colorize_time(m_time_base)
        args = ["INFO:     ", m_time, ": ", module_id, ".", func_id]
        if include_result:
            m_result = f": [{form_result(result)}]"
            args.append(m_result)
        print(*args, sep="")

    return log_message


def __timelog_sync(config: TimeLogConfig):
    def sublog(func):
        log_message = __form_log_message(config=config, func=func)

        def inner(*args, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            elapsed = time() - start
            log_message(result=result, elapsed=elapsed)
            return result

        return inner

    return sublog


def __timelog_async(config: TimeLogConfig):
    def sublog(func):
        log_message = __form_log_message(config=config, func=func)

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
    format_result: Callable[[object], str] = lambda value: value,
    message_limit: int = 200,
    is_async: bool = False,
):
    config_kwargs = dict(
        file=file,
        color=color,
        message_limit=message_limit,
        format_result=format_result,
        include_result=include_result,
    )
    config = TimeLogConfig(**config_kwargs)
    return (__timelog_async if is_async else __timelog_sync)(config=config)
