from __future__ import annotations

from dataclasses import dataclass

from src.workflows.load_atlas import LoadAtlasWorkflow
from src.workflows.load_section.load_section import LoadSectionWorkflow
from src.workflows.move_section import MoveSectionWorkflow
from src.workflows.select_channel import SelectChannelWorkflow


@dataclass
class ViewModel:
    win: Window
    _load_atlas: LoadAtlasWorkflow
    load_section: LoadSectionWorkflow
    _select_channel: SelectChannelWorkflow
    _move_section: MoveSectionWorkflow

    def move_section(self, x=0., y=0., z=0., rx=0., ry=0., rz=0.) -> None:
        result = self._move_section(x=x, y=y, z=z, rx=rx, ry=ry, rz=rz)
        if result.is_ok():
            data = result.value
            self.win.volume_view.update_transform(transform=data.transform)
        else:
            msg = result.value
            self.win.show_temp_title(msg)

    def select_channel(self, num: int) -> None:
        result = self._select_channel(num=num)
        if result.is_ok():
            data = result.value
            self.win.volume_view.update_image(image=data.section_image)
            self.win.slice_view.update_slice_image(image=data.section_image)
        else:
            self.win.show_temp_title(result.value)

    def load_atlas(self, resolution: int) -> None:
        result = self._load_atlas(resolution=resolution)
        if result.is_ok():
            data = result.value
            self.win.volume_view.view_atlas(volume=data.atlas_volume, transform=data.atlas_transform)
        else:
            self.win.show_temp_title(result.value)