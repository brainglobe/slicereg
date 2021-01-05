from abc import ABC, abstractmethod

from src.core.section.models import Section


class BaseSectionRepo(ABC):

    @abstractmethod
    def get_section(self) -> Section: ...

    @abstractmethod
    def set_section(self, section: Section) -> None: ...


class BaseSectionSerializer(ABC):

    @abstractmethod
    def read(self, filename: str, *args, **kwargs) -> Section: ...

    @abstractmethod
    def write(self, section: Section, *args, **kwargs) -> None: ...
