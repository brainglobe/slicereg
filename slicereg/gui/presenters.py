from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from numpy import ndarray

from slicereg.application.view_model import ViewModel
from slicereg.gui.window import MainWindow
from slicereg.application.load_atlas.workflow import BaseLoadAtlasPresenter as BaseLoadAtlasPresenter, LoadAtlasModel
from slicereg.application.load_section.workflow import BasePresenter as BaseLoadSectionPresenter, LoadSectionResponse
from slicereg.application.move_section.workflow import BasePresenter as BaseMoveSectionPresenter
from slicereg.application.select_channel.workflow import BasePresenter as BaseSelectChannelPresenter


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

        # self.view.volume_view.view_section(image=data.section, transform=data.model_matrix)
        # self.view.slice_view.update_slice_image(image=data.section)


@dataclass
class MoveSectionPresenter(BaseMoveSectionPresenter):
    view: MainWindow

    def update_transform(self, transform: ndarray):
        self.view.volume_view.update_transform(transform=transform)

    def show_error(self, msg: str):
        self.view.show_temp_title(title=msg)


@dataclass
class SelectChannelPresenter(BaseSelectChannelPresenter):
    view: MainWindow

    def update_section_image(self, image: ndarray):
        self.view.volume_view.update_image(image=image)
        self.view.slice_view.update_slice_image(image=image)

    def show_error(self, msg: str):
        self.view.show_temp_title(title=msg)