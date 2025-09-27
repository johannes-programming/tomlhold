from datetime import date, datetime, time
from typing import *

from frozendict import frozendict

from tomlhold._utils.Cfg import Cfg


# norm
def normvalue(value: Any, /, **kwargs: Any) -> Any:
    try:
        keys: Any = value.keys
    except AttributeError:
        return normnondict(value, **kwargs)
    else:
        return normwithkeys(value, keys=keys, **kwargs)


def normwithkeys(
    data: Any,
    *,
    keys: Callable,
    freeze: bool,
) -> dict | frozendict:
    proto: dict = dict()
    k: Any
    for k in keys():
        if type(k) is str:
            proto[k] = normvalue(data[k], freeze=freeze)
            continue
        raise TypeError(Cfg.cfg.data["msg"]["dict"] % type(k).__name__)
    if freeze:
        return frozendict(proto)
    else:
        return proto


def normnondict(value: Any, /, freeze: bool) -> Any:
    x: type
    for x in (bool, float, int, str):
        if isinstance(value, x):
            return x(value)
    for x in (datetime, date, time):
        if type(value) is x:
            return value
    g: Iterator = (normvalue(x, freeze=freeze) for x in value)
    if freeze:
        return tuple(g)
    else:
        return list(g)
