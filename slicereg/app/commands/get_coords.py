from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from slicereg.app.commands.base import BaseSectionRepo
from slicereg.app.repo import BaseRepo


@dataclass(frozen=True)
class MapImageCoordToAtlasCoordResult:
    ij: Tuple[int, int]
    xyz: Tuple[float, float, float]


@dataclass
class MapImageCoordToAtlasCoordCommand:
    _repo: BaseRepo

    def __call__(self, i: int, j: int) -> MapImageCoordToAtlasCoordResult:
        sections = self._repo.get_sections()
        if not sections:
            raise RuntimeError('no section loaded')
        section = sections[0]
        x, y, z = section.map_ij_to_xyz(i=i, j=j)
        return MapImageCoordToAtlasCoordResult(ij=(i, j), xyz=(x, y, z))
