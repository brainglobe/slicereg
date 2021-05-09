from dataclasses import dataclass, field
from typing import Tuple, Optional

import numpy as np

from slicereg.models.base import FrozenUpdater


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


ijk_to_xyz_matrix = np.array([
    [0, 1, 0, 0],
    [-1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])
