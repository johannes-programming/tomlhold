from __future__ import annotations

import operator
from collections.abc import Generator, Hashable, Iterable, Mapping, Sequence
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any

__all__ = ["gendict", "genlist", "getvalue"]


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
