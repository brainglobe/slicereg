from typing import Optional

from src.core.atlas.load_atlas import BaseAtlasRepo
from src.core.atlas.models import Atlas
from src.serializers.bg_atlas import BGAtlasSerializer
from src.core.section.base import BaseSectionRepo
from src.core.section.models import Section


class InMemoryRepo(BaseAtlasRepo, BaseSectionRepo):

    def __init__(self):
        self._atlas: Optional[Atlas] = None
        self._section: Optional[Section] = None

    def get_atlas(self) -> Optional[Atlas]:
        return self._atlas

    def set_atlas(self, atlas: Atlas) -> None:
        self._atlas = atlas

    def get_section(self) -> Optional[Section]:
        return self._section

    def save_section(self, section: Section) -> None:
        self._section = section
