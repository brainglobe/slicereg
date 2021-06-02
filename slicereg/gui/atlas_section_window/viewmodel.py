from dataclasses import dataclass, field
from typing import Tuple

import numpy as np

from slicereg.gui.app_model import AppModel
from slicereg.utils.observable import HasObservableAttributes


@dataclass(unsafe_hash=True)
class AtlasSectionViewModel(HasObservableAttributes):
    _model: AppModel = field(hash=False)
    plane: str = 'coronal'
    atlas_section_image: np.ndarray = np.zeros(shape=(3, 3), dtype=np.uint16)
    coords: Tuple[int, int] = (0, 0)
    camera_center: Tuple[float, float, float] = (1, 1, 0)
    camera_scale: float = 1.
    section_scale: Tuple[float, float, float] = (1., 1., 1.)

    def __post_init__(self):
        HasObservableAttributes.__init__(self)
        self._model.register(self.update)

    def update(self, changed: str):
        update_funs = {
            self._section_image_name: self._update_section_image,
            'atlas_resolution': self._update_section_image,
            'x': self._update_image_coords,
            'y': self._update_image_coords,
            'z': self._update_image_coords,
        }
        if (render_fun := update_funs.get(changed)) is not None:
            render_fun()

    def _update_image_coords(self):
        x, y, z = self._model.x, self._model.y, self._model.z
        coords = {
            'coronal': (x, z),
            'axial': (y, z),
            'sagittal': (y, x),
        }
        self.coords = coords[self.plane]

    def _update_section_image(self):
        if (image := getattr(self._model, self._section_image_name)) is not None:
            self.atlas_section_image = image
            if self._model.atlas_resolution is not None:
                res = self._model.atlas_resolution
                self.camera_center = (image.shape[1] / 2 * res, image.shape[0] / 2 * res, 0.)
                self.camera_scale = max(image.shape) * res
                self.section_scale = (res, res, 1.)

    @property
    def _section_image_name(self):
        return f"{self.plane}_atlas_image"

    @property
    def clim(self) -> Tuple[float, float]:
        return np.min(self.atlas_section_image), np.max(self.atlas_section_image)

    @property
    def vertical_line_color(self) -> Tuple[float, float, float, float]:
        colors = {
            'coronal': (0., 1., 0., 1.),
            'axial': (1., 0., 0., 1.),
            'sagittal': (1., 0., 0., 1.),
        }
        return colors[self.plane]

    @property
    def horizontal_line_color(self) -> Tuple[float, float, float, float]:
        colors = {
            'coronal': (0., 0., 1., 1.),
            'axial': (0., 0., 1., 1.),
            'sagittal': (0., 1., 0., 1.),
        }
        return colors[self.plane]

    def drag_left_mouse(self, x1: int, y1: int, x2: int, y2: int):
        self._update_section_position(x2, y2)

    def click_left_mouse_button(self, x: int, y: int):
        self._update_section_position(x, y)

    def _update_section_position(self, x, y):
        if self.plane == 'coronal':
            self._model.update_section(z=x, x=y)  # up-down, left-right
        elif self.plane == 'axial':
            self._model.update_section(z=x, y=y)  # forward-back, left-right
        elif self.plane == 'sagittal':
            self._model.update_section(x=x, y=y)  # forward-back, up-down
