from typing import *

from tomlhold._utils.Cfg import Cfg


# getkey
def getkey(key: int | str) -> int | str:
    "This function returns a TOML key."
    if type(key) is int:
        return key
    if type(key) is str:
        return key
    msg: str = Cfg.cfg.data["msg"]["general"]
    msg %= type(key).__name__
    raise TypeError(msg)


# getkeys
def getkeys(keys: Any, /) -> list[int | str]:
    "This function returns TOML keys."
    if isinstance(keys, tuple):
        return list(map(getkey, keys))
    else:
        return [getkey(keys)]
