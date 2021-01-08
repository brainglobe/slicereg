from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray
from result import Result, Err, Ok

from src.models.section import Section


class BaseRepo(ABC):

    @abstractmethod
    def get_section(self) -> Section: ...


@dataclass
class SectionChannelData:
    section_image: ndarray


class SelectChannelWorkflow:

    def __init__(self, repo: BaseRepo):
        self._repo = repo

    def __call__(self, num: int) -> Result[SectionChannelData, str]:
        section = self._repo.get_section()
        if section is None:
            return Err("No section loaded yet.")
        try:
            image = section.channels[num - 1]
        except IndexError:
            return Err(f"Section doesn't have a Channel {num}.")

        return Ok(SectionChannelData(section_image=image))
