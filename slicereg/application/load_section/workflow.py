from abc import ABC, abstractmethod
from typing import NamedTuple

from numpy import ndarray

from slicereg.application.shared.repos.base import BaseSectionRepo
from slicereg.models.section import Section, Plane, SliceImage


class BaseSelectChannelPresenter(ABC):

    @abstractmethod
    def show(self, section: ndarray, model_matrix: ndarray): ...


class BaseSectionReader(ABC):

    @abstractmethod
    def read(self, filename: str) -> SliceImage: ...


class LoadImageWorkflow:

    def __init__(self, repo: BaseSectionRepo, presenter: BaseSelectChannelPresenter, reader: BaseSectionReader):
        self._repo = repo
        self._presenter = presenter
        self._reader = reader

    def execute(self, filename: str) -> None:
        slice_image = self._reader.read(filename=filename)
        section = Section(image=slice_image, plane=Plane(x=0, y=0))
        self._repo.save_section(section=section)
        self._presenter.show(section=section.image.channels[0], model_matrix=section.affine_transform)
