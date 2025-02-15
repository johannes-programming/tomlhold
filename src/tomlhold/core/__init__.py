import functools
import tomllib
from datetime import date, datetime, time
from typing import *

import datahold
import tomli_w

__all__ = ["Holder"]


# getdict
def getdict(d: dict, /) -> dict:
    "This function returns a TOML dict."
    ans = dict()
    for k in d.keys():
        if type(k) is not str:
            msg = "type %r is not allowed for keys of dictionaries"
            msg %= type(k).__name__
            raise TypeError(msg)
        ans[k] = getvalue(d[k])
    return ans


# getkey


def getkey(key: int | str) -> int | str:
    "This function returns a TOML key."
    if type(key) is int:
        return key
    if type(key) is str:
        return key
    msg = "type %r is not allowed for keys"
    msg %= type(key).__name__
    raise TypeError(msg)


# getkeys


def getkeys(keys: Any, /) -> List[int | str]:
    "This function returns TOML keys."
    if isinstance(keys, tuple):
        return [getkey(k) for k in keys]
    else:
        return [getkey(keys)]


# getvalue


def getvalue(value: Any, /) -> Any:
    "This function returns a TOML value."
    if isinstance(value, dict):
        return getdict(value)
    if isinstance(value, list):
        return [getvalue(v) for v in value]
    for t in (bool, float, int, str):
        if isinstance(value, t):
            return t(value)
    for t in (datetime, date, time):
        if type(value) is t:
            return value
    msg = "type %r is not allowed for values"
    msg %= type(value).__name__
    raise TypeError(msg)


# setdocstring


def setdocstring(new: Any, /) -> Any:
    "This decorator sets the doc string."
    name = new.__name__
    old = getattr(datahold.OkayDict, name)
    new.__doc__ = old.__doc__
    return new


class Holder(datahold.OkayDict):
    @setdocstring
    def __delitem__(self, keys: tuple | int | str) -> None:
        keys = getkeys(keys)
        if keys == []:
            self.clear()
            return
        lastkey = keys.pop(-1)
        ans = self._data
        while keys:
            ans = ans[keys.pop(0)]
        del ans[lastkey]

    @setdocstring
    def __getitem__(self, keys: tuple | int | str) -> Any:
        keys = getkeys(keys)
        ans = self._data
        for k in keys:
            ans = ans[k]
        ans = getvalue(ans)
        return ans

    @setdocstring
    def __setitem__(self, keys: tuple | int | str, value: Any) -> None:
        keys = getkeys(keys)
        if keys == []:
            self.data = value
            return
        lastkey = keys.pop(-1)
        target = data = self.data
        for k in keys:
            if isinstance(target, dict):
                target = target.setdefault(k, {})
            else:
                target = target[k]
        target[lastkey] = value
        self.data = data

    @property
    @setdocstring
    def data(self) -> dict[str, Any]:
        return getdict(dict(self._data))

    @data.setter
    def data(self, value: Any) -> None:
        self._data = getdict(dict(value))

    @data.deleter
    def data(self) -> None:
        self.clear()

    def dump(self, stream: Any, **kwargs: Any) -> None:
        "This method dumps the data into a byte stream."
        tomli_w.dump(self.data, stream, **kwargs)

    def dumpintofile(self, file: str, **kwargs: Any) -> None:
        "This method dumps the data into a file."
        with open(file, "wb") as stream:
            self.dump(stream, **kwargs)

    def dumps(self, **kwargs: Any) -> str:
        "This method dumps the data as a string."
        return tomli_w.dumps(self.data, **kwargs)

    @setdocstring
    def get(self, *keys: int | str, default: Any = None) -> Any:
        try:
            return self[keys]
        except KeyError:
            return default

    @classmethod
    def load(cls, stream: Any, **kwargs: Any) -> Self:
        "This classmethod loads data from byte stream."
        data = tomllib.load(stream, **kwargs)
        return cls(data)

    @classmethod
    def loadfromfile(cls, file: str, **kwargs: Any) -> Self:
        "This classmethod loads data from file."
        with open(file, "rb") as stream:
            return cls.load(stream, **kwargs)

    @classmethod
    def loads(cls, string: str, **kwargs: Any) -> Self:
        "This classmethod loads data from string."
        data = tomllib.loads(string)
        return cls(data, **kwargs)

    @setdocstring
    def setdefault(self, *keys: int | str, default: Any) -> Any:
        try:
            return self[keys]
        except:
            self[keys] = default
            return default
