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
    image_coords: Tuple[int, int] = (0, 0)
    depth: float = 0.

    def __post_init__(self):
        HasObservableAttributes.__init__(self)
        self._model.register(self.update)

    @property
    def section_image_name(self):
        return f"{self.plane}_section_image"

    @property
    def image_coords_name(self):
        return f"{self.plane}_image_coords"

    def update(self, changed: str):
        update_funs = {
            'x': self._update_depth,
            'y': self._update_depth,
            'z': self._update_depth,
            self.image_coords_name: self._update_image_coords,
            self.section_image_name: self._update_section_image,
        }
        if (render_fun := update_funs.get(changed)) is not None:
            render_fun()

    def _update_image_coords(self):
        self.image_coords = getattr(self._model, self.image_coords_name)

    def _update_section_image(self):
        if (section_image := getattr(self._model, self.section_image_name)) is not None:
            self.atlas_section_image = section_image

    def _update_depth(self):
        if self.plane == 'coronal':
            self.depth = self._model.x
        elif self.plane == 'axial':
            self.depth = self._model.y
        elif self.plane == 'sagittal':
            self.depth = self._model.z

    @property
    def clim(self) -> Tuple[float, float]:
        return 0., 1.

    @property
    def camera_center(self) -> Tuple[float, float, float]:
        image = self.atlas_section_image
        return image.shape[1] / 2, image.shape[0] / 2, 0.

    @property
    def camera_scale(self) -> float:
        image = self.atlas_section_image
        return max(image.shape)

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
            'coronal': (1., 0., 0., 1.),
            'axial': (0., 0., 1., 1.),
            'sagittal': (0., 1., 0., 1.),
        }
        return colors[self.plane]

    def drag_left_mouse(self, x1: int, y1: int, x2: int, y2: int):
        self._model.set_pos_to_plane_indices(plane=self.plane, i=x2, j=y2)

    def click_left_mouse_button(self, x: int, y: int):
        self._model.set_pos_to_plane_indices(plane=self.plane, i=x, j=y)
