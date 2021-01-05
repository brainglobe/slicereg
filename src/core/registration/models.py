from dataclasses import dataclass
from warnings import warn

from numpy import ndarray

from src.core.atlas.models import Atlas
from src.core.section.models import Section


@dataclass
class RegisteredSection:
    section: Section
    atlas: Atlas

    def slice_atlas(self) -> ndarray:
        warn("Atlas Slicing not correctly implemented, don't rely on this result!")
        return self.atlas.volume[20]
