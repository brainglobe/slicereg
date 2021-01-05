from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray

from src.reference_atlas.models import Atlas


class BaseAtlasRepo(ABC):

    @abstractmethod
    def get_atlas(self, resolution_um: int) -> Atlas: ...

    @abstractmethod
    def get_current_atlas(self) -> Atlas: ...


class BaseLoadAtlasPresenter(ABC):

    @abstractmethod
    def show_atlas(self, volume: ndarray, transform: ndarray): ...


@dataclass
class LoadAtlasUseCase:
    atlas_repo: BaseAtlasRepo
    presenter: BaseLoadAtlasPresenter

    def __call__(self, resolution: int) -> None:
        atlas = self.atlas_repo.get_atlas(resolution_um=resolution)
        self.presenter.show_atlas(volume=atlas.volume, transform=atlas.model_matrix)