from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

import numpy as np
from numpy import ndarray


@dataclass(frozen=True)
class AtlasTransform:
    x: float = 0.
    y: float = 0.
    z: float = 0.
    rot_lateral: float = 0.
    rot_axial: float = 0.
    rot_median: float = 0.

    def translate(self, x: float = 0., y: float = 0., z: float = 0.) -> AtlasTransform:
        return replace(self, x=self.x + x, y=self.y + y,
                       z=self.z + z)

    def rotate(self, rot_lateral: float = 0., rot_axial: float = 0., rot_median: float = 0.) -> AtlasTransform:
        return replace(self, rot_lateral=self.rot_lateral + rot_lateral, rot_axial=self.rot_axial + rot_axial,
                       rot_median=self.rot_median + rot_median)

    @property
    def position(self) -> Tuple[float, float, float]:
        return self.x, self.y, self.z

    @property
    def rotation(self) -> Tuple[float, float, float]:
        return self.rot_lateral, self.rot_axial, self.rot_median

    @property
    def affine_transform(self) -> ndarray:
        translate = np.array([
            [1, 0, 0, self.x],
            [0, 1, 0, self.y],
            [0, 0, 1, self.z],
            [0, 0, 0, 1],
        ])

        s, c, t = np.sin, np.cos, np.radians(self.rot_lateral)
        rot_lateral = np.array([
            [1,    0,     0, 0],
            [0, c(t), -s(t), 0],
            [0, s(t),  c(t), 0],
            [0,    0,     0, 1],
        ])

        s, c, t = np.sin, np.cos, np.radians(self.rot_axial)
        rot_axial = np.array([
            [c(t), 0, -s(t), 0],
            [   0, 1,     0, 0],
            [s(t), 0,  c(t), 0],
            [   0, 0,     0, 1],
        ])

        s, c, t = np.sin, np.cos, np.radians(self.rot_median)
        rot_median = np.array([
            [c(t), -s(t), 0, 0],
            [s(t),  c(t), 0, 0],
            [   0,     0, 1, 0],
            [   0,     0, 0, 1],
        ])

        return translate @ rot_lateral @ rot_axial @ rot_median
