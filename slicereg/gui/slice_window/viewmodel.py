from dataclasses import dataclass, field
from typing import Tuple

import numpy as np

from slicereg.commands.constants import Direction, Axis
from slicereg.commands.update_section import Translate, Rotate
from slicereg.gui.app_model import AppModel
from slicereg.utils.observable import HasObservableAttributes


@dataclass(unsafe_hash=True)
class SliceViewModel(HasObservableAttributes):
    _model: AppModel = field(hash=False)
    atlas_image: np.ndarray = np.zeros(shape=(3, 3), dtype=np.uint16)
    section_image: np.ndarray = np.zeros(shape=(3, 3), dtype=np.uint16)
    clim: Tuple[int, int] = (0, 2)

    def __post_init__(self):
        HasObservableAttributes.__init__(self)
        self._model.register(self.update)

    def update(self, changed: str):
        if changed == 'atlas_image' and self._model.atlas_image is not None:
            self.atlas_image = self._model.atlas_image
        if changed == 'section_image' and self._model.section_image is not None:
            self.section_image = self._model.section_image
            self.clim = self._model.clim_2d_values
        if changed == 'clim_2d':
            self.clim = self._model.clim_2d_values

    def on_left_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        scale = 4.
        scaled_dx = (x2 - x1) * scale
        scaled_dy = (y2 - y1) * scale
        self._model.update_section(Translate(direction=Direction.Right, value=scaled_dx))
        self._model.update_section(Translate(direction=Direction.Superior, value=scaled_dy))

    def on_mouse_move(self, x: int, y: int):
        self._model.select_coord(i=x, j=y)

    def on_right_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        scale = 1.
        scaled_dx = (x2 - x1) * scale
        scaled_dy = (y2 - y1) * scale
        self._model.update_section(Rotate(axis=Axis.Longitudinal, value=scaled_dx))
        self._model.update_section(Rotate(axis=Axis.Horizontal, value=scaled_dy))

    def on_mousewheel_move(self, increment: int):
        scale = 10
        self._model.update_section(Translate(direction=Direction.Anterior, value=scale * increment))
