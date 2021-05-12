from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from numpy import ndarray

from slicereg.app.repo import BaseRepo
from slicereg.io.bg_atlasapi import BrainglobeAtlasReader
from slicereg.io.imio import ImioAtlasReader



@dataclass(frozen=True)
class LoadAtlasResult:
    volume: ndarray
    transform: ndarray
    resolution: float
    annotation_volume: Optional[ndarray]


@dataclass
class LoadBrainglobeAtlasCommand:
    _repo: BaseRepo
    _reader: BrainglobeAtlasReader

    def __call__(self, bgatlas_name: str) -> LoadAtlasResult:
        atlas = self._reader.read(path=bgatlas_name)
        self._repo.set_atlas(atlas=atlas)
        return LoadAtlasResult(
            volume=atlas.volume,
            transform=atlas.shared_space_transform,
            resolution=atlas.resolution_um,
            annotation_volume=atlas.annotation_volume,
        )


@dataclass
class LoadAtlasFromFileCommand:
    _repo: BaseRepo
    _reader: ImioAtlasReader

    def __call__(self, filename: str, resolution_um: int) -> LoadAtlasResult:
        atlas = self._reader.read(path=filename, resolution_um=resolution_um)
        self._repo.set_atlas(atlas=atlas)
        return LoadAtlasResult(
            volume=atlas.volume,
            transform=atlas.shared_space_transform,
            resolution=atlas.resolution_um,
            annotation_volume=None,
        )
