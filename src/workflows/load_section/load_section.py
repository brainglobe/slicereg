from abc import ABC, abstractmethod

from numpy import ndarray

from src.models.section import Section
from src.workflows.shared.section_repo import BaseSectionRepo


class BasePresenter(ABC):

    @abstractmethod
    def show_section(self, image: ndarray, transform: ndarray): ...


class BaseSectionReader(ABC):

    @abstractmethod
    def read(self, filename: str) -> Section: ...


class LoadSectionWorkflow:

    def __init__(self, repo: BaseSectionRepo, presenter: BasePresenter, reader: BaseSectionReader):
        self._repo = repo
        self._presenter = presenter
        self._reader = reader

    def __call__(self, filename: str) -> None:
        section = self._reader.read(filename=filename)
        self._repo.set_section(section=section)
        self._presenter.show_section(
            image=section.channels[0],
            transform=section.affine_transform,
        )
