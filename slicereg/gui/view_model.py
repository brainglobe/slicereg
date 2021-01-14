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

    def change_channel(self, channel: int, image: ndarray):
        self.current_section = self.current_section._replace(image=image)
        self.current_channel = channel

        self.channel_changed.emit()


@dataclass
class LoadAtlasPresenter(BaseLoadAtlasPresenter):
    view_model: ViewModel

    def show(self, reference_volume: ndarray, atlas_transform: ndarray,  atlas_resolution: ndarray) -> None:
        self.view_model.update_atlas(volume=reference_volume, transform=atlas_transform)


@dataclass
class LoadSectionPresenter(BaseLoadSectionPresenter):
    view_model: ViewModel

    def show(self, section: ndarray, model_matrix: ndarray):
        self.view_model.show_new_slice(image=section, transform=model_matrix)


@dataclass
class MoveSectionPresenter(BaseMoveSectionPresenter):
    view_model: ViewModel

    def show(self, transform: ndarray):
        self.view_model.update_section_transform(transform=transform)

    def show_error(self, msg: str):
        self.view_model.show_error(msg=msg)


@dataclass
class SelectChannelPresenter(BaseSelectChannelPresenter):
    view_model: ViewModel

    def show(self, channel: int, image: ndarray):
        self.view_model.change_channel(channel=channel, image=image)

    def show_error(self, msg: str):
        self.view.show_temp_title(title=msg)