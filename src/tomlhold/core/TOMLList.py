"""Provide the TOMLList class for holding TOML array data."""

from __future__ import annotations

__all__: list[str] = ["TOMLList"]

from collections.abc import Iterable
from typing import Any, Self

import datahold

from .._utils.funcs import genlist


class TOMLList(datahold.HoldList[Any]):
    @property
    def data(self: Self) -> tuple[Any, ...]:
        "Return the held list data as tuple."
        return self._data

    @data.setter
    def data(self: Self, value: Iterable[Any]) -> None:
        "Set the held list data from an iterable."
        self._data = tuple(genlist(value, dump=False))
