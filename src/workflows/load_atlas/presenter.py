from __future__ import annotations

from dataclasses import dataclass

from numpy import ndarray

from src.gui.window import Window
from src.workflows.load_atlas.load_atlas import BasePresenter


@dataclass
class GuiPresenter(BasePresenter):
    win: Window

    def show_atlas(self, volume: ndarray, transform: ndarray) -> None:
        self.win.volume_view.view_atlas(volume=volume, transform=transform)