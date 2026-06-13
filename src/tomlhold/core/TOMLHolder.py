from __future__ import annotations

import operator
from collections.abc import Iterable, Iterator, Mapping, Sequence, Callable
from typing import Any, Optional, Self, overload, ParamSpecArgs

import setdoc
import datahold
from frozendict import frozendict
from datetime import datetime, date, time
from functools import partial, wraps
import enum

__all__ = ["TOMLHolder"]


class Missing(enum.Enum):
    missing = None


def find(data:dict[str, Any], key:Any, /) -> tuple[Any, Any]:
    if isinstance(key, tuple):
        keys = tuple(key)
    else:
        keys = key,
    ans = data
    for x in keys[:-1]:
        if isinstance(ans, dict):
            ans = ans.setdefault(str(x), dict())
        else:
            ans = ans[x]
    if isinstance(ans, dict):
        return ans, str(keys[-1])
    else:
        return ans, keys[-1]




def getdict(mapping: Mapping, /, *, freeze:bool) -> dict:
    ans:dict[str, Any]
    x:object
    y:Any
    ans = dict()
    for x in mapping.keys():
        y=getvalue(mapping[x], freeze=freeze)
        if y is not None:
            ans[str(x)] = y
    if freeze:
        return frozendict(ans)
    else:
        return ans

def getkey(key: object) -> int|str:
    try:
        return operator.index(key)
    except Exception:
        return str(key)
    
def getkeys(keys: object) -> tuple[int|str]:
    if isinstance(keys, tuple):
        return tuple(map(getkey, keys))
    else:
        return getkey(keys),

def getvalue(value: Any, /, *, freeze: bool) -> Any:
    "This function returns a TOML value."
    g: Iterator
    if value is None:
        return None
    if isinstance(value, Mapping):
        return getdict(value, freeze=freeze)
    if isinstance(value, str):
        return str(value)
    if isinstance(value, Sequence):
        g = map(partial(getvalue, freeze=freeze), value)
        g = filter(partial(operator.is_not, None), g)
        if freeze:
            return tuple(g)
        else:
            return list(g)
    if isinstance(value, bool):
        return bool(value)
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
    if isinstance(value, float):
        return float(value)
    if isinstance(value, int):
        return operator.index(value)
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

class TOMLHolder(datahold.HoldDict):

    @setdoc.basic
    def __delitem__(self: Self, key: Any, /) -> None:
        operator.delitem(*self._find(key))

    @setdoc.basic
    def __getitem__(self: Self, key: Any, /) -> Any:
        return getvalue(operator.getitem(*self._find(key)), freeze=False)
    
    @setdoc.basic
    def __setitem__(
        self: Self,
        key: object,
        value: Any,
        /,
    ) -> None:
        if value is None:
            try:
                del self[key]
            except Exception:
                pass
            return
        operator.setitem(*self._find(key), getvalue(value, freeze=False))
    
    def _find(self:Self, key:Any, /) -> tuple[Any, Any]:
        if isinstance(key, tuple):
            keys = tuple(key)
        else:
            keys = key,
        ans = self._data
        for x in keys[:-1]:
            if isinstance(ans, dict):
                ans = ans.setdefault(str(x), dict())
            else:
                ans = ans[x]
        if isinstance(ans, dict):
            return ans, str(keys[-1])
        else:
            return ans, keys[-1]
        
    
    @property
    @setdoc.basic
    def data(self:Self) -> frozendict[str, Any]:
        return getvalue(self._data, freeze=True)
    
    @data.setter
    def data(self:Self, value:Any) -> None:
        if value is None:
            del self.data
            return
        self._data = getdict(value, freeze=False)

    @data.deleter
    def data(self:Self) -> None:
        self._data.clear()

    @setdoc.basic
    def get(
        self: Self,
        key: Any,
        default: Any = None,
        /,
        *,
        frozen: bool = False,
    ) -> Any:
        try:
            return getvalue(operator.getitem(*self._find(key)), freeze=frozen)
        except Exception:
            return default


    @overload
    @setdoc.setdoc(datahold.DataDict.pop.__doc__)
    def pop(
        self: Self, 
        key: object, 
        /, 
        *, 
        frozen:bool = False,
    ) -> Any: ...

    @overload
    @setdoc.setdoc(datahold.DataDict.pop.__doc__)
    def pop(
        self: Self,
        key: object,
        default: Any,
        /,
        *, 
        frozen:bool = False,
    ) -> Any: ...

    @setdoc.setdoc(datahold.DataDict.pop.__doc__)
    def pop(
        self: Self,
        key: object,
        default: Any = Missing.missing,
        /,
        *, 
        frozen:bool = False,
    ) -> Any:
        args:tuple
        data_, x = self._find(key)
        if isinstance(default, Missing):
            return data_.pop(x)
        try:
            return data_.pop(x)
        except Key

        keys = getkeys(key)
        unfrozen=self._data
        if not keys:
            del self.data
            return getdict(unfrozen, freeze=frozen)
        if isinstance(default, Missing):
            for x in keys[:-1]:
                unfrozen = unfrozen[x]
            return unfrozen.pop(keys[-1])
        try:
            for x in keys[:-1]:
                unfrozen = unfrozen[x]
            return unfrozen.pop(keys[-1])
        except Exception:
            return default

    @setdoc.setdoc(dict.setdefault.__doc__)
    def setdefault(
        self: Self,
        key: object,
        default: Any = None,
        /,
    ) -> Optional[Value]:
        ans: Optional[Value]
        data: dict[Key | str, Optional[Value]]
        data = dict(self.data)
        ans = data.setdefault(key, default)
        self.data = frozendict(data)
        return ans

    @setdoc.setdoc(dict.update.__doc__)
    def update(
        self: Self,
        other: (
            SupportsKeysAndGetitem[Key | str, Optional[Value]]
            | Iterable[tuple[Key | str, Optional[Value]]]
        ) = (),
        /,
        **kwargs: Optional[Value],
    ) -> None:
        data: dict[Key | str, Optional[Value]]
        data = dict(self.data)
        data.update(other, **kwargs)
        self.data = frozendict(data)
