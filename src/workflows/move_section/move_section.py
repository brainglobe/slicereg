from abc import ABC, abstractmethod

from numpy import ndarray

from src.models.section import Section


class BaseRepo(ABC):

    @abstractmethod
    def get_section(self) -> Section: ...

    @abstractmethod
    def set_section(self, section: Section) -> None: ...


class BasePresenter(ABC):

    @abstractmethod
    def update_section_transform(self, transform: ndarray) -> None: ...

    @abstractmethod
    def show_error(self, msg: str) -> None: ...


class MoveSectionWorkflow:

    def __init__(self, repo: BaseRepo, presenter: BasePresenter):
        self._repo = repo
        self._presenter = presenter

    def __call__(self, x=0., y=0., z=0., rx=0., ry=0., rz=0.) -> None:
        section = self._repo.get_section()
        if section is None:
            self._presenter.show_error("No section available to translate.")
            return
        new_section = section.translate(dx=x, dy=y, dz=z).rotate(dx=rx, dy=ry, dz=rz)

        self._repo.set_section(new_section)
        self._presenter.update_section_transform(transform=new_section.affine_transform)
