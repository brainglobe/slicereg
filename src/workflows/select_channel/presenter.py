from dataclasses import dataclass

from numpy import ndarray

from src.gui.main_view import MainView
from src.workflows.select_channel.workflow import BasePresenter


@dataclass
class SelectChannelPresenter(BasePresenter):
    view: MainView

    def update_section_image(self, image: ndarray):
        self.view.volume_view.update_image(image=image)
        self.view.slice_view.update_slice_image(image=image)

    def show_error(self, msg: str):
        self.view.show_temp_title(title=msg)