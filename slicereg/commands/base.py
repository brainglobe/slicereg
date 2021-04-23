from abc import ABC, abstractmethod
from typing import List

from slicereg.models.image import Image
from slicereg.models.section import Section


class BaseSectionRepo(ABC):

    @property
    @abstractmethod
    def sections(self) -> List[Section]:  ...

    @abstractmethod
    def save_section(self, section: Section) -> None: ...


class BaseImageReader(ABC):

    def read(self, filename: str) -> Image: ...