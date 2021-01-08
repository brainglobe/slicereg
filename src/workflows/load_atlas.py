from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray
from result import Result, Ok

from src.models.atlas import Atlas


class BaseRepo(ABC):

    @abstractmethod
    def load_atlas(self, resolution: int) -> Atlas: ...


class BasePresenter(ABC):

    @abstractmethod
    def show_atlas(self, volume: ndarray, transform: ndarray): ...


@dataclass
class AtlasData:
    atlas_volume: ndarray
    atlas_transform: ndarray


class LoadAtlasWorkflow:

    def __init__(self, repo: BaseRepo):
        self._repo = repo

    def __call__(self, resolution: int) -> Result[AtlasData, str]:
        atlas = self._repo.load_atlas(resolution=resolution)
        return Ok(AtlasData(atlas_volume=atlas.volume, atlas_transform=atlas.model_matrix))
