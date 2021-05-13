from dataclasses import dataclass, field
from typing import Tuple

import numpy as np

from slicereg.app.app_model import AppModel
from slicereg.utils.signal import Signal


@dataclass(unsafe_hash=True)
class AtlasSectionViewModel:
    axis: int
    _model: AppModel = field(hash=False)
    updated: Signal = field(default_factory=Signal)
    atlas_section_image: np.ndarray = np.zeros(shape=(3, 3), dtype=np.uint16)
    coords: Tuple[int, int] = (0, 0)

    def __post_init__(self):
        self._model.updated.connect(self.update)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if hasattr(self, 'updated'):
            self.updated.emit(changed=key)

    def update(self, changed: str):
        if changed == 'atlas_volume':
            self._update_section_image()
        elif changed == 'atlas_section_coords':
            self._update_coords()

    def _update_coords(self):
        self.coords = tuple(np.delete(self._model.atlas_section_coords, self.axis))

    def _update_section_image(self):
        if (volume := self._model.atlas_volume) is not None:
            section_slice_idx = self._model.atlas_section_coords[self.axis]
            return np.rollaxis(volume, self.axis)[section_slice_idx]
        else:
            return None

    @property
    def axis_colors(self):
        colors = [(1., 0., 0., 1.),
                  (0., 1., 0., 1.),
                  (0., 0., 1., 1.)]
        visible_axes = np.delete(np.arange(3), self.axis)
        return tuple(np.array(colors)[visible_axes])

    def on_left_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        visible_axes = np.delete(np.arange(3), self.axis)
        coords = np.array(self._model.atlas_section_coords)
        coords[visible_axes[0]] = int(np.clip(y2, 0, self._model.atlas_volume.shape[visible_axes[0]] - 1))
        coords[visible_axes[1]] = int(np.clip(x2, 0, self._model.atlas_volume.shape[visible_axes[1]] - 1))
        x, y, z = coords
        self._model.atlas_section_coords = x, y, z
