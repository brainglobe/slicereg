from abc import ABC, abstractmethod
from typing import Optional

from numpy import ndarray

from src.core.models.atlas import Atlas


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


def load_atlas(repo: BaseAtlasRepo, serializer: BaseAtlasSerializer, presenter: BaseLoadAtlasPresenter, resolution: int) -> None:
        atlas = repo.get_atlas()
        if atlas is None or atlas.resolution_um != resolution:
            atlas = serializer.read(resolution_um=resolution)
            repo.set_atlas(atlas=atlas)

        presenter.show_atlas(volume=atlas.volume, transform=atlas.model_matrix)
