from __future__ import annotations

from abc import ABC, abstractmethod

from numpy import ndarray

from slicereg.commands.base import BaseSectionRepo


class BaseMoveSectionPresenter(ABC):

    @abstractmethod
    def show(self, transform: ndarray): ...

    @abstractmethod
    def show_error(self, msg: str): ...


class MoveSectionCommand:

    def __init__(self, repo: BaseSectionRepo, presenter: BaseMoveSectionPresenter):
        self._repo = repo
        self._presenter = presenter

    def __call__(self, x=0., y=0., z=0., rx=0., ry=0., rz=0.):
        sections = self._repo.sections
        if not sections:
            return self._presenter.show_error("No section available to translate.")
        section = sections[0]
        new_section = section.translate(dx=x, dy=y, dz=z).rotate(dx=rx, dy=ry, dz=rz)

        self._repo.save_section(new_section)
        self._presenter.show(transform=new_section.affine_transform)
