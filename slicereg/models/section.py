from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Tuple, NamedTuple
from uuid import UUID, uuid4

from numpy import ndarray
from vispy.util.transforms import translate, rotate

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
        translation = translate((self.x, self.y, 0), dtype=float)
        rotation = rotate(self.theta, (0, 0, 1), dtype=float)
        return (rotation @ translation).T


@dataclass(frozen=True)
class SliceImage:
    channels: ndarray = field(repr=False)
    pixel_resolution_um: float

    @property
    def num_channels(self) -> int:
        return self.channels.shape[0]


@dataclass(frozen=True)
class Section:
    image: SliceImage
    plane: Plane
    thickness_um: float = 16.
    position_um: Tuple[float, float, float] = (0., 0., 0.)
    rotation_deg: Tuple[float, float, float] = (0., 0., 0.)
    id: UUID = field(default_factory=uuid4)

    @property
    def affine_transform(self) -> ndarray:
        x, y, z = self.position_um
        rx, ry, rz = self.rotation_deg
        s = self.image.pixel_resolution_um
        return self.plane.affine_transform @ affine_transform(x=x, y=y, z=z, rx=rx, ry=ry, rz=rz, s=s)

    def translate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Section:
        x, y, z = self.position_um
        return replace(self, position_um=(x + dx, y + dy, z + dz))

    def rotate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Section:
        x, y, z = self.rotation_deg
        return replace(self, rotation_deg=(x + dx, y + dy, z + dz))

    def pos_from_coord(self, i: int, j: int) -> Tuple[float, float, float]:
        return float(j), -float(i), 0.
