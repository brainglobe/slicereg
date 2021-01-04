from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray

from src.use_cases.base import BaseUseCase, BaseAtlasRepo


class BaseLoadAtlasPresenter(ABC):

    @abstractmethod
    def show_atlas(self, volume: ndarray, transform: ndarray): ...


@dataclass
class LoadAtlasUseCase(BaseUseCase):
    atlas_repo: BaseAtlasRepo
    presenter: BaseLoadAtlasPresenter

    def __call__(self, resolution: int) -> None:
        atlas = self.atlas_repo.get_atlas(resolution_um=resolution)
        self.presenter.show_atlas(volume=atlas.volume, transform=atlas.model_matrix)
