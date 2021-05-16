from abc import ABC, abstractmethod
from typing import List, Optional, NamedTuple

from numpy import ndarray

from slicereg.core.atlas import Atlas
from slicereg.core.section import Section


class ImageReaderData(NamedTuple):
    channels: ndarray
    resolution_um: Optional[float]


class BaseLocalImageReader(ABC):

    @abstractmethod
    def read(self, filename: str) -> ImageReaderData: ...


class BaseLocalAtlasReader(ABC):

    @abstractmethod
    def read(self, filename: str, resolution_um: float) -> Atlas: ...


class BaseRemoteAtlasReader:

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def read(self, name: str) -> Atlas: ...

    @abstractmethod
    def list(self) -> List[str]: ...


class BaseRepo(ABC):

    @abstractmethod
    def get_sections(self) -> List[Section]: ...

    @abstractmethod
    def save_section(self, section: Section): ...

    @abstractmethod
    def get_atlas(self) -> Optional[Atlas]: ...

    @abstractmethod
    def set_atlas(self, atlas: Atlas) -> None: ...
