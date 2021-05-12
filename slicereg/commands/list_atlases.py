from __future__ import annotations

from dataclasses import dataclass
from typing import List

from slicereg.commands.base import BaseRemoteAtlasReader


@dataclass(frozen=True)
class ListBgAtlasesResult:
    atlas_names: List[str]


@dataclass
class ListRemoteAtlasesCommand:
    _remote_atlas_reader: BaseRemoteAtlasReader

    def __call__(self):
        atlas_names = self._remote_atlas_reader.list()
        return ListBgAtlasesResult(atlas_names=atlas_names)
