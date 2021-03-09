from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy import ndarray


@dataclass(frozen=True)
class ImageData:
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
        matrix = np.diag([scale, scale, 1., 1.])
        assert matrix.shape == (4, 4)
        return matrix

    def project_coord(self, i: int, j: int) -> ndarray:
        if not 0 <= i < self.height or not 0 <= j < self.width:
            raise ValueError(f"Coord ({i, j}) not in image.")

        return np.array([[j, -i, 0., 1.]])

    def resample(self, scale: float) -> ImageData:

        return ImageData(
            channels=self.channels[:, ::int(1/scale), ::int(1/scale)],
            pixel_resolution_um=self.pixel_resolution_um / scale
        )