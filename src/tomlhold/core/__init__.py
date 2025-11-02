import tomllib
from datetime import date, datetime, time
from functools import partial
from typing import *

import datahold
import setdoc
import tomli_w
from frozendict import frozendict

__all__ = ["Holder", "TOMLHolder"]


def getdict(d: dict, /, *, freeze: bool = False) -> dict | frozendict:
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
        ans[k] = getvalue(d[k], freeze=freeze)
    if freeze:
        return frozendict(ans)
    else:
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


def getvalue(value: Any, /, *, freeze: bool = False) -> Any:
    "This function returns a TOML value."
    msg: str
    g: Iterable
    t: str
    if isinstance(value, (dict, frozendict)):
        return getdict(value, freeze=freeze)
    if isinstance(value, (list, tuple)):
        g = map(partial(getvalue, freeze=freeze), value)
        if freeze:
            return tuple(g)
        else:
            return list(g)
    for t in (bool, float, int, str):
        if isinstance(value, t):
            return t(value)
    for t in (datetime, date, time):
        if type(value) is t:
            return value
    msg = "type %r is not allowed for values"
    msg %= type(value).__name__
    raise TypeError(msg)


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
        keys: list
        key: Any
        ans: Any
        keys = getkeys(keys)
        ans = self._data
        for key in keys:
            ans = ans[key]
        ans = getvalue(ans)
        return ans

    @setdoc.basic
    def __setitem__(self: Self, keys: tuple | int | str, value: Any) -> None:
        lastkey: Any
        keys: list
        data: Any
        target: Any
        k: Any
        keys = getkeys(keys)
        if keys == []:
            self.data = value
            return
        lastkey = keys.pop()
        data = getdict(self._data)
        target = data
        for k in keys:
            if isinstance(target, dict):
                target = target.setdefault(k, {})
            else:
                target = target[k]
        target[lastkey] = value
        self.data = data

    @property
    @setdoc.basic
    def data(self: Self) -> frozendict[str, Any]:
        return getdict(self._data, freeze=True)

    @data.setter
    def data(self: Self, value: Any) -> None:
        self._data = getdict(dict(value))

    @data.deleter
    def data(self: Self) -> None:
        self.clear()

    def dump(self: Self, stream: Any, **kwargs: Any) -> None:
        "This method dumps the data into a byte stream."
        tomli_w.dump(self._data, stream, **kwargs)

    def dumpintofile(self: Self, file: str, **kwargs: Any) -> None:
        "This method dumps the data into a file."
        with open(file, "wb") as stream:
            self.dump(stream, **kwargs)

    def dumps(self: Self, **kwargs: Any) -> str:
        "This method dumps the data as a string."
        return tomli_w.dumps(self._data, **kwargs)

    def get(self: Self, *keys: int | str, default: Any = None) -> Any:
        "This method returns self[*keys] if that exists, otherwise default."
        try:
            return self[keys]
        except KeyError:
            return default

    @classmethod
    def load(cls: type, stream: Any, **kwargs: Any) -> Self:
        "This classmethod loads data from byte stream."
        data: dict
        ans: Self
        data = tomllib.load(stream, **kwargs)
        ans = cls(data)
        return ans

    @classmethod
    def loadfromfile(cls: type, file: str, **kwargs: Any) -> Self:
        "This classmethod loads data from file."
        with open(file, "rb") as stream:
            return cls.load(stream, **kwargs)

    @classmethod
    def loads(cls: type, string: str, **kwargs: Any) -> Self:
        "This classmethod loads data from string."
        data: dict
        ans: Self
        data = tomllib.loads(string)
        ans = cls(data, **kwargs)
        return ans

    def setdefault(self: Self, *keys: int | str, default: Any) -> Any:
        "This method returns self[*keys] after setting it to default if previously absent."
        ans: Any
        try:
            ans = self[keys]
        except:
            self[keys] = default
            ans = self[keys]
        return ans


Holder: type = TOMLHolder
