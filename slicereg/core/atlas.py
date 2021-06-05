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
        return self.scale_matrix

    @property
    def scale_matrix(self) -> np.ndarray:
        return np.diag((self.resolution_um, self.resolution_um, self.resolution_um, 1))

    @property
    def center(self) -> Tuple[float, float, float]:
        """Returns center coordinates, in shared physical (CCF) space."""
        d0, d1, d2 = self.volume.shape
        x, y, z = np.array([[d0, d1, d2, 1]]).transpose()[:3, 0]
        cx, cy, cz = tuple(dim * self.resolution_um / 2 for dim in (x, y, z))
        return cx, cy, cz

    def coord_is_in_volume(self, x: float, y: float, z: float) -> bool:
        res = self.resolution_um
        shape = self.volume.shape
        return 0 <= x / res < shape[0] and 0 <= y / res < shape[1] and 0 <= z / res < shape[2]

    def make_coronal_slice_at(self, x: float) -> Image:
        if self.coord_is_in_volume(x=x, y=0, z=0):
            channels = self.volume[int(x / self.resolution_um), :, :]
        else:
            channels = np.zeros((self.volume.shape[1], self.volume.shape[2]))
        return Image(channels=channels[None, :, :], resolution_um=self.resolution_um, thickness_um=self.resolution_um)

    def make_axial_slice_at(self, y: float) -> Image:
        if self.coord_is_in_volume(x=0, y=y, z=0):
            channels = self.volume[:, int(y / self.resolution_um), :]
        else:
            channels = np.zeros((self.volume.shape[0], self.volume.shape[2]))
        return Image(channels=channels[None, :, :], resolution_um=self.resolution_um, thickness_um=self.resolution_um)

    def make_sagittal_slice_at(self, z: float) -> Image:
        if self.coord_is_in_volume(x=0, y=0, z=z):
            channels = self.volume[:, :, int(z / self.resolution_um)].T
        else:
            channels = np.zeros((self.volume.shape[0],  self.volume.shape[1]))
        return Image(channels=channels[None, :, :], resolution_um=self.resolution_um, thickness_um=self.resolution_um)
