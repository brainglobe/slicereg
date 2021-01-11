from __future__ import annotations

from dataclasses import dataclass

from numpy import ndarray

from src.gui.main_view import MainView
from src.workflows.load_atlas.workflow import BasePresenter


@dataclass
class LoadAtlasPresenter(BasePresenter):
    view: MainView

    def show_atlas(self, volume: ndarray, transform: ndarray) -> None:
        self.view.volume_view.view_atlas(volume=volume, transform=transform)