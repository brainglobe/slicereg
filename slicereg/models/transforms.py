from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

import numpy as np
from numpy import ndarray


@dataclass(frozen=True)
class Transform3D:
    x: float = 0.
    y: float = 0.
    z: float = 0.
    rx: float = 0.
    ry: float = 0.
    rz: float = 0.

    def translate(self, x: float = 0., y: float = 0., z: float = 0.) -> Transform3D:
        return replace(self, x=self.x + x, y=self.y + y,
                       z=self.z + z)

    def rotate(self, rot_lateral: float = 0., rot_axial: float = 0., rot_median: float = 0.) -> Transform3D:
        return replace(self, rot_lateral=self.rx + rot_lateral, rot_axial=self.ry + rot_axial,
                       rot_median=self.rz + rot_median)

    @property
    def position(self) -> Tuple[float, float, float]:
        return self.x, self.y, self.z

    @property
    def rotation(self) -> Tuple[float, float, float]:
        return self.rx, self.ry, self.rz

    @property
    def affine_transform(self) -> ndarray:
        translate = np.array([
            [1, 0, 0, self.x],
            [0, 1, 0, self.y],
            [0, 0, 1, self.z],
            [0, 0, 0, 1],
        ])

        s, c, t = np.sin, np.cos, np.radians(self.rx)
        rot_lateral = np.array([
            [1,    0,     0, 0],
            [0, c(t), -s(t), 0],
            [0, s(t),  c(t), 0],
            [0,    0,     0, 1],
        ])

        s, c, t = np.sin, np.cos, np.radians(self.ry)
        rot_axial = np.array([
            [c(t), 0, -s(t), 0],
            [   0, 1,     0, 0],
            [s(t), 0,  c(t), 0],
            [   0, 0,     0, 1],
        ])

        s, c, t = np.sin, np.cos, np.radians(self.rz)
        rot_median = np.array([
            [c(t), -s(t), 0, 0],
            [s(t),  c(t), 0, 0],
            [   0,     0, 1, 0],
            [   0,     0, 0, 1],
        ])

        return translate @ rot_lateral @ rot_axial @ rot_median
