from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from src.models.section import Section


class BaseSectionRepo(ABC):

    @abstractmethod
    def get_section(self) -> Optional[Section]:  ...

    @abstractmethod
    def set_section(self, section: Section) -> None: ...


class InMemorySectionRepo(BaseSectionRepo):
    __section: Optional[Section] = None

    def get_section(self) -> Optional[Section]:
        return self.__class__.__section

    def set_section(self, section: Section) -> None:
        self.__class__.__section = section
