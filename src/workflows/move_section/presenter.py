from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray
from result import Result

from src.workflows.move_section.move_section import BasePresenter, SectionTransformData


@dataclass
class GuiPresenter(BasePresenter):
    view: BaseView

    def present(self, result: Result[SectionTransformData, str]):
        if result.is_ok():
            result = result.value
            self.view.update_transform(transform=result.transform)
        else:
            msg = result.value
            self.view.show_error(msg)


class BaseView(ABC):

    @abstractmethod
    def update_transform(self, transform: ndarray): ...

    @abstractmethod
    def show_error(self, msg: str): ...
