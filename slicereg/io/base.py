from abc import ABC, abstractmethod

from slicereg.models.section import Section


class BaseSectionReader(ABC):

    @abstractmethod
    def read(self, filename: str) -> Section: ...
