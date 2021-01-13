from abc import ABC, abstractmethod
from typing import Optional, List

from slicereg.models.section import Section


class BaseSectionRepo(ABC):

    @property
    @abstractmethod
    def sections(self) -> List[Section]:  ...

    @abstractmethod
    def save_section(self, section: Section) -> None: ...