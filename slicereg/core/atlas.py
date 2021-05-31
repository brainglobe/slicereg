from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple, Optional, NamedTuple

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

    def orthogonal_sections_at(self, x: float, y: float, z: float) -> Optional[AtlasSections]:
        ijk = self.map_xyz_to_ijk(x=x, y=y, z=z)
        if ijk is not None:
            i, j, k = ijk
            return AtlasSections(coronal=self.volume[i, :, :], axial=self.volume[:, j, :], sagittal=self.volume[:, :, k])
        else:
            return None

    def coord_is_in_volume(self, x: float, y: float, z: float) -> bool:
        res = self.resolution_um
        shape = self.volume.shape
        return 0 <= x / res < shape[0] and 0 <= y / res < shape[1] and 0 <= z / res < shape[2]

    def get_coronal_image(self, x: float) -> Image:
        if 0 <= x < self.volume.shape[0] * self.resolution_um:
            i = int(x / self.resolution_um)
            channels = self.volume[[i], :, :]
        else:
            channels = np.zeros_like(self.volume[[0], :, :])
        return Image(channels=channels, resolution_um=self.resolution_um, thickness_um=self.resolution_um)


ijk_to_xyz_matrix = np.array([
    [0, 1, 0, 0],
    [-1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])


class AtlasSections(NamedTuple):
    coronal: np.ndarray
    axial: np.ndarray
    sagittal: np.ndarray
