from abc import ABC, abstractmethod
from typing import List

from slicereg.core.atlas import Atlas


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