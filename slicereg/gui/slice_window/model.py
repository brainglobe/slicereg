from dataclasses import dataclass, field
from typing import Tuple, Callable

import numpy as np

from slicereg.app.app_model import AppModel
from slicereg.utils.signal import Signal


@dataclass(unsafe_hash=True)
class SliceViewModel:
    _model: AppModel = field(hash=False)
    updated: Signal = field(default_factory=Signal)
    atlas_image: np.ndarray = np.zeros(shape=(3, 3), dtype=np.uint16)
    section_image: np.ndarray = np.zeros(shape=(3, 3), dtype=np.uint16)
    clim: Tuple[int, int] = (0, 2)

    def __post_init__(self):
        self._model.register(self.update)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if hasattr(self, 'updated'):
            self.updated.emit(changed=key)

    def register(self, fun: Callable[[str], None]):
        """Takes a callback function that gets called with the name of the changed argument."""
        self.updated.connect(fun)

    def update(self, changed: str):
        if changed == 'atlas_image':
            self.atlas_image = self._model.atlas_image
        if changed == 'section_image':
            self.section_image = self._model.section_image
            self.clim = self._model.clim_2d_values
        if changed == 'clim_2d':
            self.clim = self._model.clim_2d_values

    def on_left_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        scale = 4.
        scaled_dx = (x2 - x1) * scale
        scaled_dy = (y2 - y1) * scale
        self._model.move_section(x=scaled_dx, z=scaled_dy)

    def on_mouse_move(self, x: int, y: int):
        self._model.select_coord(i=x, j=y)

    def on_right_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        scale = 1.
        scaled_dx = (x2 - x1) * scale
        scaled_dy = (y2 - y1) * scale
        self._model.move_section(rx=scaled_dx, rz=scaled_dy)

    def on_mousewheel_move(self, increment: int):
        scale = 10
        self._model.move_section(y=scale * increment)
