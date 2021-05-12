from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from numpy import ndarray

from slicereg.commands.base import BaseRepo, BaseRemoteAtlasReader, BaseLocalAtlasReader


@dataclass(frozen=True)
class LoadAtlasResult:
    volume: ndarray
    transform: ndarray
    resolution: float
    annotation_volume: Optional[ndarray]


@dataclass
class LoadRemoteAtlasCommand:
    _repo: BaseRepo
    _remote_atlas_reader: BaseRemoteAtlasReader

    def __call__(self, name: str) -> LoadAtlasResult:
        atlas = self._remote_atlas_reader.read(name=name)
        if atlas is None:
            raise RuntimeError("Atlas not loaded.")
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
    _local_atlas_reader: BaseLocalAtlasReader

    def __call__(self, filename: str, resolution_um: int) -> LoadAtlasResult:
        atlas = self._local_atlas_reader.read(filename=filename, resolution_um=resolution_um)
        self._repo.set_atlas(atlas=atlas)
        return LoadAtlasResult(
            volume=atlas.volume,
            transform=atlas.shared_space_transform,
            resolution=atlas.resolution_um,
            annotation_volume=None,
        )
