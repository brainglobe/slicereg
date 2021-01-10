from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray

from src.workflows.load_section.load_section import LoadSectionWorkflow
from src.workflows.move_section import MoveSectionWorkflow
from src.workflows.select_channel import SelectChannelWorkflow


class BaseView(ABC):

    @abstractmethod
    def update_transform(self, transform: ndarray) -> None: ...

    @abstractmethod
    def show_error(self, msg: str) -> None: ...

    @abstractmethod
    def update_section_image(self, image: ndarray) -> None: ...



@dataclass
class Controller:
    view: BaseView
    load_section: LoadSectionWorkflow
    _select_channel: SelectChannelWorkflow
    _move_section: MoveSectionWorkflow

    def move_section(self, x=0., y=0., z=0., rx=0., ry=0., rz=0.) -> None:
        result = self._move_section(x=x, y=y, z=z, rx=rx, ry=ry, rz=rz)
        if result.is_ok():
            data = result.value
            self.view.update_transform(transform=data.transform)
        else:
            msg = result.value
            self.view.show_error(msg)

    def select_channel(self, num: int) -> None:
        result = self._select_channel(num=num)
        if result.is_ok():
            data = result.value
            self.view.update_section_image(image=data.section_image)
        else:
            self.view.show_error(result.value)



