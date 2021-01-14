from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, NamedTuple, Tuple, List

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
    errors: List[str] = field(default_factory=list)
    atlas_updated: Signal = Signal()
    section_loaded: Signal = Signal()
    section_moved: Signal = Signal()
    error_raised: Signal = Signal()

    def update_atlas(self, volume: ndarray, transform: ndarray):
        self.atlas = AtlasModel(volume=volume, transform=transform)
        self.atlas_updated.emit()

    def show_new_slice(self, image: ndarray, transform: ndarray):
        self.current_section = SectionModel(image=image, transform=transform)
        self.section_loaded.emit()

    def update_section_transform(self, transform: ndarray):
        self.current_section = self.current_section._replace(transform=transform)
        self.section_moved.emit()

    def show_error(self, msg: str):
        self.errors.append(msg)
        self.error_raised.emit()