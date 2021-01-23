from __future__ import annotations

from dataclasses import dataclass, field

from numpy import ndarray

from slicereg.commands.load_atlas import BaseLoadAtlasPresenter
from slicereg.commands.load_section import BaseLoadSectionPresenter
from slicereg.commands.move_section import BaseMoveSectionPresenter
from slicereg.commands.select_channel import BaseSelectChannelPresenter
from slicereg.gui.utils import Signal


@dataclass
class LoadAtlasPresenter(BaseLoadAtlasPresenter):
    atlas_updated: Signal = field(default_factory=Signal)

    def show(self, reference_volume: ndarray, atlas_transform: ndarray, atlas_resolution: int) -> None:
        self.atlas_updated.emit(volume=reference_volume, transform=atlas_transform)


@dataclass
class LoadSectionPresenter(BaseLoadSectionPresenter):
    section_loaded: Signal = field(default_factory=Signal)

    def show(self, section: ndarray, model_matrix: ndarray):
        self.section_loaded.emit(image=section, transform=model_matrix)


@dataclass
class MoveSectionPresenter(BaseMoveSectionPresenter):
    section_moved: Signal = Signal()

    def show(self, transform: ndarray):
        self.section_moved.emit(transform=transform)


@dataclass
class SelectChannelPresenter(BaseSelectChannelPresenter):
    channel_changed: Signal = Signal()

    def show(self, channel: int, image: ndarray):
        self.channel_changed.emit(image=image, channel=channel)
