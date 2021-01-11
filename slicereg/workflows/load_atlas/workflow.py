from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple

from numpy import ndarray

from slicereg.models.atlas import Atlas


@dataclass
class AtlasRepoData:
    volume: ndarray
    resolution_um: float
    origin: Tuple[float, float, float]


class BaseRepo(ABC):

    @abstractmethod
    def get_atlas(self, resolution: int) -> AtlasRepoData: ...


class LoadAtlasWorkflow:

    def __init__(self, repo: BaseRepo, presenter: BasePresenter):
        self._repo = repo
        self._presenter = presenter

    def __call__(self, resolution: int):
        data = self._repo.get_atlas(resolution=resolution)
        atlas = Atlas(volume=data.volume, resolution_um=data.resolution_um, origin=data.origin)
        self._presenter.show_atlas(volume=atlas.volume, transform=atlas.model_matrix)


class BasePresenter(ABC):

    @abstractmethod
    def show_atlas(self, volume: ndarray, transform: ndarray) -> None: ...

