from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple

from numpy import ndarray  # type: ignore

from slicereg.commands.base import BaseCommand
from slicereg.models.atlas import Atlas


class BaseLoadAtlasRepo(ABC):

    @abstractmethod
    def get_atlas(self, resolution: int) -> Atlas: ...

    @abstractmethod
    def get_downloaded_resolutions(self) -> Tuple[int, ...]: ...


class BaseLoadAtlasPresenter(ABC):

    @abstractmethod
    def show(self, reference_volume: ndarray, atlas_transform: ndarray, atlas_resolution: int) -> None: ...


class LoadAtlasCommand(BaseCommand):

    def __init__(self, repo: BaseLoadAtlasRepo, presenter: BaseLoadAtlasPresenter):
        self._repo = repo
        self._presenter = presenter

    def __call__(self, resolution: int):
        atlas = self._repo.get_atlas(resolution=resolution)
        self._presenter.show(reference_volume=atlas.volume, atlas_transform=atlas.model_matrix,
                             atlas_resolution=int(atlas.resolution_um))
