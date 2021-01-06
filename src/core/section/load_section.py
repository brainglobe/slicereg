from abc import ABC, abstractmethod

from numpy import ndarray

from src.core.section.base import BaseSectionRepo, BaseSectionSerializer


class BaseLoadSectionPresenter(ABC):

    @abstractmethod
    def show_section(self, image: ndarray, transform: ndarray): ...


def load_section(section_repo: BaseSectionRepo, presenter: BaseLoadSectionPresenter, serializer: BaseSectionSerializer, filename: str) -> None:
    section = serializer.read(filename=filename)
    section_repo.set_section(section=section)
    presenter.show_section(
        image=section.channels[0],
        transform=section.affine_transform,
    )
