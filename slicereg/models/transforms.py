from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

from numpy import ndarray
from vispy.util.transforms import translate, rotate


@dataclass(frozen=True)
class Plane2D:
    x: float = 0.
    y: float = 0.
    theta: float = 0.

    def translate(self, dx: float, dy: float) -> Plane2D:
        return replace(self, x=self.x + dx, y=self.y + dy)

    def rotate(self, theta: float) -> Plane2D:
        return replace(self, theta=self.theta + theta)

    @property
    def affine_transform(self) -> ndarray:
        translation = translate((self.x, self.y, 0), dtype=float)
        rotation = rotate(self.theta, (0, 0, 1), dtype=float)
        matrix = (rotation @ translation).T
        assert matrix.shape == (4, 4)
        return matrix


@dataclass(frozen=True)
class Plane3D:
    right: float = 0.
    superior: float = 0.
    anterior: float = 0.
    rot_lateral: float = 0.
    rot_axial: float = 0.
    rot_median: float = 0.

    def translate(self, right: float = 0., superior: float = 0., anterior: float = 0.) -> Plane3D:
        return replace(self, right=self.right + right, superior=self.superior + superior, anterior=self.anterior + anterior)

    def rotate(self, rot_lateral: float = 0., rot_axial: float = 0., rot_median: float = 0.) -> Plane3D:
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