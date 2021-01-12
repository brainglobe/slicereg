from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, NamedTuple, Dict

from numpy import ndarray
from vispy.util.transforms import translate, scale

from slicereg.models.math import affine_transform

class Plane(NamedTuple):
    x: float
    y: float
    theta: float = 0.

    def translate(self, dx: float, dy: float) -> Plane:
        return self._replace(x=self.x + dx, y=self.y + dy)

    def rotate(self, theta: float) -> Plane:
        return self._replace(theta=self.theta + theta)

    @property
    def affine_transform(self) -> ndarray:
        return (translate((self.x, self.y, 0), dtype=float)).T

class Image(NamedTuple):
    channels: ndarray
    pixel_resolution_um: float
    x: float
    y: float

    def transform(self) -> ndarray:
        s = self.pixel_resolution_um
        return scale((s, s, s)) @ translate((-self.x, -self.y, 0))


@dataclass
class Section(NamedTuple):
    channels: Dict[int, Image]
    thickness_um: float = 16.
    position_um: Tuple[float, float, float] = (0., 0., 0.)
    rotation_deg: Tuple[float, float, float] = (0., 0., 0.)

    @property
    def affine_transform(self) -> ndarray:
        x, y, z = self.position_um
        cx, cy = self.image_center
        rx, ry, rz = self.rotation_deg
        # return shift_plane(x=-cx, y=-cy) @ affine_transform(x=x, y=y, z=z, rx=rx, ry=ry, rz=rz, s=self.pixel_res_um)

    def translate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Section:
        x, y, z = self.position_um
        return self._replace(position_um=(x + dx, y + dy, z + dz))

    def rotate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Section:
        x, y, z = self.rotation_deg
        return self._replace(rotation_deg=(x + dx, y + dy, z + dz))
