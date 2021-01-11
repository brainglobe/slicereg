from typing import Optional

from numpy import ndarray

from src.gui.window import Window
from src.workflows.load_section.load_section import BasePresenter


class GuiPresenter(BasePresenter):

    def __init__(self, win: Window):
        self.win = win

    def show_section(self, image: ndarray, transform: Optional[ndarray] = None) -> None:
        self.win.volume_view.view_section(image=image, transform=transform)
        self.win.slice_view.update_slice_image(image=image)
