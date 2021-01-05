from typing import Optional

from src.core.atlas.load_atlas import BaseAtlasRepo
from src.core.atlas.models import Atlas
from src.serializers.bg_atlas import BGAtlasSerializer
from src.core.section.base import BaseSectionRepo
from src.core.section.models import Section


class InMemoryRepo(BaseAtlasRepo, BaseSectionRepo):

    def __init__(self):
        self._current_atlas: Optional[Atlas] = None
        self._section: Optional[Section] = None

    def get_atlas(self, resolution_um: int) -> Atlas:
        if self._current_atlas is None or self._current_atlas.resolution_um != resolution_um:
            self._current_atlas = BGAtlasSerializer().read(resolution_um=resolution_um)
        return self._current_atlas

    def get_current_atlas(self) -> Atlas:
        return self._current_atlas

    def get_section(self) -> Optional[Section]:
        return self._section

    def save_section(self, section: Section) -> None:
        self._section = section
