from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from numpy import ndarray

from src.gui.main_view import MainView
from src.workflows.load_atlas.workflow import BasePresenter as BaseLoadAtlasPresenter
from src.workflows.load_section.workflow import BasePresenter as BaseLoadSectionPresenter
from src.workflows.move_section.workflow import BasePresenter as BaseMoveSectionPresenter
from src.workflows.select_channel.workflow import BasePresenter as BaseSelectChannelPresenter


@dataclass
class LoadAtlasPresenter(BaseLoadAtlasPresenter):
    view: MainView

    def show_atlas(self, volume: ndarray, transform: ndarray) -> None:
        self.view.volume_view.view_atlas(volume=volume, transform=transform)


class LoadSectionPresenter(BaseLoadSectionPresenter):

    def __init__(self, view: MainView):
        self.view = view

    def show_section(self, image: ndarray, transform: Optional[ndarray] = None) -> None:
        self.view.volume_view.view_section(image=image, transform=transform)
        self.view.slice_view.update_slice_image(image=image)


@dataclass
class MoveSectionPresenter(BaseMoveSectionPresenter):
    view: MainView

    def update_transform(self, transform: ndarray):
        self.view.volume_view.update_transform(transform=transform)

    def show_error(self, msg: str):
        self.view.show_temp_title(title=msg)


@dataclass
class SelectChannelPresenter(BaseSelectChannelPresenter):
    view: MainView

    def update_section_image(self, image: ndarray):
        self.view.volume_view.update_image(image=image)
        self.view.slice_view.update_slice_image(image=image)

    def show_error(self, msg: str):
        self.view.show_temp_title(title=msg)