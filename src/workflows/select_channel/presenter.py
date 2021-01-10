from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray
from result import Result

from src.workflows.select_channel.select_channel import BasePresenter, SectionChannelData


@dataclass
class GuiPresenter(BasePresenter):
    view: BaseView

    def present(self, result: Result[SectionChannelData, str]) -> None:
        if result.is_ok():
            data = result.value
            self.view.update_section_image(image=data.section_image)
        else:
            self.view.show_error(result.value)


class BaseView(ABC):

    @abstractmethod
    def update_section_image(self, image: ndarray): ...

    @abstractmethod
    def show_error(self, msg: str): ...
