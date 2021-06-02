from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple, Optional

import numpy as np

from slicereg.core import Image
from slicereg.core.base import FrozenUpdater


@dataclass(frozen=True)
class Atlas(FrozenUpdater):
    volume: np.ndarray = field(repr=False)
    resolution_um: float
    annotation_volume: Optional[np.ndarray] = field(default=None, repr=False)

    @property
    def shared_space_transform(self) -> np.ndarray:
        return self.scale_matrix @ ijk_to_xyz_matrix

    @property
    def scale_matrix(self) -> np.ndarray:
        return np.diag((self.resolution_um, self.resolution_um, self.resolution_um, 1))

    @property
    def center(self) -> Tuple[float, float, float]:
        """Returns center coordinates, in shared physical (CCF) space."""
        d0, d1, d2 = self.volume.shape
        x, y, z = (ijk_to_xyz_matrix @ np.array([[d0, d1, d2, 1]]).T)[:3, 0]
        cx, cy, cz = tuple(dim * self.resolution_um / 2 for dim in (x, y, z))
        return cx, cy, cz

    def map_xyz_to_ijk(self, x: float, y: float, z: float) -> Optional[Tuple[int, int, int]]:
        if self.coord_is_in_volume(x=x, y=y, z=z):
            res = self.resolution_um
            return int(x // res), int(y // res), int(z // res)
        else:
            return None

    def coord_is_in_volume(self, x: float, y: float, z: float) -> bool:
        res = self.resolution_um
        shape = self.volume.shape
        return 0 <= x / res < shape[0] and 0 <= y / res < shape[1] and 0 <= z / res < shape[2]

    def make_coronal_slice_at(self, x: float) -> Image:
        if 0 <= x < self.volume.shape[0] * self.resolution_um:
            i = int(x / self.resolution_um)
            channels = self.volume[[i], :, :]
        else:
            shape = self.volume.shape
            channels = np.zeros((1, shape[1], shape[2]))
        return Image(channels=channels, resolution_um=self.resolution_um, thickness_um=self.resolution_um)

    def make_axial_slice_at(self, y: float) -> Image:
        if 0 <= y < self.volume.shape[1] * self.resolution_um:
            j = int(y / self.resolution_um)
            slice = self.volume[:, j, :]
            channels = slice[None, :, :]
        else:
            shape = self.volume.shape
            channels = np.zeros((1, shape[0], shape[2]))
        return Image(channels=channels, resolution_um=self.resolution_um, thickness_um=self.resolution_um)

    def make_sagittal_slice_at(self, z: float) -> Image:
        if 0 <= z < self.volume.shape[2] * self.resolution_um:
            k = int(z / self.resolution_um)
            slice = self.volume[:, :, k].T
            channels = slice[None, :, :]
        else:
            shape = self.volume.shape
            channels = np.zeros((1, shape[0], shape[1]))
        return Image(channels=channels, resolution_um=self.resolution_um, thickness_um=self.resolution_um)


ijk_to_xyz_matrix = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])
