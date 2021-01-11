from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray
from result import Result, Err, Ok

from src.models.section import Section
from src.workflows.shared.repos.base import BaseSectionRepo


class BaseRepo(ABC):

    @abstractmethod
    def get_section(self) -> Section: ...


@dataclass
class SectionChannelData:
    section_image: ndarray


class SelectChannelWorkflow:

    def __init__(self, repo: BaseSectionRepo, presenter: BasePresenter):
        self._repo = repo
        self._presenter = presenter

    def __call__(self, num: int):
        section = self._repo.get_section()
        if section is None:
            self._presenter.present(Err("No section loaded yet."))
        try:
            image = section.channels[num - 1]
            self._presenter.present(Ok(SectionChannelData(section_image=image)))
        except IndexError:
            self._presenter.present(Err(f"Section doesn't have a Channel {num}."))

        
class BasePresenter(ABC):

    @abstractmethod
    def update_section_image(self, image: ndarray): ...

    @abstractmethod
    def show_error(self, msg: str): ...