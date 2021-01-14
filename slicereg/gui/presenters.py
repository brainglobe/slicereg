from __future__ import annotations

from dataclasses import dataclass

from numpy import ndarray

from slicereg.commands.load_atlas import BaseLoadAtlasPresenter
from slicereg.commands.load_section import BaseLoadSectionPresenter
from slicereg.commands.move_section import BaseMoveSectionPresenter
from slicereg.commands.select_channel import BaseSelectChannelPresenter
from slicereg.gui.view_model import ViewModel


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