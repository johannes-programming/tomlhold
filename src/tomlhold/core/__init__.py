import datetime
import tomllib
from typing import *

import tomli_w

import datahold

__all__ = ["Holder"]
NONITER = (
    bool,
    datetime.date,
    datetime.datetime,
    datetime.time,
    float,
    int,
    str,
)
KEYUNION = Union[int, str]
ITERUNION = Union[dict, list]
NONITERUNION = Union[NONITER]
TOTALUNION = Union[NONITERUNION, ITERUNION]


def _copy(value: NONITERUNION) -> NONITERUNION:
    if type(value) is dict:
        return _copy_dict(value)
    if type(value) is list:
        return _copy_list(value)
    if type(value) in NONITER:
        return value
    raise TypeError("type %r is not allowed" % type(value))


def _copy_dict(value: Any) -> Dict:
    return {str(k): _copy(value[k]) for k in value.keys()}


def _copy_list(value: Iterable) -> List:
    return [_copy(v) for v in value]


def _get_key(k: Any, /) -> KEYUNION:
    if issubclass(type(k), str):
        return str(k)
    else:
        return int(k)


def _get_keys(keys: Iterable, /) -> List[KEYUNION]:
    try:
        return [_get_key(keys)]
    except:
        pass
    return [_get_key(k) for k in keys]


def setdocstring(new: Any, /) -> Any:
    name = new.__name__
    old = getattr(datahold.OkayDict, name)
    new.__doc__ = old.__doc__
    return new


class Holder(datahold.OkayDict):
    @setdocstring
    def __delitem__(self, keys: Iterable) -> None:
        keys = _get_keys(keys)
        if not keys:
            self.clear()
            return
        ans = self._data
        while len(keys) > 1:
            ans = ans[keys.pop(0)]
        del ans[keys[0]]

    @setdocstring
    def __getitem__(self, keys: Iterable):
        keys = _get_keys(keys)
        ans = self._data
        for k in keys:
            ans = ans[k]
        ans = _copy(ans)
        return ans

    @setdocstring
    def __setitem__(self, keys: Iterable, value: TOTALUNION):
        keys = _get_keys(keys)
        if not keys:
            self.data = value
            return
        data = self.data
        ans = data
        while len(keys) > 1:
            k = keys.pop(0)
            if type(ans) is dict and type(keys[0]) is str:
                ans.setdefault(k, {})
            ans = ans[k]
        value = _copy(value)
        ans[keys[0]] = value
        self._data = data

    @setdocstring
    def __str__(self) -> str:
        return tomli_w.dumps(self._data)

    @property
    @setdocstring
    def data(self) -> Dict[str, Any]:
        return _copy_dict(self._data)

    @data.setter
    def data(self, value: Any) -> None:
        self._data = _copy_dict(value)

    @data.deleter
    def data(self):
        self.clear()

    def dump(self, file):
        """dump into toml file"""
        with open(file, "w") as s:
            s.write(str(self))

    @classmethod
    def fromdict(cls, dictionary: Any):
        """from a dict"""
        ans = cls()
        ans.data = dictionary
        return ans

    @classmethod
    def fromstr(cls, string: str):
        """from a str"""
        ans = cls()
        ans._data = tomllib.loads(string)
        return ans

    @setdocstring
    def get(self, *keys: KEYUNION, default: Any = None) -> TOTALUNION:
        try:
            return self[keys]
        except KeyError:
            return default

    @classmethod
    def load(cls, file: str) -> Self:
        """load from toml file"""
        with open(file, "r") as s:
            text = s.readlines()
        return cls(text)

    @setdocstring
    def setdefault(self, *keys, default: Any) -> Any:
        if not keys:
            return _copy_dict(self._data)
        keys = list(keys)
        data = self.data
        ans = data
        while len(keys) > 1:
            k = keys.pop(0)
            if type(ans) is dict and type(keys[0]) is str:
                ans.setdefault(k, {})
            ans = ans[k]
        if type(ans) is not dict or keys[0] in ans.keys():
            ans = ans[keys[0]]
            self._data = data
            return ans
        else:
            ans[keys[0]] = _copy(default)
            self._data = data
            return ans[keys[0]]
