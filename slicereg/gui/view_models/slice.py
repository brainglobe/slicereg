from dataclasses import dataclass, field
from typing import Tuple, Optional

from numpy import ndarray

from slicereg.commands.utils import Signal
from slicereg.gui.app_model import AppModel


@dataclass(unsafe_hash=True)
class SliceViewModel:
    _model: AppModel = field(hash=False)
    updated: Signal = field(default_factory=Signal)

    def __post_init__(self):
        self._model.updated.connect(self.update)

    def update(self, **kwargs):
        print(self.__class__.__name__, f"updated {kwargs}")
        if kwargs.get('_section_image') is not None:
            kwargs['clim'] = self._model.clim_2d_values
        if kwargs.get('clim_2d') is not None:
            kwargs['clim'] = self._model.clim_2d_values
        self.updated.emit(**kwargs)

    @property
    def clim(self) -> Tuple[float, float]:
        return self._model.clim_2d

    @clim.setter
    def clim(self, val):
        self._model.clim_2d = val

    @property
    def section_image(self) -> Optional[ndarray]:
        return self._model._section_image

    @property
    def atlas_image(self) -> Optional[ndarray]:
        return self._model._atlas_image

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
