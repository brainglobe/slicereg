from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union

from numpy import ndarray
from result import Result, Err, Ok

from slicereg.commands.base import BaseRepo, BaseRemoteAtlasReader, BaseLocalAtlasReader
from slicereg.core.atlas import Atlas

@dataclass(frozen=True)
class LoadBrainglobeAtlasRequest:
    name: str


@dataclass(frozen=True)
class LoadAtlasFromFileRequest:
    filename: str
    resolution_um: int


@dataclass(frozen=True)
class LoadAtlasData:
    volume: ndarray
    transform: ndarray
    resolution: float
    annotation_volume: Optional[ndarray]


@dataclass
class LoadAtlasCommand:
    _repo: BaseRepo
    _remote_atlas_reader: BaseRemoteAtlasReader
    _local_atlas_reader: BaseLocalAtlasReader

    def __call__(self, request: Union[LoadBrainglobeAtlasRequest, LoadAtlasFromFileRequest]) -> Result[LoadAtlasData, str]:
        if isinstance(request, LoadBrainglobeAtlasRequest):
            atlas_data = self._remote_atlas_reader.read(name=request.name)
            if atlas_data is None:
                return Err("Atlas not loaded.")
            atlas = Atlas(
                volume=atlas_data.registration_volume,
                resolution_um=atlas_data.resolution_um,
                annotation_volume=atlas_data.annotation_volume,
            )
        elif isinstance(request, LoadAtlasFromFileRequest):
            atlas_data2 = self._local_atlas_reader.read(filename=request.filename)
            if atlas_data2 is None:
                return Err("Atlas not loaded.")
            atlas = Atlas(
                volume=atlas_data2.registration_volume,
                resolution_um=request.resolution_um,
                annotation_volume=None,
            )

        self._repo.set_atlas(atlas=atlas)

        return Ok(LoadAtlasData(
            volume=atlas.volume,
            transform=atlas.shared_space_transform,
            resolution=atlas.resolution_um,
            annotation_volume=atlas.annotation_volume,
        ))
