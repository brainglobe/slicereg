from typing import Optional

from src.core.atlas.load_atlas import BaseAtlasRepo
from src.core.atlas.models import Atlas
from src.serializers.bg_atlas import BGAtlasSerializer


class InMemoryAtlasRepo(BaseAtlasRepo):

    def __init__(self):
        self._current_atlas: Optional[Atlas] = None

    def get_atlas(self, resolution_um: int) -> Atlas:
        if self._current_atlas is None or self._current_atlas.resolution_um != resolution_um:
            self._current_atlas = BGAtlasSerializer().read(resolution_um=resolution_um)
        return self._current_atlas

    def get_current_atlas(self) -> Atlas:
        return self._current_atlas

