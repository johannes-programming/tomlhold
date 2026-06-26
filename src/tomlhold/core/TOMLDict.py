"""Provide the TOMLDict class for holding TOML table data."""

from __future__ import annotations

__all__: list[str] = ["TOMLDict"]

import io
import tomllib
from collections.abc import Iterable
from decimal import Decimal
from typing import Any, Self

import datahold
import tomli_w
from datahold.typing.SupportsKeysAndGetitem import SupportsKeysAndGetitem
from frozendict import frozendict

from .._utils.funcs import gendict


class TOMLDict(datahold.HoldDict[str, Any]):
    @property
    def data(self: Self) -> frozendict[str, Any]:
        "Return the held dictionary data."
        return self._data

    @data.setter
    def data(
        self: Self,
        value: (
            SupportsKeysAndGetitem[object, Any] | Iterable[tuple[object, Any]]
        ),
    ) -> None:
        "Set the held dictionary data from keys and values."
        self._data = frozendict(gendict(value, dump=False))

    def dump(self: Self, stream: Any, /, **kwargs: Any) -> None:
        "Dump the data into a byte stream."
        data_: dict[str, Any]
        data_ = dict(gendict(self._data, dump=True))
        tomli_w.dump(data_, stream, **kwargs)

    def dumpintofile(self: Self, file: str, /, **kwargs: Any) -> None:
        "Dump the data into a file."
        with open(file, "wb") as stream:
            self.dump(stream, **kwargs)

    def dumps(self: Self, **kwargs: Any) -> str:
        "Dump the data as a string."
        data_: dict[str, Any]
        data_ = dict(gendict(self._data, dump=True))
        return tomli_w.dumps(data_, **kwargs)

    @classmethod
    def load(cls: type[Self], stream: Any, /) -> Self:
        "Load data from a byte stream."
        return cls(tomllib.load(stream, parse_float=Decimal))

    @classmethod
    def loadfromfile(cls: type[Self], file: str, /) -> Self:
        "Load data from a file."
        stream: io.BufferedReader
        with open(file, "rb") as stream:
            return cls.load(stream)

    @classmethod
    def loads(cls: type[Self], string: str, /) -> Self:
        "Load data from a string."
        return cls(tomllib.loads(string, parse_float=Decimal))
