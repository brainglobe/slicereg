from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from numpy import ndarray

from src.core.models.math import shift_plane, affine_transform


@dataclass(frozen=True)
class Section:
    channels: ndarray
    pixel_res_um: float
    width_um: float = 16.
    position_um: Tuple[float, float, float] = (0., 0., 0.)
    rotation_deg: Tuple[float, float, float] = (0., 0., 0.)

    @property
    def affine_transform(self) -> ndarray:
        x, y, z = self.position_um
        cx, cy = self.image_center
        rx, ry, rz = self.rotation_deg
        return shift_plane(x=-cx, y=-cy) @ affine_transform(x=x, y=y, z=z, rx=rx, ry=ry, rz=rz, s=self.pixel_res_um)

    @property
    def image_center(self) -> Tuple[float, float]:
        return self.channels.shape[2] / 2, self.channels.shape[1] / 2

    def translate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Section:
        x, y, z = self.position_um
        return Section(
            channels=self.channels,
            pixel_res_um=self.pixel_res_um,
            position_um=(x + dx, y + dy, z + dz),
            rotation_deg=self.rotation_deg
        )

    def rotate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Section:
        x, y, z = self.rotation_deg
        return Section(
            channels=self.channels,
            pixel_res_um=self.pixel_res_um,
            position_um=self.position_um,
            rotation_deg=(x + dx, y + dy, z + dz),
        )
