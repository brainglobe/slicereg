from typing import Optional

from src.models.section import Section


class InMemoryStorage:
    _section: Optional[Section] = None  # ClassVar

    @property
    def section(self) -> Optional[Section]:
        return self.__class__._section

    @section.setter
    def section(self, section: Section) -> None:
        self.__class__._section = section
