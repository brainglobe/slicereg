from abc import ABC, abstractmethod
from typing import List

from slicereg.core.image import Image
from slicereg.core.section import Section


class BaseSectionRepo(ABC):

    @property
    @abstractmethod
    def sections(self) -> List[Section]:  ...

    @abstractmethod
    def save_section(self, section: Section) -> None: ...


class BaseImageReader(ABC):

    def read(self, filename: str) -> Image: ...