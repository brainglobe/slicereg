from dataclasses import dataclass, field
from typing import Tuple, Optional

from numpy import ndarray

from slicereg.commands.utils import Signal
from slicereg.gui.app_model import AppModel


@dataclass
class SliceViewDTO:
    section_image: Optional[ndarray] = None
    atlas_image: Optional[ndarray] = None
    clim: Optional[Tuple[int, int]] = None


@dataclass(unsafe_hash=True)
class SliceViewModel:
    _model: AppModel = field(hash=False)
    updated: Signal = field(default_factory=Signal)

    def __post_init__(self):
        self._model.updated.connect(self.update)

    def update(self, **kwargs):
        print(self.__class__.__name__, f"updated {kwargs.keys()}")
        updates = SliceViewDTO()
        if 'atlas_image' in kwargs:
            updates.atlas_image = kwargs['atlas_image']
        if 'section_image' in kwargs:
            updates.section_image = kwargs['section_image']
            updates.clim = self._model.clim_2d_values
        if 'clim_2d' in kwargs:
            updates.clim = self._model.clim_2d_values
        self.updated.emit(dto=updates)

    def on_left_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        scale = 4.
        scaled_dx = (x2 - x1) * scale
        scaled_dy = (y2 - y1) * scale
        self._model.move_section(x=scaled_dx, z=scaled_dy)
        self._model.get_coord(i=x2, j=y2)

    def on_right_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        scale = 1.
        scaled_dx = (x2 - x1) * scale
        scaled_dy = (y2 - y1) * scale
        self._model.move_section(rx=scaled_dx, rz=scaled_dy)

    def on_mousewheel_move(self, increment: int):
        scale = 10
        self._model.move_section(y=scale * increment)
