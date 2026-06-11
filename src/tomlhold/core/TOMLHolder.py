import io
import operator
import tomllib
from collections.abc import Iterable, Mapping, Sequence
from datetime import date, datetime, time
from functools import partial
from typing import Any, Self, cast, overload

import datahold  # type: ignore[import-untyped]
import setdoc
import tomli_w
from frozendict import frozendict

__all__ = ["TOMLHolder"]


def getdict(
    data: Mapping[str, Any],
    /,
    *,
    freeze: bool = False,
) -> dict[str, Any] | frozendict[str, Any]:
    "This function returns a TOML dict."
    ans: dict[str, Any]
    x: str
    z: str
    ans = dict()
    for x in frozendict(data).keys():
        if isinstance(x, str):
            z = str(x)
            ans[z] = getvalue(data[z], freeze=freeze)
            continue
        raise TypeError(
            f"The type {type(x).__name__!r} is not allowed for keys."
        )
    return frozendict(ans) if freeze else ans


@overload
def getkey(key: int) -> int: ...


@overload
def getkey(key: str) -> str: ...


def getkey(key: int | str) -> int | str:
    "This function returns a TOML key."
    if isinstance(key, int):
        return operator.index(key)
    if isinstance(key, str):
        return str(key)
    raise TypeError(
        f"The type {type(key).__name__!r} is not allowed for keys."
    )


def getkeys(keys: int | str | tuple[int | str, ...], /) -> list[int | str]:
    "This function returns TOML keys."
    if isinstance(keys, int | str):
        return [getkey(keys)]
    else:
        return list(map(getkey, keys))  # type: ignore[arg-type]


def getvalue(value: Any, /, *, freeze: bool = False) -> Any:
    "This function returns a TOML value."
    g: Iterable[Any]
    if isinstance(value, Mapping):
        return getdict(value, freeze=freeze)
    if isinstance(value, str):
        return str(value)
    if isinstance(value, Sequence):
        g = map(partial(getvalue, freeze=freeze), value)
        if freeze:
            return tuple(g)
        else:
            return list(g)
    if isinstance(value, bool):
        return bool(value)
    if isinstance(value, float):
        return float(value)
    if isinstance(value, int):
        return operator.index(value)
    if isinstance(value, datetime):
        return datetime(
            year=value.year,
            month=value.month,
            day=value.day,
            hour=value.hour,
            minute=value.minute,
            second=value.second,
            microsecond=value.microsecond,
            tzinfo=value.tzinfo,
            fold=value.fold,
        )
    if isinstance(value, date):
        return date(
            year=value.year,
            month=value.month,
            day=value.day,
        )
    if isinstance(value, time):
        return time(
            hour=value.hour,
            minute=value.minute,
            second=value.second,
            microsecond=value.microsecond,
            tzinfo=value.tzinfo,
            fold=value.fold,
        )
    raise TypeError(
        f"The type {type(value).__name__!r} is not allowed for values."
    )


class TOMLHolder(datahold.OkayDict):

    @setdoc.basic
    def __delitem__(
        self: Self,
        keys: int | str | tuple[int | str, ...],
    ) -> None:
        data_: dict | list
        keys_: list[int | str]
        lastkey: int | str
        keys_ = getkeys(keys)
        try:
            lastkey = keys_.pop()
        except Exception:
            self.clear()
            return
        data_ = self._data  # type: ignore[assignment]
        while keys_:
            data_ = data_[keys_.pop(0)]  # type: ignore[index]
        del data_[lastkey]  # type: ignore[arg-type]

    @setdoc.basic
    def __getitem__(
        self: Self,
        keys: int | str | tuple[int | str, ...],
    ) -> Any:
        data_: Any
        keys_: list
        key: Any
        keys_ = getkeys(keys)
        data_ = self._data
        for key in keys_:
            data_ = data_[key]
        return getvalue(data_)

    @setdoc.basic
    def __setitem__(
        self: Self,
        keys: int | str | tuple[int | str, ...],
        value: Any,
    ) -> None:
        data: Any
        k: Any
        keys_: list[int | str]
        lastkey: Any
        target: Any
        keys_ = getkeys(keys)
        if keys_ == []:
            self.data = value
            return
        lastkey = keys_.pop()
        data = getdict(self._data)
        target = data
        for k in keys_:
            if isinstance(target, dict):
                target = target.setdefault(k, {})
            else:
                target = target[k]
        target[lastkey] = value
        self.data = data

    @property
    @setdoc.basic
    def data(self: Self) -> frozendict[str, Any]:
        return cast(frozendict[str, Any], getdict(self._data, freeze=True))

    @data.setter
    def data(self: Self, value: Mapping[str, Any], /) -> None:
        self._data = cast(frozendict[str, Any], getdict(value))

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
    def load(cls: type[Self], stream: Any, **kwargs: Any) -> Self:
        "This classmethod loads data from byte stream."
        return cls(tomllib.load(stream, **kwargs))

    @classmethod
    def loadfromfile(cls: type[Self], file: str, **kwargs: Any) -> Self:
        "This classmethod loads data from file."
        stream: io.BufferedReader
        with open(file, "rb") as stream:
            return cls.load(stream, **kwargs)

    @classmethod
    def loads(cls: type[Self], string: str, **kwargs: Any) -> Self:
        "This classmethod loads data from string."
        return cls(tomllib.loads(string, **kwargs))

    @setdoc.basic
    def setdefault(self: Self, *keys: int | str, default: Any) -> Any:
        try:
            return self[keys]
        except Exception:
            self[keys] = default
            return self[keys]
