from abc import ABC, abstractmethod
from typing import Optional

from slicereg.models.section import Section


class BaseSectionRepo(ABC):

    @abstractmethod
    def get_section(self) -> Optional[Section]:  ...

    @abstractmethod
    def set_section(self, section: Section) -> None: ...