from dataclasses import dataclass

from numpy import ndarray

from src.gui.window import Window
from src.workflows.load_atlas.presenter import BaseView


@dataclass
class GuiView(BaseView):
    win: Window

    def show_atlas(self, volume: ndarray, transform: ndarray) -> None:
        self.win.volume_view.view_atlas(volume=volume, transform=transform)

    def show_error(self, msg: str) -> None:
        self.win.show_temp_title(title=msg)
