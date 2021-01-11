from dataclasses import dataclass

from numpy.core._multiarray_umath import ndarray

from src.gui.main_view import MainView
from src.workflows.move_section.workflow import BasePresenter


@dataclass
class MoveSectionPresenter(BasePresenter):
    view: MainView

    def update_transform(self, transform: ndarray):
        self.view.volume_view.update_transform(transform=transform)

    def show_error(self, msg: str):
        self.view.show_temp_title(title=msg)
