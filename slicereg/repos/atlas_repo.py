from abc import ABC, abstractmethod
from typing import Optional

from slicereg.models.atlas import Atlas


class AtlasRepo:

    def __init__(self):
        self._atlas: Optional[Atlas] = None

    def get_atlas(self) -> Optional[Atlas]:
        return self._atlas

    def set_atlas(self, atlas: Atlas) -> None:
        self._atlas = atlas
