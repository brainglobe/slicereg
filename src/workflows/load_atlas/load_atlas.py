from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple

from numpy import ndarray
from result import Result, Ok

from src.models.atlas import Atlas

@dataclass
class AtlasRepoData:
    volume: ndarray
    resolution_um: float
    origin: Tuple[float, float, float]


class BaseRepo(ABC):

    @abstractmethod
    def get_atlas(self, resolution: int) -> AtlasRepoData: ...


@dataclass
class AtlasData:
    atlas_volume: ndarray
    atlas_transform: ndarray


class LoadAtlasWorkflow:

    def __init__(self, repo: BaseRepo):
        self._repo = repo

    def __call__(self, resolution: int) -> Result[AtlasData, str]:
        data = self._repo.get_atlas(resolution=resolution)
        atlas = Atlas(volume=data.volume, resolution_um=data.resolution_um, origin=data.origin)
        return Ok(AtlasData(atlas_volume=atlas.volume, atlas_transform=atlas.model_matrix))


@dataclass
class BaseLoadAtlasView(ABC):

    @abstractmethod
    def show_atlas(self, volume: ndarray, transform: ndarray) -> None: ...

    @abstractmethod
    def show_error(self, msg: str) -> None: ...


@dataclass
class LoadAtlasController:
    view: BaseLoadAtlasView
    _load_atlas: LoadAtlasWorkflow

    def load_atlas(self, resolution: int) -> None:
        result = self._load_atlas(resolution=resolution)
        if result.is_ok():
            data = result.value
            self.view.show_atlas(volume=data.atlas_volume, transform=data.atlas_transform)
        else:
            self.view.show_error(result.value)