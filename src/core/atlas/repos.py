from typing import Optional

from src.core.atlas.load_atlas import BaseAtlasRepo
from src.core.atlas.models import Atlas


class AtlasRepo(BaseAtlasRepo):

    def __init__(self):
        self._atlas: Optional[Atlas] = None

    def get_atlas(self) -> Optional[Atlas]:
        return self._atlas

    def set_atlas(self, atlas: Atlas) -> None:
        self._atlas = atlas
