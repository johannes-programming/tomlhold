from typing import Final

from tomlhold.core.TOMLHolder import TOMLHolder

__all__ = ["Holder", "TOMLHolder"]


Holder: Final[type[TOMLHolder]] = TOMLHolder
