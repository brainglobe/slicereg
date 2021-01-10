from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray

from src.workflows.load_atlas.load_atlas import LoadAtlasWorkflow
from src.workflows.load_section.load_section import LoadSectionWorkflow
from src.workflows.move_section.move_section import MoveSectionWorkflow
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
    load_atlas: LoadAtlasWorkflow
    load_section: LoadSectionWorkflow
    _select_channel: SelectChannelWorkflow
    move_section: MoveSectionWorkflow

    def select_channel(self, num: int) -> None:
        result = self._select_channel(num=num)
        if result.is_ok():
            data = result.value
            self.view.update_section_image(image=data.section_image)
        else:
            self.view.show_error(result.value)



