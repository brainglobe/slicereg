from abc import ABC, abstractmethod

from numpy import ndarray

from slicereg.commands.base import BaseSectionRepo, BaseCommand
from slicereg.models.section import Section, Plane, SliceImage


class BaseSectionReader(ABC):

    @abstractmethod
    def read(self, filename: str) -> SliceImage: ...


class BaseLoadSectionPresenter(ABC):

    @abstractmethod
    def show(self, section: ndarray, model_matrix: ndarray): ...


class LoadImageCommand(BaseCommand):

    def __init__(self, repo: BaseSectionRepo, presenter: BaseLoadSectionPresenter, reader: BaseSectionReader):
        self._repo = repo
        self._presenter = presenter
        self._reader = reader

    def __call__(self, filename: str) -> None:
        slice_image = self._reader.read(filename=filename)
        section = Section(image=slice_image, plane=Plane(x=0, y=0))
        self._repo.save_section(section=section)
        self._presenter.show(section=section.image.channels[0], model_matrix=section.affine_transform)
