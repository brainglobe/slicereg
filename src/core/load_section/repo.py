from abc import ABC, abstractmethod
from typing import Optional

from src.core.load_section.load_section import BaseRepo
from src.core.models.section import Section


class BaseSectionSerializer(ABC):

    @abstractmethod
    def read(self, filename: str) -> Section: ...


class SectionRepo(BaseRepo):

    def __init__(self, serializer: BaseSectionSerializer):
        self._serializer = serializer
        self._section: Optional[Section] = None

    def load_section(self, filename: str) -> Section:
        return self._serializer.read(filename=filename)

    def get_section(self) -> Optional[Section]:
        return self._section

    def set_section(self, section: Section) -> None:
        self._section = section
