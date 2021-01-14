from __future__ import annotations

from dataclasses import dataclass

from numpy import ndarray

from slicereg.application.load_atlas.workflow import BaseLoadAtlasPresenter as BaseLoadAtlasPresenter, LoadAtlasModel
from slicereg.application.load_section.workflow import BaseSelectChannelPresenter as BaseLoadSectionPresenter, \
    LoadSectionResponse
from slicereg.application.move_section.workflow import BaseMoveSectionPresenter
from slicereg.application.select_channel.workflow import BasePresenter as BaseSelectChannelPresenter
from slicereg.application.view_model import ViewModel


@dataclass
class LoadAtlasPresenter(BaseLoadAtlasPresenter):
    view_model: ViewModel

    def show(self, data: LoadAtlasModel) -> None:
        self.view_model.update_atlas(volume=data.reference_volume, transform=data.atlas_transform)


@dataclass
class LoadSectionPresenter(BaseLoadSectionPresenter):
    view_model: ViewModel

    def show(self, data: LoadSectionResponse):
        self.view_model.show_new_slice(image=data.section, transform=data.model_matrix)


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