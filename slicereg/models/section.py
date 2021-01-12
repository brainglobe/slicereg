from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, NamedTuple, Dict

from numpy import ndarray
from vispy.util.transforms import translate, rotate


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
        translation = translate((self.x, self.y, 0), dtype=float)
        rotation = rotate(self.theta, (0, 0, 1), dtype=float)
        return (rotation @ translation).T


class SliceImage(NamedTuple):
    channels: ndarray
    pixel_resolution_um: float


@dataclass
class Section(NamedTuple):
    image: SliceImage
    image_plane: Plane
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
