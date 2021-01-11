from dataclasses import dataclass

from numpy import ndarray

from src.gui.window import Window
from src.workflows.select_channel.workflow import BasePresenter


@dataclass
class GuiView(BasePresenter):
    win: Window

    def update_section_image(self, image: ndarray):
        self.win.volume_view.update_image(image=image)
        self.win.slice_view.update_slice_image(image=image)

    def show_error(self, msg: str):
        self.win.show_temp_title(title=msg)