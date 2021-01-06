from abc import ABC, abstractmethod

from numpy import ndarray

from src.core.section.base import BaseSectionRepo


class BaseMoveSectionPresenter(ABC):

    @abstractmethod
    def update_section_transform(self, transform: ndarray) -> None: ...

    @abstractmethod
    def show_error(self, msg: str) -> None: ...


def move_section(section_repo: BaseSectionRepo, presenter: BaseMoveSectionPresenter, x=0., y=0., z=0., rx=0., ry=0., rz=0.) -> None:
        section = section_repo.get_section()
        if section is None:
            presenter.show_error("No section available to translate.")
            return
        new_section = section.translate(dx=x, dy=y, dz=z).rotate(dx=rx, dy=ry, dz=rz)

        section_repo.set_section(new_section)
        presenter.update_section_transform(transform=new_section.affine_transform)
