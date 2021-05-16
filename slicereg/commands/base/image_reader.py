from abc import ABC, abstractmethod
from typing import NamedTuple, Optional

from numpy import ndarray


class ImageReaderData(NamedTuple):
    channels: ndarray
    resolution_um: Optional[float]


class BaseLocalImageReader(ABC):

    @abstractmethod
    def read(self, filename: str) -> ImageReaderData: ...