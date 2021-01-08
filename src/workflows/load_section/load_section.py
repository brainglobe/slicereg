from abc import ABC, abstractmethod

from numpy import ndarray

from src.models.section import Section


class BaseRepo(ABC):

    @abstractmethod
    def load_section(self, filename: str) -> Section: ...

    @abstractmethod
    def set_section(self, section: Section) -> None: ...


class BasePresenter(ABC):

    @abstractmethod
    def show_section(self, image: ndarray, transform: ndarray): ...


class LoadSectionWorkflow:

    def __init__(self, repo: BaseRepo, presenter: BasePresenter):
        self._repo = repo
        self._presenter = presenter

    def __call__(self, filename: str) -> None:
        section = self._repo.load_section(filename=filename)
        self._repo.set_section(section=section)
        self._presenter.show_section(
            image=section.channels[0],
            transform=section.affine_transform,
        )
