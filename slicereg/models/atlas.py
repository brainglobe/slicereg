from dataclasses import dataclass, field

import numpy as np

from slicereg.models.base import FrozenUpdater


@dataclass(frozen=True)
class Atlas(FrozenUpdater):
    volume: np.ndarray = field(repr=False)
    resolution_um: float

    @property
    def shared_space_transform(self) -> np.ndarray:
        return self.scale_matrix @ ijk_to_xyz_matrix

    @property
    def scale_matrix(self) -> np.ndarray:
        return np.diag((self.resolution_um, self.resolution_um, self.resolution_um, 1))


ijk_to_xyz_matrix = np.array([
    [0, 1, 0, 0],
    [-1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])
