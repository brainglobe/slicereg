from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray

from slicereg.application.shared.repos.base import BaseSectionRepo


@dataclass
class SectionTransformData:
    transform: ndarray


class MoveSectionWorkflow:

    def __init__(self, repo: BaseSectionRepo, presenter: BasePresenter):
        self._repo = repo
        self._presenter = presenter

    def __call__(self, x=0., y=0., z=0., rx=0., ry=0., rz=0.):
        section = self._repo.get_section()
        if section is None:
            return self._presenter.show_error("No section available to translate.")
        new_section = section.translate(dx=x, dy=y, dz=z).rotate(dx=rx, dy=ry, dz=rz)

        self._repo.set_section(new_section)
        self._presenter.update_transform(transform=new_section.affine_transform)


class BasePresenter(ABC):

    @abstractmethod
    def update_transform(self, transform: ndarray): ...

    @abstractmethod
    def show_error(self, msg: str): ...
