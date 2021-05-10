from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from slicereg.commands.base import BaseSectionRepo
from slicereg.repos.atlas_repo import AtlasRepo


@dataclass(frozen=True)
class MapImageCoordToAtlasCoordResult:
    ij: Tuple[int, int]
    xyz: Tuple[float, float, float]


@dataclass
class MapImageCoordToAtlasCoordCommand:
    _repo: BaseSectionRepo
    _atlas_repo: AtlasRepo

    def __call__(self, i: int, j: int) -> MapImageCoordToAtlasCoordResult:
        sections = self._repo.sections
        if not sections:
            raise RuntimeError('no section loaded')
        section = sections[0]
        x, y, z = section.map_ij_to_xyz(i=i, j=j)
        return MapImageCoordToAtlasCoordResult(ij=(i, j), xyz=(x, y, z))
