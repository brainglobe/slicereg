from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np


@dataclass(frozen=True)
class ImageTransformer:
    i_shift: float = 0.
    j_shift: float = 0.
    theta: float = 0.

    @property
    def shift_matrix(self) -> np.ndarray:
        """
        Translation matrix in pixel coordinate space.
        """
        return np.array([
            [1, 0, 0, self.i_shift],
            [0, 1, 0, self.j_shift],
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

    def shift_origin_to_center(self) -> ImageTransformer:
        return replace(self, j_shift=-0.5, i_shift=-0.5)


ij_to_xyz_matrix = np.array([
    [0, 1, 0, 0],
    [-1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])
