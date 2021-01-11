from typing import Optional

from numpy import ndarray

from src.gui.main_view import MainView
from src.workflows.load_section.workflow import BasePresenter


class LoadSectionPresenter(BasePresenter):

    def __init__(self, view: MainView):
        self.view = view

    def show_section(self, image: ndarray, transform: Optional[ndarray] = None) -> None:
        self.view.volume_view.view_section(image=image, transform=transform)
        self.view.slice_view.update_slice_image(image=image)
