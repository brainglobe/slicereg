from abc import ABC, abstractmethod
from abc import ABC, abstractmethod
from typing import Optional, List

from slicereg.models.atlas import Atlas


class BaseAtlasRepo(ABC):

    @abstractmethod
    def get_atlas(self) -> Optional[Atlas]: ...

    @abstractmethod
    def set_atlas(self, atlas: Atlas) -> None: ...


class AtlasRepo(BaseAtlasRepo):

    def __init__(self):
        self._atlas: Optional[Atlas] = None

    def get_atlas(self) -> Optional[Atlas]:
        return self._atlas

    def set_atlas(self, atlas: Atlas) -> None:
        self._atlas = atlas
