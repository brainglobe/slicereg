from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray

from src.core.section.base import BaseSectionRepo, BaseSectionSerializer


class BaseLoadSectionPresenter(ABC):

    @abstractmethod
    def show_section(self, image: ndarray, transform: ndarray): ...


@dataclass
class LoadSectionWorkflow:
    section_repo: BaseSectionRepo
    presenter: BaseLoadSectionPresenter
    serializer: BaseSectionSerializer

    def __call__(self, filename: str) -> None:
        section = self.serializer.read(filename=filename)
        self.section_repo.save_section(section=section)
        self.presenter.show_section(
            image=section.channels[0],
            transform=section.affine_transform,
        )
