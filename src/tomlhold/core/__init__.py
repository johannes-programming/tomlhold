import tomllib
from datetime import date, datetime, time
from functools import partial
from typing import *

import setdoc
import tomli_w
from namings import FrozenNaming, Naming
from datahold import DataNaming

__all__ = ["TOMLHolder"]


VALUE = bool| float| int| str| datetime| date| time


def getnaming(data: Any, /, *, freeze: bool = False) -> Naming | FrozenNaming:
    "This function returns a TOML dict."
    ans: Naming
    x: Any
    y: Any
    ans = Naming()
    for x in FrozenNaming(data).keys():
        ans[x] = getvalue(y, freeze=freeze)
    if freeze:
        return FrozenNaming(ans)
    else:
        return ans


def getvalue(value: Any, /, *, freeze: bool = False) -> Any:
    "This function returns a TOML value."
    msg: str
    g: Iterable
    t: str
    if isinstance(value, (Naming, FrozenNaming)):
        return getnaming(value, freeze=freeze)
    if isinstance(value, (list, tuple)):
        g = map(partial(getvalue, freeze=freeze), value)
        if freeze:
            return tuple(g)
        else:
            return list(g)
    for t in (bool, float, int, str):
        if isinstance(value, t):
            return t(value)
    for t in (datetime, date, time):
        if type(value) is t:
            return value
    msg = "type %r is not allowed for values"
    msg %= type(value).__name__
    raise TypeError(msg)


class TOMLHolder(DataNaming[FrozenNaming|tuple|VALUE]):

    __slots__ = ("_frozen", "_unfrozen")

    data: FrozenNaming[FrozenNaming|tuple|VALUE]

    @property
    def data(self:Self) -> FrozenNaming:
        if self._frozen is None:
            self._frozen = getnaming(self._unfrozen, freeze=True)
        return self._frozen
            
    @data.setter
    def data(self:Self, value:Any) -> None:
        self._unfrozen = getvalue(value, freeze=False)
        self._frozen = None

    def delitem(self:Self, key0:Any, /, *keys:Any)-> Naming|list|FrozenNaming|tuple|VALUE:
        keys_:tuple
        target: Any
        keys_ = (key0,) + keys
        target = self._unfrozen
        for key in keys_[:-1]:
            target = target[key]
        del target[keys_[-1]] 
        self._frozen = None


    def dump(self: Self, stream: Any, **kwargs: Any) -> None:
        "This method dumps the data into a byte stream."
        tomli_w.dump(self._unfrozen, stream, **kwargs)

    def dumpintofile(self: Self, file: str, **kwargs: Any) -> None:
        "This method dumps the data into a file."
        with open(file, "wb") as stream:
            self.dump(stream, **kwargs)

    def dumps(self: Self, **kwargs: Any) -> str:
        "This method dumps the data as a string."
        return tomli_w.dumps(self._unfrozen, **kwargs)
    
    def getitem(self:Self, *keys:Any, frozen:bool = False)->Naming|list|FrozenNaming|tuple|VALUE:
        key:Any
        target: Any
        if frozen:
            target = self.data
        else:
            target = self._unfrozen
        for key in keys:
            target = target[key]
        return target

    @classmethod
    def load(cls: type, stream: Any, **kwargs: Any) -> Self:
        "This classmethod loads data from byte stream."
        return cls(tomllib.load(stream, **kwargs).items())

    @classmethod
    def loadfromfile(cls: type, file: str, **kwargs: Any) -> Self:
        "This classmethod loads data from file."
        with open(file, "rb") as stream:
            return cls.load(stream, **kwargs)

    @classmethod
    def loads(cls: type, string: str, **kwargs: Any) -> Self:
        "This classmethod loads data from string."
        return cls(tomllib.loads(string, **kwargs).items())
    

    def setitem(self:Self, *keys:Any, value:Any)-> Naming|list|FrozenNaming|tuple|VALUE:
        key:Any
        target: Any
        if len(keys) == 0:
            self.data = getnaming(value)
            return
        target = self.data
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = getvalue(value, freeze=False)
        self._frozen = None
