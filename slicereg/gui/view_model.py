from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, NamedTuple, List

from numpy import ndarray

from slicereg.commands.load_atlas import BaseLoadAtlasPresenter
from slicereg.commands.load_section import BaseLoadSectionPresenter
from slicereg.commands.move_section import BaseMoveSectionPresenter
from slicereg.commands.select_channel import BaseSelectChannelPresenter

from slicereg.gui.utils import Signal


class SectionModel(NamedTuple):
    image: ndarray
    transform: ndarray


class AtlasModel(NamedTuple):
    volume: ndarray
    transform: ndarray
    resolution: int


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
    channel_changed: Signal = Signal()


@dataclass
class LoadAtlasPresenter(BaseLoadAtlasPresenter):
    view_model: ViewModel

    def show(self, reference_volume: ndarray, atlas_transform: ndarray, atlas_resolution: int) -> None:
        self.view_model.atlas = AtlasModel(volume=reference_volume, transform=atlas_transform,
                                           resolution=atlas_resolution)
        self.view_model.atlas_updated.emit()


@dataclass
class LoadSectionPresenter(BaseLoadSectionPresenter):
    view_model: ViewModel

    def show(self, section: ndarray, model_matrix: ndarray):
        self.view_model.current_section = SectionModel(image=section, transform=model_matrix)
        self.view_model.section_loaded.emit()


@dataclass
class MoveSectionPresenter(BaseMoveSectionPresenter):
    view_model: ViewModel

    def show(self, transform: ndarray):
        self.view_model.current_section = self.view_model.current_section._replace(transform=transform)
        self.view_model.section_moved.emit()

    def show_error(self, msg: str):
        self.view_model.errors.append(msg)
        self.view_model.error_raised.emit()


@dataclass
class SelectChannelPresenter(BaseSelectChannelPresenter):
    view_model: ViewModel

    def show(self, channel: int, image: ndarray):
        model = self.view_model
        model.current_section = model.current_section._replace(image=image)
        model.current_channel = channel
        model.channel_changed.emit()

    def show_error(self, msg: str):
        self.view_model.errors.append(msg)
        self.view_model.error_raised.emit()
