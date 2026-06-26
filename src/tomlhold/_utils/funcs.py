"""Provide generator and value conversion utilities for TOML data."""

from __future__ import annotations

__all__: list[str] = ["gendict", "genlist", "getvalue"]

import operator
from collections.abc import Generator, Hashable, Iterable, Mapping, Sequence
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any


def gendict(
    data: Any, /, *, dump: bool = False
) -> Generator[tuple[str, Any], None, None]:
    "Generate string-keyed items from mapping data for TOML."
    x: Hashable
    y: Any
    for x, y in dict(data).items():
        yield str(x), getvalue(y, dump=dump)


def genlist(
    data: Iterable[Any], /, *, dump: bool = False
) -> Generator[Any, None, None]:
    "Generate processed items from iterable data for TOML."
    x: Any
    for x in data:
        yield getvalue(x, dump=dump)


def getvalue(value: Any, /, *, dump: bool = False) -> Any:
    "Return a TOML value."
    if value is None:
        return Decimal("nan")
    if isinstance(value, Mapping):
        if dump:
            return dict(gendict(value, dump=dump))
        # The style guide prefers all imports at the top level of modules.
        # Compliance is impossible here because moving these imports to the
        # module top level would create a circular import with TOMLDict and
        # TOMLList causing import time failure before function execution.
        from ..core.TOMLDict import TOMLDict

        return TOMLDict(value)
    if isinstance(value, str):
        return str(value)
    if isinstance(value, Sequence):
        if dump:
            return list(genlist(value, dump=dump))
        from ..core.TOMLList import TOMLList

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
