"""Export the public TOML data holder classes."""

from __future__ import annotations

__all__: list[str] = ["TOMLDict", "TOMLList"]

from .core.TOMLDict import TOMLDict
from .core.TOMLList import TOMLList
