from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

from numpy import ndarray


@dataclass(frozen=True)
class AtlasReaderData:
    source: str
    name: str
    registration_volume: ndarray
    annotation_volume: Optional[ndarray] = field(repr=False)
    resolution_um: Optional[float] = field(repr=False)


class BaseLocalAtlasReader(ABC):

    @abstractmethod
    def read(self, filename: str) -> Optional[AtlasReaderData]: ...


class BaseRemoteAtlasReader:

    @abstractmethod
    def read(self, name: str) -> Optional[AtlasReaderData]: ...

    @abstractmethod
    def list(self) -> List[str]: ...
