from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

from numpy import ndarray
from vispy.util.transforms import translate, rotate


@dataclass(frozen=True)
class Image2DTransform:
    i: float = 0.
    j: float = 0.
    theta: float = 0.

    def translate(self, i: float, j: float) -> Image2DTransform:
        return replace(self, i=self.i + i, j=self.j + j)

    def rotate(self, theta: float) -> Image2DTransform:
        return replace(self, theta=self.theta + theta)

    @property
    def affine_transform(self) -> ndarray:
        translation = translate((self.i, self.j, 0), dtype=float)
        rotation = rotate(self.theta, (0, 0, 1), dtype=float)
        matrix = (rotation @ translation).T
        assert matrix.shape == (4, 4)
        return matrix


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
        r = rotate(self.rot_lateral, (1, 0, 0)) @ rotate(self.rot_axial, (0, 1, 0)) @ rotate(self.rot_median, (0, 0, 1))
        t = translate((self.right, self.superior, self.anterior))
        matrix = (r @ t).T
        assert matrix.shape == (4, 4)
        return matrix