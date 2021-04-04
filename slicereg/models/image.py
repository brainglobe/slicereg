from __future__ import annotations

from dataclasses import dataclass, field, replace

import numpy as np
from scipy import ndimage


@dataclass(frozen=True)
class ImageData:
    channels: np.ndarray = field(repr=False)
    pixel_resolution_um: float
    x_shift: float = 0.
    y_shift: float = 0.
    theta: float = 0.

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
    def aspect_ratio(self) -> float:
        return self.width / self.height

    def shift_origin_to_center(self) -> ImageData:
        return replace(self, x_shift=-0.5, y_shift=-0.5)

    @property
    def shift_matrix(self) -> np.ndarray:
        return np.array([
            [1, 0, 0, self.y_shift * self.width],
            [0, 1, 0, self.x_shift * self.height],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])

    @property
    def rot_matrix(self) -> np.ndarray:
        """
        Get 4x4  Z rotation matrix as in https://en.wikipedia.org/wiki/Rotation_matrix#Basic_rotations
        """
        t, cos, sin = np.radians(self.theta), np.cos, np.sin
        return np.array([
            [cos(t), -sin(t), 0, 0],
            [sin(t), cos(t), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])

    @property
    def scale_matrix(self) -> np.ndarray:
        scale = self.pixel_resolution_um
        matrix = np.diag([scale, scale, 1., 1.])
        return matrix

    @property
    def affine_transform(self) -> np.ndarray:
        return self.scale_matrix @ self.rot_matrix @ self.shift_matrix

    def project_coord(self, i: int, j: int) -> np.ndarray:
        if not 0 <= i < self.height or not 0 <= j < self.width:
            raise ValueError(f"Coord ({i, j}) not in image.")

        return np.array([[j, -i, 0., 1.]])

    def resample(self, resolution_um: float) -> ImageData:
        if resolution_um <= 0:
            raise ValueError("Resolution must be positive.")

        zoom_level = self.pixel_resolution_um / resolution_um
        zoomed_channels = ndimage.zoom(self.channels, zoom=(1, zoom_level, zoom_level))
        return replace(self, channels=zoomed_channels, pixel_resolution_um=resolution_um)
