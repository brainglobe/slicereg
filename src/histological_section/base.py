from abc import ABC, abstractmethod

from src.histological_section.models import Section


class BaseSectionRepo(ABC):

    @abstractmethod
    def get_section(self) -> Section: ...

    @abstractmethod
    def save_section(self, section: Section) -> None: ...