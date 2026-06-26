from __future__ import annotations

import io
import operator
import tomllib
from collections.abc import Generator, Hashable, Iterable, Mapping, Sequence
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any, Self

import datahold
import tomli_w
from datahold.typing.SupportsKeysAndGetitem import SupportsKeysAndGetitem
from frozendict import frozendict

__all__ = ["TOMLDict", "TOMLList"]


def gendict(
    data: Any, /, *, dump: bool = False
) -> Generator[tuple[str, Any], None, None]:
    x: Hashable
    y: Any
    for x, y in dict(data).items():
        yield str(x), getvalue(y, dump=dump)


def genlist(
    data: Iterable[Any], /, *, dump: bool = False
) -> Generator[Any, None, None]:
    x: Any
    for x in data:
        yield getvalue(x, dump=dump)


def getvalue(value: Any, /, *, dump: bool = False) -> Any:
    "This function returns a TOML value."
    if value is None:
        return Decimal("nan")
    if isinstance(value, Mapping):
        if dump:
            return dict(gendict(value, dump=dump))
        else:
            return TOMLDict(value)
    if isinstance(value, str):
        return str(value)
    if isinstance(value, Sequence):
        if dump:
            return list(genlist(value, dump=dump))
        else:
            return TOMLList(value)
    if isinstance(value, bool):
        return bool(value)
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
    return Decimal(value)


class TOMLDict(datahold.HoldDict[str, Any]):
    @property
    def data(self: Self) -> frozendict[str, Any]:
        return self._data

    @data.setter
    def data(
        self: Self,
        value: (
            SupportsKeysAndGetitem[object, Any] | Iterable[tuple[object, Any]]
        ),
    ) -> None:
        self._data = frozendict(gendict(value, dump=False))

    def dump(self: Self, stream: Any, **kwargs: Any) -> None:
        "This method dumps the data into a byte stream."
        data_: dict[str, Any]
        data_ = dict(gendict(self._data, dump=True))
        tomli_w.dump(data_, stream, **kwargs)

    def dumpintofile(self: Self, file: str, **kwargs: Any) -> None:
        "This method dumps the data into a file."
        with open(file, "wb") as stream:
            self.dump(stream, **kwargs)

    def dumps(self: Self, **kwargs: Any) -> str:
        "This method dumps the data as a string."
        data_: dict[str, Any]
        data_ = dict(gendict(self._data, dump=True))
        return tomli_w.dumps(data_, **kwargs)

    @classmethod
    def load(cls: type[Self], stream: Any, /) -> Self:
        "This classmethod loads data from byte stream."
        return cls(tomllib.load(stream, parse_float=Decimal))

    @classmethod
    def loadfromfile(cls: type[Self], file: str) -> Self:
        "This classmethod loads data from file."
        stream: io.BufferedReader
        with open(file, "rb") as stream:
            return cls.load(stream)

    @classmethod
    def loads(cls: type[Self], string: str, /) -> Self:
        "This classmethod loads data from string."
        return cls(tomllib.loads(string, parse_float=Decimal))


class TOMLList(datahold.HoldList[Any]):
    @property
    def data(self: Self) -> tuple[Any, ...]:
        return self._data

    @data.setter
    def data(self: Self, value: Iterable[Any]) -> None:
        self._data = tuple(genlist(value, dump=False))
