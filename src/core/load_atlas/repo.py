from abc import ABC, abstractmethod
from typing import Optional

from src.core.load_atlas.load_atlas import BaseRepo
from src.core.models.atlas import Atlas


class BaseAtlasSerializer(ABC):

    @abstractmethod
    def read(self, resolution_um: int) -> Atlas: ...


class AtlasRepo(BaseRepo):
    _atlas: Optional[Atlas] = None

    def __init__(self, serializer: BaseAtlasSerializer):
        self._serializer = serializer

    def load_atlas(self, resolution: int) -> Atlas:
        return self._serializer.read(resolution_um=resolution)

    def set_atlas(self, atlas: Atlas) -> None:
        self._atlas = atlas
