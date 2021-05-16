from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from result import Err, Result, Ok

from slicereg.commands.base import BaseRepo


@dataclass(frozen=True)
class MapImageCoordToAtlasCoordData:
    ij: Tuple[int, int]
    xyz: Tuple[float, float, float]


@dataclass
class MapImageCoordToAtlasCoordCommand:
    _repo: BaseRepo

    def __call__(self, i: int, j: int) -> Result[MapImageCoordToAtlasCoordData, str]:
        sections = self._repo.get_sections()
        if not sections:
            return Err('no section loaded')
        section = sections[0]
        x, y, z = section.map_ij_to_xyz(i=i, j=j)
        return Ok(MapImageCoordToAtlasCoordData(ij=(i, j), xyz=(x, y, z)))
