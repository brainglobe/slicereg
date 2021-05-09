from dataclasses import dataclass, field
from typing import Tuple, Optional

import numpy as np
from numpy import ndarray

from slicereg.commands.utils import Signal
from slicereg.gui.app_model import AppModel


@dataclass
class AtlasSectionDTO:
    section_image: Optional[ndarray] = None
    coords: Optional[Tuple[int, int]] = None


@dataclass(unsafe_hash=True)
class AtlasSectionViewModel:
    axis: int
    _model: AppModel = field(hash=False)
    updated: Signal = field(default_factory=Signal)

    def __post_init__(self):
        self._model.updated.connect(self.update)

    def update(self, **kwargs):
        print(self.__class__.__name__, f"updated {kwargs.keys()}")
        updates = AtlasSectionDTO()
        if 'atlas_volume' in kwargs or 'atlas_section_coords' in kwargs:
            updates.section_image = self.section_image
        if 'atlas_section_coords' in kwargs:
            updates.coords = tuple(np.delete(kwargs['atlas_section_coords'], self.axis))
        self.updated.emit(dto=updates)

    @property
    def section_image(self):
        if (volume := self._model.atlas_volume) is not None:
            section_slice_idx = self._model.atlas_section_coords[self.axis]
            return np.rollaxis(volume, self.axis)[section_slice_idx]
        else:
            return None

    def on_left_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        visible_axes = np.delete(np.arange(3), self.axis)
        coords = np.array(self._model.atlas_section_coords)
        coords[visible_axes[0]] = int(np.clip(y2, 0, self._model.atlas_volume.shape[visible_axes[0]] - 1))
        coords[visible_axes[1]] = int(np.clip(x2, 0, self._model.atlas_volume.shape[visible_axes[1]] - 1))
        x, y, z = coords
        self._model.atlas_section_coords = x, y, z

    @property
    def axis_colors(self):
        colors = [(1., 0., 0., 1.),
                  (0., 1., 0., 1.),
                  (0., 0., 1., 1.)]
        visible_axes = np.delete(np.arange(3), self.axis)
        return tuple(np.array(colors)[visible_axes])
