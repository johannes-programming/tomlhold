import tomllib
from datetime import date, datetime, time
from typing import *

import datahold
import setdoc
import tomli_w

__all__ = ["Holder", "TOMLHolder"]


def getdict(d: dict, /) -> dict:
    "This function returns a TOML dict."
    ans: dict
    k: Any
    msg: str
    ans = dict()
    for k in d.keys():
        if type(k) is not str:
            msg = "type %r is not allowed for keys of dictionaries"
            msg %= type(k).__name__
            raise TypeError(msg)
        ans[k] = getvalue(d[k])
    return ans


def getkey(key: int | str) -> int | str:
    "This function returns a TOML key."
    msg: str
    if type(key) is int:
        return key
    if type(key) is str:
        return key
    msg = "type %r is not allowed for keys"
    msg %= type(key).__name__
    raise TypeError(msg)


def getkeys(keys: Any, /) -> list[int | str]:
    "This function returns TOML keys."
    if isinstance(keys, tuple):
        return list(map(getkey, keys))
    else:
        return [getkey(keys)]


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


def setdocstring(new: Any, /) -> Any:
    "This decorator sets the doc string."
    name: Any = new.__name__
    old: Any = getattr(datahold.OkayDict, name)
    new.__doc__ = old.__doc__
    return new


class TOMLHolder(datahold.OkayDict):
    @setdoc.basic
    def __delitem__(self: Self, keys: tuple | int | str) -> None:
        keys = getkeys(keys)
        if keys == []:
            self.clear()
            return
        lastkey = keys.pop(-1)
        ans = self._data
        while keys:
            ans = ans[keys.pop(0)]
        del ans[lastkey]

    @setdoc.basic
    def __getitem__(self: Self, keys: tuple | int | str) -> Any:
        keys: list = getkeys(keys)
        ans: Any = self._data
        key: Any
        for key in keys:
            ans = ans[key]
        ans = getvalue(ans)
        return ans

    @setdoc.basic
    def __setitem__(self: Self, keys: tuple | int | str, value: Any) -> None:
        keys: list = getkeys(keys)
        if keys == []:
            self.data = value
            return
        lastkey: Any = keys.pop(-1)
        data: Any = self.data
        target: Any = data
        k: Any
        for k in keys:
            if isinstance(target, dict):
                target = target.setdefault(k, {})
            else:
                target = target[k]
        target[lastkey] = value
        self.data = data

    @property
    @setdocstring
    def data(self: Self) -> dict[str, Any]:
        return getdict(dict(self._data))

    @data.setter
    def data(self: Self, value: Any) -> None:
        self._data = getdict(dict(value))

    @data.deleter
    def data(self: Self) -> None:
        self.clear()

    def dump(self: Self, stream: Any, **kwargs: Any) -> None:
        "This method dumps the data into a byte stream."
        tomli_w.dump(self.data, stream, **kwargs)

    def dumpintofile(self: Self, file: str, **kwargs: Any) -> None:
        "This method dumps the data into a file."
        with open(file, "wb") as stream:
            self.dump(stream, **kwargs)

    def dumps(self: Self, **kwargs: Any) -> str:
        "This method dumps the data as a string."
        return tomli_w.dumps(self.data, **kwargs)

    @setdocstring
    def get(self: Self, *keys: int | str, default: Any = None) -> Any:
        try:
            return self[keys]
        except KeyError:
            return default

    @classmethod
    def load(cls: type, stream: Any, **kwargs: Any) -> Self:
        "This classmethod loads data from byte stream."
        data: dict = tomllib.load(stream, **kwargs)
        ans: Self = cls(data)
        return ans

    @classmethod
    def loadfromfile(cls: type, file: str, **kwargs: Any) -> Self:
        "This classmethod loads data from file."
        with open(file, "rb") as stream:
            return cls.load(stream, **kwargs)

    @classmethod
    def loads(cls: type, string: str, **kwargs: Any) -> Self:
        "This classmethod loads data from string."
        data: dict = tomllib.loads(string)
        ans: Self = cls(data, **kwargs)
        return ans

    @setdocstring
    def setdefault(self: Self, *keys: int | str, default: Any) -> Any:
        ans: Any
        try:
            ans = self[keys]
        except:
            self[keys] = default
            ans = self[keys]
        return ans


Holder: type = TOMLHolder
