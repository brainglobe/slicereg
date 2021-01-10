from __future__ import annotations

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

    def __init__(self, repo: BaseRepo, presenter: BasePresenter):
        self._repo = repo
        self._presenter = presenter

    def __call__(self, resolution: int):
        data = self._repo.get_atlas(resolution=resolution)
        atlas = Atlas(volume=data.volume, resolution_um=data.resolution_um, origin=data.origin)
        response = Ok(AtlasData(atlas_volume=atlas.volume, atlas_transform=atlas.model_matrix))
        self._presenter.present(response)


class BasePresenter(ABC):

    @abstractmethod
    def present(self, data: Result[AtlasData, str]): ...

