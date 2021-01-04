from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray

from src.use_cases.base import BaseUseCase, BaseSectionRepo


class BaseMoveSectionPresenter(ABC):

    @abstractmethod
    def update_section_transform(self, transform: ndarray) -> None: ...

    @abstractmethod
    def show_error(self, msg: str) -> None: ...


@dataclass
class MoveSectionUseCase(BaseUseCase):
    section_repo: BaseSectionRepo
    presenter: BaseMoveSectionPresenter

    def __call__(self, x=0., y=0., z=0., rx=0., ry=0., rz=0.) -> None:
        section = self.section_repo.get_section()
        if section is None:
            self.presenter.show_error("No section available to translate.")
            return
        new_section = section.translate(dx=x, dy=y, dz=z).rotate(dx=rx, dy=ry, dz=rz)

        self.section_repo.save_section(new_section)
        self.presenter.update_section_transform(transform=new_section.model_matrix)
