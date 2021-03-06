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
    x: float = 0.
    y: float = 0.
    z: float = 0.
    rx: float = 0.
    ry: float = 0.
    rz: float = 0.

    def translate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Plane3D:
        return replace(self, x=self.x + dx, y=self.y + dy, z=self.z + dz)

    def rotate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Plane3D:
        return replace(self, rx=self.rx + dx, ry=self.ry + dy, rz=self.rz + dz)

    @property
    def position(self) -> Tuple[float, float, float]:
        return self.x, self.y, self.z

    @property
    def rotation(self) -> Tuple[float, float, float]:
        return self.rx, self.ry, self.rz

    @property
    def affine_transform(self) -> ndarray:
        r = rotate(self.rx, (1, 0, 0)) @ rotate(self.ry, (0, 1, 0)) @ rotate(self.rz, (0, 0, 1))
        t = translate((self.x, self.y, self.z))
        matrix = (r @ t).T
        assert matrix.shape == (4, 4)
        return matrix