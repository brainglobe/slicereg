from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from numpy import ndarray

from src.core.atlas.models import Atlas


class BaseAtlasRepo(ABC):

    @abstractmethod
    def get_atlas(self) -> Optional[Atlas]: ...

    @abstractmethod
    def set_atlas(self, atlas: Atlas) -> None: ...


class BaseAtlasSerializer(ABC):

    @abstractmethod
    def read(self, resolution_um: int) -> Atlas: ...


class BaseLoadAtlasPresenter(ABC):

    @abstractmethod
    def show_atlas(self, volume: ndarray, transform: ndarray): ...


@dataclass
class LoadAtlasWorkflow:
    repo: BaseAtlasRepo
    serializer: BaseAtlasSerializer
    presenter: BaseLoadAtlasPresenter

    def __call__(self, resolution: int) -> None:
        atlas = self.repo.get_atlas()
        if atlas is None or atlas.resolution_um != resolution:
            atlas = self.serializer.read(resolution_um=resolution)
            self.repo.set_atlas(atlas=atlas)

        self.presenter.show_atlas(volume=atlas.volume, transform=atlas.model_matrix)
