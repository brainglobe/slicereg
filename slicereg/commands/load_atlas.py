from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from numpy import ndarray

from slicereg.commands.base import BaseRepo, BaseRemoteAtlasReader, BaseLocalAtlasReader
from slicereg.core.atlas import Atlas


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
        atlas_data = self._remote_atlas_reader.read(name=name)
        if atlas_data is None:
            raise RuntimeError("Atlas not loaded.")



        atlas = Atlas(
            volume=atlas_data.registration_volume,
            resolution_um=resolution if (resolution := atlas_data.resolution_um) is not None else 25.,
            annotation_volume=atlas_data.annotation_volume,
        )

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
        atlas_data = self._local_atlas_reader.read(filename=filename)
        if atlas_data is None:
            raise RuntimeError("Atlas loading failed.")

        atlas = Atlas(
            volume=atlas_data.registration_volume,
            resolution_um=resolution if (resolution := atlas_data.resolution_um) is not None else resolution_um,
            annotation_volume=atlas_data.annotation_volume,
        )

        self._repo.set_atlas(atlas=atlas)

        return LoadAtlasResult(
            volume=atlas.volume,
            transform=atlas.shared_space_transform,
            resolution=atlas.resolution_um,
            annotation_volume=None,
        )
