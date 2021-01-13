from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from numpy import ndarray

from slicereg.gui.window import MainWindow
from slicereg.workflows.load_atlas.workflow import BasePresenter as BaseLoadAtlasPresenter
from slicereg.workflows.load_section.workflow import BasePresenter as BaseLoadSectionPresenter, LoadSectionResponse
from slicereg.workflows.move_section.workflow import BasePresenter as BaseMoveSectionPresenter
from slicereg.workflows.select_channel.workflow import BasePresenter as BaseSelectChannelPresenter


@dataclass
class LoadAtlasPresenter(BaseLoadAtlasPresenter):
    view: MainWindow

    def show_atlas(self, volume: ndarray, transform: ndarray) -> None:
        self.view.volume_view.view_atlas(volume=volume, transform=transform)


class LoadSectionPresenter(BaseLoadSectionPresenter):

    def __init__(self, view: MainWindow):
        self.view = view

    def show(self, data: LoadSectionResponse):
        self.view.volume_view.view_section(image=data.section, transform=data.model_matrix)
        self.view.slice_view.update_slice_image(image=data.section)


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