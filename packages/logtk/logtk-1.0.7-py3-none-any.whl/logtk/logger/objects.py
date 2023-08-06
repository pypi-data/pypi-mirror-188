import colortk
from dataclasses import dataclass, field
from typing import Optional, Callable, Dict, Union, Any


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


@dataclass(frozen=False, order=True)
class TimeLogConfig:
    file: str
    color: Optional[Union[str, int]]
    include_result: bool
    format_result: Callable[[object], str]
    message_limit: int
    include_result: bool
