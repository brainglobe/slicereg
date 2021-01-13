from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, NamedTuple

from numpy import ndarray

from slicereg.models.atlas import Atlas


@dataclass
class AtlasRepoData:
    volume: ndarray
    resolution_um: float
    origin: Tuple[float, float, float]


class BaseLoadAtlasRepo(ABC):

    @abstractmethod
    def get_atlas(self, resolution: int) -> AtlasRepoData: ...

    @abstractmethod
    def get_downloaded_resolutions(self) -> Tuple[int, ...]: ...


class LoadAtlasModel(NamedTuple):
    reference_volume: ndarray
    atlas_transform: ndarray
    atlas_resolution: int


class LoadAtlasWorkflow:

    def __init__(self, repo: BaseLoadAtlasRepo, presenter: BasePresenter):
        self._repo = repo
        self._presenter = presenter

    def execute(self, resolution: int):
        data = self._repo.get_atlas(resolution=resolution)
        atlas = Atlas(volume=data.volume, resolution_um=data.resolution_um, origin=data.origin)
        response = LoadAtlasModel(
            reference_volume=atlas.volume,
            atlas_transform=atlas.model_matrix,
            atlas_resolution=int(atlas.resolution_um),
        )
        self._presenter.show(response)


class BasePresenter(ABC):

    @abstractmethod
    def show(self, data: LoadAtlasModel) -> None: ...
