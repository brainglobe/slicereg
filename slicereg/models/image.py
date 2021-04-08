from __future__ import annotations

from dataclasses import dataclass, field, replace
from functools import cached_property

import numpy as np


@dataclass(frozen=True)
class Image:
    channels: np.ndarray = field(repr=False)
    i_shift: float = 0.
    j_shift: float = 0.
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

    @cached_property
    def inds_homog(self) -> np.ndarray:
        """All the i,j indices in the image as a 4 x (width x height) homogonous vertex array"""
        return inds_homog(height=self.height, width=self.width)

    @property
    def shift_matrix(self) -> np.ndarray:
        """
        Translation matrix in pixel coordinate space.
        """
        return np.array([
            [1, 0, 0, self.i_shift * self.height],
            [0, 1, 0, self.j_shift * self.width],
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
    def affine_transform(self) -> np.ndarray:
        return self.rot_matrix @ self.shift_matrix

    def shift_origin_to_center(self) -> Image:
        return replace(self, j_shift=-0.5, i_shift=-0.5)


def inds_homog(height: int, width: int) -> np.ndarray:
    return np.mgrid[:height, :width, :1, 1:2].reshape(-1, width * height)


def ij_homog(i: int, j: int) -> np.ndarray:
    return np.array([[i, j, 0, 1]]).T
