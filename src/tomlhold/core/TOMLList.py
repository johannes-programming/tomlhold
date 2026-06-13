from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Self

import datahold

from .._utils.funcs import genlist

__all__ = ["TOMLList"]


class TOMLList(datahold.HoldList[Any]):
    @property
    def data(self: Self) -> tuple[Any, ...]:
        return self._data

    @data.setter
    def data(self: Self, value: Iterable[Any]) -> None:
        self._data = tuple(genlist(value, dump=False))
