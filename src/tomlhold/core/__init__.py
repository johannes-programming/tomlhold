import tomllib
from typing import *

import datahold
import setdoc
import tomli_w
from frozendict import frozendict

from tomlhold._utils.keying import getkey, getkeys
from tomlhold._utils.norming import normvalue

__all__ = ["Holder"]


class Holder(datahold.OkayDict):
    data: frozendict

    @setdoc.basic
    def __delitem__(self: Self, keys: tuple | int | str) -> None:
        keys: list = getkeys(keys)
        if keys == []:
            self.clear()
            return
        lastkey = keys.pop(-1)
        data: dict = normvalue(self.data, freeze=False)
        stage: Any = data
        while keys:
            stage = stage[keys.pop(0)]
        del stage[lastkey]
        self.data = data

    @setdoc.basic
    def __getitem__(self: Self, keys: tuple | int | str) -> Any:
        return self.getitem(*getkeys(keys))

    @setdoc.basic
    def __setitem__(
        self: Self,
        keys: tuple | int | str,
        value: Any,
    ) -> None:
        keys: list = getkeys(keys)
        if keys == []:
            self.data = value
            return
        lastkey: Any = keys.pop(-1)
        data: Any = normvalue(self.data, freeze=False)
        stage: Any = data
        k: Any
        for k in keys:
            if isinstance(stage, dict):
                stage = stage.setdefault(k, {})
            else:
                stage = stage[k]
        stage[lastkey] = value
        self.data = data

    @property
    @setdoc.basic
    def data(self: Self) -> frozendict:
        return self._data

    @data.setter
    def data(self: Self, value: Any) -> None:
        self._data = normvalue(dict(value), freeze=True)

    def dump(self: Self, stream: Any, **kwargs: Any) -> None:
        "This method dumps the data into a byte stream."
        tomli_w.dump(normvalue(self.data, freeze=False), stream, **kwargs)

    def dumpintofile(self: Self, file: str, **kwargs: Any) -> None:
        "This method dumps the data into a file."
        stream: Any
        with open(file, "wb") as stream:
            self.dump(stream, **kwargs)

    def dumps(self: Self, **kwargs: Any) -> str:
        "This method dumps the data as a string."
        return tomli_w.dumps(normvalue(self.data, freeze=False), **kwargs)

    def get(
        self: Self,
        *keys: int | str,
        default: Any = None,
        unfreeze: Any = False,
    ) -> Any:
        "This method returns the value under the nested keys, or default if that turns up a KeyError."
        try:
            return self.getitem(*keys, unfreeze=unfreeze)
        except KeyError:
            return default

    def getitem(
        self: Self,
        *keys: int | str,
        unfreeze: Any = False,
    ) -> Any:
        "This method returns the value under the nested keys."
        stage: Any = self.data
        key: Any
        for key in map(getkey, keys):
            stage = stage[key]
        if unfreeze:
            stage = normvalue(stage, freeze=False)
        return stage

    @classmethod
    def load(cls: type, stream: Any, **kwargs: Any) -> Self:
        "This classmethod loads data from byte stream."
        data: dict = tomllib.load(stream, **kwargs)
        ans: Self = cls(data)
        return ans

    @classmethod
    def loadfromfile(cls: type, file: str, **kwargs: Any) -> Self:
        "This classmethod loads data from file."
        stream: Any
        with open(file, "rb") as stream:
            return cls.load(stream, **kwargs)

    @classmethod
    def loads(cls: type, string: str, **kwargs: Any) -> Self:
        "This classmethod loads data from string."
        data: dict = tomllib.loads(string)
        ans: Self = cls(data, **kwargs)
        return ans

    def setdefault(
        self: Self,
        *keys: int | str,
        default: Any,
        unfreeze: Any = False,
    ) -> Any:
        "This method returns the value under the nested keys, placing default there if none is there already."
        unf: bool = bool(unfreeze)
        ans: Any
        try:
            ans = self.getitem(*keys, unfreeze=unf)
        except KeyError:
            self[keys] = default
            ans = self.getitem(*keys, unfreeze=unf)
        return ans
