from dataclasses import dataclass, field

import numpy as np

from slicereg.models.base import FrozenUpdater


@dataclass(frozen=True)
class Atlas(FrozenUpdater):
    volume: np.ndarray = field(repr=False)
    resolution_um: float

    @property
    def affine_transform(self) -> np.ndarray:
        # need -90 degree rotation (ignore left-handed nature of Z coords, since don't exist)
        ijk_to_xyz_matrix = np.array([
            [0, 1, 0, 0],
            [-1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])
        return self.scale_matrix @ ijk_to_xyz_matrix

    @property
    def scale_matrix(self) -> np.ndarray:
        return np.diag((self.resolution_um, self.resolution_um, self.resolution_um, 1))
