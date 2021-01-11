from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray
from numpy.core._multiarray_umath import ndarray
from result import Result

from src.gui.window import Window
from src.workflows.load_atlas.load_atlas import BasePresenter, AtlasData


@dataclass
class GuiPresenter(BasePresenter):
    view: BaseView

    def present(self, result: Result[AtlasData, str]):
        if result.is_ok():
            data = result.value
            self.view.show_atlas(volume=data.atlas_volume, transform=data.atlas_transform)
        else:
            self.view.show_error(msg=result.value)


class BaseView(ABC):

    @abstractmethod
    def show_atlas(self, volume: ndarray, transform: ndarray) -> None: ...

    @abstractmethod
    def show_error(self, msg: str) -> None: ...


@dataclass
class GuiView(BaseView):
    win: Window

    def show_atlas(self, volume: ndarray, transform: ndarray) -> None:
        self.win.volume_view.view_atlas(volume=volume, transform=transform)

    def show_error(self, msg: str) -> None:
        self.win.show_temp_title(title=msg)