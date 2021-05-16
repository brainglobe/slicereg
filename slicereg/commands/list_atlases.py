from __future__ import annotations

from dataclasses import dataclass
from typing import List

from result import Result, Ok

from slicereg.commands.base import BaseRemoteAtlasReader


@dataclass(frozen=True)
class ListBgAtlasesData:
    atlas_names: List[str]


@dataclass
class ListRemoteAtlasesCommand:
    _remote_atlas_reader: BaseRemoteAtlasReader

    def __call__(self) -> Result[ListBgAtlasesData, str]:
        atlas_names = self._remote_atlas_reader.list()
        return Ok(ListBgAtlasesData(atlas_names=atlas_names))