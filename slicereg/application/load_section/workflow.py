from abc import ABC, abstractmethod
from typing import NamedTuple, Optional

from numpy import ndarray

from slicereg.models.section import Section, Plane, SliceImage
from slicereg.application.shared.repos.base import BaseSectionRepo


class LoadSectionResponse(NamedTuple):
    section: ndarray
    model_matrix: ndarray


class BaseSelectChannelPresenter(ABC):

    @abstractmethod
    def show(self, data: LoadSectionResponse): ...


class SliceImageData(NamedTuple):
    channels: ndarray
    pixel_resolution_um: float


class BaseSectionReader(ABC):

    @abstractmethod
    def read(self, filename: str) -> SliceImageData: ...


class LoadImageWorkflow:

    def __init__(self, repo: BaseSectionRepo, presenter: BaseSelectChannelPresenter, reader: BaseSectionReader):
        self._repo = repo
        self._presenter = presenter
        self._reader = reader

    def execute(self, filename: str) -> None:
        slice_data = self._reader.read(filename=filename)
        section = Section(
            image=SliceImage(
                channels=slice_data.channels,
                pixel_resolution_um=slice_data.pixel_resolution_um
            ),
            plane=Plane(x=0, y=0)
        )

        self._repo.save_section(section=section)
        response = LoadSectionResponse(section=section.image.channels[0], model_matrix=section.affine_transform)
        self._presenter.show(response)
        # image=section.channels[0],
        # transform=section.affine_transform,
        # )
