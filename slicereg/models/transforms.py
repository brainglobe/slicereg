from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

import numpy as np
from numpy import ndarray
from vispy.util.transforms import translate, rotate



@dataclass(frozen=True)
class AtlasTransform:
    right: float = 0.
    superior: float = 0.
    anterior: float = 0.
    rot_lateral: float = 0.
    rot_axial: float = 0.
    rot_median: float = 0.

    def translate(self, right: float = 0., superior: float = 0., anterior: float = 0.) -> AtlasTransform:
        return replace(self, right=self.right + right, superior=self.superior + superior, anterior=self.anterior + anterior)

    def rotate(self, rot_lateral: float = 0., rot_axial: float = 0., rot_median: float = 0.) -> AtlasTransform:
        return replace(self, rot_lateral=self.rot_lateral + rot_lateral, rot_axial=self.rot_axial + rot_axial, rot_median=self.rot_median + rot_median)

    @property
    def position(self) -> Tuple[float, float, float]:
        return self.right, self.superior, self.anterior

    @property
    def rotation(self) -> Tuple[float, float, float]:
        return self.rot_lateral, self.rot_axial, self.rot_median

    @property
    def affine_transform(self) -> ndarray:

        # r = rotate(self.rot_lateral, (1, 0, 0)).T @ rotate(self.rot_axial, (0, 1, 0)).T @ rotate(self.rot_median, (0, 0, 1)).T
        # t = translate((self.right, self.superior, self.anterior)).T
        # matrix = t @ r

        translate = np.array([
            [1, 0, 0, self.right],
            [0, 1, 0, self.superior],
            [0, 0, 1, self.anterior],
            [0, 0, 0, 1],
        ])

        # assert matrix.shape == (4, 4)
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