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
    camera_center: Tuple[float, float, float] = (1, 1, 0)
    camera_scale: float = 1.
    section_scale: Tuple[float, float, float] = (1., 1., 1.)
    vertical_line_pos: float = 0
    horizontal_line_pos: float = 0

    def __post_init__(self):
        HasObservableAttributes.__init__(self)
        self._model.register(self.update)

    def update(self, changed: str):
        update_funs = {
            self._section_image_name: self._update_section_image,
            self._horizontal_coord: self._update_horizontal_line,
            self._vertical_coord: self._update_vertical_line,
        }
        if (render_fun := update_funs.get(changed)) is not None:
            render_fun()

    @property
    def _horizontal_coord(self) -> str:
        return {'coronal': 'z', 'axial': 'z', 'sagittal': 'x'}[self.plane]

    def _update_horizontal_line(self):
        self.horizontal_line_pos = getattr(self._model, self._horizontal_coord)

    @property
    def _vertical_coord(self) -> str:
        return {'coronal': 'y', 'axial': 'x', 'sagittal': 'y'}[self.plane]

    def _update_vertical_line(self):
        self.vertical_line_pos = getattr(self._model, self._vertical_coord)

    def _update_section_position(self, x, y):
        if self.plane == 'coronal':
            self._model.update_section(y=x, z=y)  # left-right, up-down
        elif self.plane == 'axial':
            self._model.update_section(x=x, z=y)  # left-right, forward-back
        elif self.plane == 'sagittal':
            self._model.update_section(x=y, y=x)  # up-down, forward-back

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

    @staticmethod
    def _color_from_axis_name(axis: str) -> Tuple[float, float, float, float]:
        return {
            'x': (1., 0., 0., 1.),
            'y': (0., 1., 0., 1.),
            'z': (0., 0., 1., 1.),
        }[axis]

    @property
    def vertical_line_color(self) -> Tuple[float, float, float, float]:
        return self._color_from_axis_name(axis=self._vertical_coord)

    @property
    def horizontal_line_color(self) -> Tuple[float, float, float, float]:
        return self._color_from_axis_name(axis=self._horizontal_coord)

    def drag_left_mouse(self, x1: int, y1: int, x2: int, y2: int):
        self._update_section_position(x2, y2)

    def click_left_mouse_button(self, x: int, y: int):
        self._update_section_position(x, y)
