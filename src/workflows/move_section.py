from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray
from result import Result, Err, Ok

from src.models.section import Section


class BaseRepo(ABC):

    @abstractmethod
    def get_section(self) -> Section: ...

    @abstractmethod
    def set_section(self, section: Section) -> None: ...

@dataclass
class SectionTransformData:
    transform: ndarray


class MoveSectionWorkflow:

    def __init__(self, repo: BaseRepo):
        self._repo = repo

    def __call__(self, x=0., y=0., z=0., rx=0., ry=0., rz=0.) -> Result[SectionTransformData, str]:
        section = self._repo.get_section()
        if section is None:
            return Err("No section available to translate.")
        new_section = section.translate(dx=x, dy=y, dz=z).rotate(dx=rx, dy=ry, dz=rz)

        self._repo.set_section(new_section)
        return Ok(SectionTransformData(transform=new_section.affine_transform))
