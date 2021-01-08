from abc import ABC, abstractmethod

from numpy import ndarray

from src.models.atlas import Atlas


class BaseRepo(ABC):

    @abstractmethod
    def load_atlas(self, resolution: int) -> Atlas: ...


class BasePresenter(ABC):

    @abstractmethod
    def show_atlas(self, volume: ndarray, transform: ndarray): ...


class LoadAtlasWorkflow:

    def __init__(self, repo: BaseRepo, presenter: BasePresenter):
        self._repo = repo
        self._presenter = presenter

    def __call__(self, resolution: int) -> None:
        atlas = self._repo.load_atlas(resolution=resolution)
        self._presenter.show_atlas(volume=atlas.volume, transform=atlas.model_matrix)
