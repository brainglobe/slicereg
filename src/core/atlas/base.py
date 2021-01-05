from abc import ABC, abstractmethod

from src.core.atlas.models import Atlas


class BaseAtlasSerializer(ABC):

    @abstractmethod
    def read(self, *args, **kwargs) -> Atlas: ...

