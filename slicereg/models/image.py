from __future__ import annotations

from dataclasses import dataclass, field
from typing import NamedTuple, Tuple

import numpy as np
from numpy.core.multiarray import ndarray
from vispy.util.transforms import translate, rotate


class ImagePlane(NamedTuple):
    x: float = 0.
    y: float = 0.
    theta: float = 0.

    def translate(self, dx: float, dy: float) -> ImagePlane:
        return self._replace(x=self.x + dx, y=self.y + dy)

    def rotate(self, theta: float) -> ImagePlane:
        return self._replace(theta=self.theta + theta)

    @property
    def affine_transform(self) -> ndarray:
        translation = translate((self.x, self.y, 0), dtype=float)
        rotation = rotate(self.theta, (0, 0, 1), dtype=float)
        return (rotation @ translation).T


@dataclass(frozen=True)
class SliceImage:
    channels: ndarray = field(repr=False)
    pixel_resolution_um: float

    @property
    def num_channels(self) -> int:
        return self.channels.shape[0]

    @property
    def height(self) -> int:
        return self.channels.shape[1]

    @property
    def width(self) -> int:
        return self.channels.shape[2]

    @property
    def scale_matrix(self):
        scale = 1 / self.pixel_resolution_um
        return np.diag([scale, scale, 1., 1.])

    def project_coord(self, i: int, j: int) -> ndarray:
        if not 0 <= i < self.height or not 0 <= j < self.width:
            raise ValueError(f"Coord ({i, j}) not in image.")

        return np.array([[j, -i, 0., 1.]])
