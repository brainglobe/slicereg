from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

from numpy import ndarray


@dataclass(frozen=True)
class LocalAtlasReaderData:
    source: str
    name: str
    registration_volume: ndarray


class BaseLocalAtlasReader(ABC):

    @abstractmethod
    def read(self, filename: str) -> Optional[LocalAtlasReaderData]: ...


@dataclass(frozen=True)
class RemoteAtlasReaderData:
    source: str
    name: str
    registration_volume: ndarray
    annotation_volume: ndarray = field(repr=False)
    resolution_um: float = field(repr=False)


class BaseRemoteAtlasReader:

    @abstractmethod
    def read(self, name: str) -> Optional[RemoteAtlasReaderData]: ...

    @abstractmethod
    def list(self) -> List[str]: ...
