from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from numpy.core._multiarray_umath import ndarray
from vispy.util.transforms import translate, scale, rotate


@dataclass(frozen=True)
class Section:
    channels: ndarray
    pixel_res_um: float
    width_um: float = 16.
    position_um: Tuple[float, float, float] = (0., 0., 0.)
    rotation_deg: Tuple[float, float, float] = (0., 0., 0.)

    @property
    def model_matrix(self) -> ndarray:
        cx, cy = self.image_center
        rx, ry, rz = self.rotation_deg
        return \
            translate((-cx, -cy, 0)) @ \
            scale((self.pixel_res_um,) * 3) @ \
            rotate(rx, (1, 0, 0)) @ \
            rotate(ry, (0, 1, 0)) @ \
            rotate(rz, (0, 0, 1)) @ \
            translate(self.position_um)

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
