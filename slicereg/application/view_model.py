from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, NamedTuple, Tuple

from numpy import ndarray

from slicereg.application.utils import Signal


class SectionModel(NamedTuple):
    image: ndarray
    transform: ndarray


class AtlasModel(NamedTuple):
    volume: ndarray
    transform: ndarray


@dataclass
class ViewModel:
    atlas: Optional[AtlasModel] = None
    current_section: Optional[SectionModel] = None
    current_channel: int = 1
    main_title: str = "Default Title"
    atlas_updated: Signal = Signal()
    section_loaded: Signal = Signal()

    def update_atlas(self, volume: ndarray, transform: ndarray):
        self.atlas = AtlasModel(volume=volume, transform=transform)
        self.atlas_updated.emit()

    def show_new_slice(self, image: ndarray, transform: ndarray):
        self.current_section = SectionModel(image=image, transform=transform)
        self.section_loaded.emit()
