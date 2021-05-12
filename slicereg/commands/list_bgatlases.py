from __future__ import annotations

from dataclasses import dataclass
from typing import List

from slicereg.io.brainglobe.atlas import BrainglobeAtlasReader


@dataclass(frozen=True)
class ListBgAtlasesResult:
    atlas_names: List[str]


@dataclass
class ListBgAtlasesCommand:
    _reader: BrainglobeAtlasReader

    def __call__(self):
        atlas_names = self._reader.list_available()
        return ListBgAtlasesResult(atlas_names=atlas_names)
