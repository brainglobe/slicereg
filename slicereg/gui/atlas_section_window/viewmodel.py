from dataclasses import dataclass, field
from typing import Tuple

import numpy as np

from slicereg.gui.app_model import AppModel
from slicereg.utils.observable import HasObservableAttributes


@dataclass(unsafe_hash=True)
class AtlasSectionViewModel(HasObservableAttributes):
    _model: AppModel = field(hash=False)
    plane: str = 'coronal'
    _axis: int = 0
    atlas_section_image: np.ndarray = np.zeros(shape=(3, 3), dtype=np.uint16)
    coords: Tuple[int, int] = (0, 0)
    image_coords: Tuple[int, int] = (0, 0)
    depth: float = 0.

    def __post_init__(self):
        HasObservableAttributes.__init__(self)
        self._model.register(self.update)

    def update(self, changed: str):
        update_funs = {
            'registration_volume': self._update_section_image,
            'atlas_section_coords': self._update_coords,
            'x': self._update_depth_and_coords,
            'y': self._update_depth_and_coords,
            'z': self._update_depth_and_coords,
        }
        if (render_fun := update_funs.get(changed)) is not None:
            render_fun()

    def _update_depth_and_coords(self):
        if self.plane == 'coronal':
            # self.image_coords = self._model.coronal_image_coords  # todo
            self.image_coords = self._model.coronal_image_coords
            self.depth = self._model.x
        elif self.plane == 'axial':
            # self.image_coords = self._model.axial_image_coords  # todo
            self.image_coords = self._model.axial_image_coords
            self.depth = self._model.y
        elif self.plane == 'sagittal':
            # self.image_coords = self._model.sagittal_image_coords  # todo
            self.image_coords = self._model.sagittal_image_coords
            self.depth = self._model.z

    def _update_section_image(self):
        self.atlas_section_image = self._model.coronal_section_image

    def _update_coords(self):
        self.coords = tuple(np.delete(self._model.atlas_section_coords, self._axis))

    @property
    def axis_colors(self):
        colors = [(1., 0., 0., 1.),
                  (0., 1., 0., 1.),
                  (0., 0., 1., 1.)]
        visible_axes = np.delete(np.arange(3), self._axis)
        return tuple(np.array(colors)[visible_axes])

    def on_left_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        visible_axes = np.delete(np.arange(3), self._axis)
        coords = np.array(self._model.atlas_section_coords)
        coords[visible_axes[0]] = int(np.clip(y2, 0, self._model.registration_volume.shape[visible_axes[0]] - 1))
        coords[visible_axes[1]] = int(np.clip(x2, 0, self._model.registration_volume.shape[visible_axes[1]] - 1))
        x, y, z = coords
        self._model.atlas_section_coords = x, y, z
